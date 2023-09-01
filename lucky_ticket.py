from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread
from multiprocessing import Process, Pool, Manager


def is_lucky(ticket_number: int, ticket_len: int):
    add_count = ticket_len - len(str(ticket_number))
    ticket_number = "0" * add_count + str(ticket_number)
    first_half = ticket_number[0:ticket_len // 2]
    second_half = ticket_number[ticket_len // 2:]
    first_sum = sum([int(i) for i in first_half])
    second_sum = sum([int(i) for i in second_half])
    if first_sum == second_sum:
        return 1
    return 0


def tickets_handler(start, end, ticket_len: int, counter: list):
    count = 0
    for num in range(start, end):
        count += is_lucky(num, ticket_len)
    counter.append(count)


def lucky_threads(ticket_length, num_of_threads):
    numbers_per_thread = int("9" * ticket_length) // num_of_threads
    threads = []
    lucky_counter = []
    for i in range(num_of_threads):
        start_t = i * numbers_per_thread
        end_t = (i+1) * numbers_per_thread
        threads.append(Thread(target=tickets_handler, args=(start_t, end_t, ticket_length, lucky_counter)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"Lucky tickets:{sum(lucky_counter)}")


def lucky_processes(ticket_length, num_of_processes):
    numbers_per_thread = int("9" * ticket_length) // num_of_processes
    processes = []
    manager = Manager()
    p_lucky_counter = manager.list()
    for i in range(num_of_processes):
        start_p = i * numbers_per_thread
        end_p = (i+1) * numbers_per_thread
        processes.append(Process(target=tickets_handler, args=(start_p, end_p, ticket_length, p_lucky_counter)))
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(f"Lucky tickets: {sum(p_lucky_counter)}")


def lucky_thread_pool(ticket_length, numbers, num_of_threads):
    with ThreadPoolExecutor(max_workers=num_of_threads) as executor:
        count_with_t = executor.map(is_lucky, numbers, [ticket_length] * len(numbers))
        print(f"Lucky tickets: {sum(count_with_t)}")


def lucky_process_pool(ticket_length, numbers, num_of_processes):
    p = Pool(num_of_processes)
    count_with_p = p.starmap(is_lucky, [(num, ticket_length) for num in numbers])
    print(f"Lucky tickets: {sum(count_with_p)}")


def main():
    ticket_length = 6
    numbers = range(0, int("9"*ticket_length))
    number_of_processes_threads = 4

    t_start = datetime.now()
    lucky_threads(ticket_length, number_of_processes_threads)
    print(f"Completed in {datetime.now() - t_start}")

    t_start = datetime.now()
    lucky_processes(ticket_length, number_of_processes_threads)
    print(f"Completed in {datetime.now() - t_start}")

    t_start = datetime.now()
    lucky_thread_pool(ticket_length, numbers, number_of_processes_threads)
    print(f"Completed in {datetime.now() - t_start}")

    t_start = datetime.now()
    lucky_process_pool(ticket_length, numbers, number_of_processes_threads)
    print(f"Completed in {datetime.now() - t_start}")


if __name__ == '__main__':
    main()
