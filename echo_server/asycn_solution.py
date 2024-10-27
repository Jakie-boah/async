from asyncio import AbstractEventLoop
import asyncio
import signal
import socket
import logging
from typing import Set, List


async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        while data := await loop.sock_recv(connection, 1024):
            if b'boom' in data:
                raise Exception("Неожиданная ошибка сети")
            await loop.sock_sendall(connection, data)
    except Exception as e:
        logging.exception(e)

    finally:
        connection.close()


echo_tasks = []


async def listen_for_connections(server_socket: socket,
                                 loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Получен запрос на подключение от {address}")
        echo_tasks.append(asyncio.create_task(echo(connection, loop)))


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    await listen_for_connections(server_socket, asyncio.get_event_loop())


loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
