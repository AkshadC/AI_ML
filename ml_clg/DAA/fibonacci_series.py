def fibonacci(n):
    n1 = 0
    n2 = 1
    for i in range(2, n + 1):
        n3 = n1 + n2
        n1 = n2
        n2 = n3
        print(n3, end=" ")


def fibonacci_series(i):
    if i <= 1:
        return i
    else:
        return fibonacci_series(i - 1) + fibonacci_series(i - 2)


if __name__ == "__main__":
    n = int(input("ENTER THE NO OF  FIBONACCI NUMBERS YOU WANT TO PRINT :"))
    print("FIBO BY ITERATION : ", end=" ")
    fibonacci(n)
    print()
    print("FIBO BY RECURSION : ", end=" ")
    if n != 0:
        print("Fibonacci Series:", end=" ")
        for i in range(n):
            print(fibonacci_series(i), end=" ")
