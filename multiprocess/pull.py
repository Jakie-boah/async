from multiprocessing import Pool
import multiprocessing


def say_hello(name: str) -> str:
    return f"Hello {name}"


def blocking_exec(process_pool: Pool):
    hi_jeff = process_pool.apply(say_hello, args=('Jeff',))  # блокирует выполнение
    hi_john = process_pool.apply(say_hello, args=('John',))
    print(hi_jeff)
    print(hi_john)


def async_exec(process_pool: Pool):
    hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))  # НЕ блокирует выполнение
    hi_john = process_pool.apply_async(say_hello, args=('John',))
    print(hi_jeff.get())
    print(hi_john.get())


if __name__ == '__main__':
    with Pool() as process_pool:
        async_exec(process_pool)
