from bz2 import BZ2Compressor
from lzma import LZMACompressor
from os import get_terminal_size
from random import random
from string import printable
from time import time

def progress_bar(iterable):
    total = len(iterable)
    start_time = time()
    columns, lines = get_terminal_size()
    bar_width = columns - 20 if columns < 60 else 40

    def show_progress(iteration):
        progress = int(bar_width * iteration / total)
        elapsed_time = time() - start_time
        minutes, seconds = divmod(elapsed_time, 60)
        hours, minutes = divmod(minutes, 60)
        elapsed_str = "{:01}:{:02}:{:02}".format(
            int(hours), int(minutes), int(seconds)
        )

        bar = "=" * progress + " " * (bar_width - progress)
        percent_complete = round((iteration / total) * 100, 1)
        output = f"\r[{bar}] {percent_complete: >5}% {elapsed_str}"
        print(output, end='', flush=True)

    for i, item in enumerate(iterable, 1):
        yield item
        show_progress(i)

    print()  # newline after progress bar completion

def pi_wallis(n):
    pi = 2.
    for i in progress_bar(range(1, n)):
        left = (2. * i) / (2. * i - 1.)
        right = (2. * i) / (2. * i + 1.)
        pi = pi * left * right

def fibonacci_recursive(n):
    def fibonacci(n):
        if n <= 1:
            return 1
        else:
            return fibonacci(n - 1) + fibonacci(n - 2)
    for i in progress_bar(range(1, n)):
        fibonacci(i)

def fibonacci_iterative(n):
    first, second = 0, 1
    for _ in progress_bar(range(2, n)):
        first, second = second, first + second

def multiply_matrices(size):
    A = [[random() for _ in range(size)] for _ in range(size)]
    B = [[random() for _ in range(size)] for _ in range(size)]
    C = [[0 for _ in range(size)] for _ in range(size)]

    for i in progress_bar(range(size)):
        for j in range(size):
            C[i][j] = sum(A[i][k] * B[k][j] for k in range(size))

def compress(n, algo_class, algo_args=[]):
    algo = algo_class(*algo_args)
    data = printable.encode()
    for i in progress_bar(range(n)):
        algo.compress(data * n)
    algo.flush()

def benchmarks():
    # Timing Pi calculation using Wallis product
    print('Calculate Pi using Wallis product:')
    start_time = time()
    for _ in range(50):
        pi_wallis(2**21 + 2**20)
    elapsed_time = time() - start_time
    print('Time for Pi calculation:', round(elapsed_time, 4), 'seconds')
    
    # Timing BZ2 compression
    print('Compress using BZ2 algorithm:')
    start_time = time()
    for _ in range(50):
        compress(n=2**10, algo_class=BZ2Compressor, algo_args=[1])
    elapsed_time = time() - start_time
    print('Time for BZ2 compression:', round(elapsed_time, 4), 'seconds')

    # Timing LZMA compression
    print('Compress using LZMA algorithm:')
    start_time = time()
    for _ in range(50):
        compress(n=2**11 + 2**10, algo_class=LZMACompressor)
    elapsed_time = time() - start_time
    print('Time for LZMA compression:', round(elapsed_time, 4), 'seconds')

    # Timing recursive Fibonacci
    print('Calculate Fibonacci numbers recursively:')
    start_time = time()
    for _ in range(50):
        fibonacci_recursive(2**5 + 2**2 + 2 + 1)
    elapsed_time = time() - start_time
    print('Time for recursive Fibonacci:', round(elapsed_time, 4), 'seconds')

    # Timing iterative Fibonacci
    print('Calculate Fibonacci numbers iteratively:')
    start_time = time()
    for _ in range(50):
        fibonacci_iterative(2**19 + 2**18)
    elapsed_time = time() - start_time
    print('Time for iterative Fibonacci:', round(elapsed_time, 4), 'seconds')

    # Timing matrix multiplication
    print('Multiply matrices:')
    start_time = time()
    for _ in range(50):
        multiply_matrices(2**9)
    elapsed_time = time() - start_time
    print('Time for matrix multiplication:', round(elapsed_time, 4), 'seconds')

def main():
    benchmarks()

if __name__ == "__main__":
    main()

