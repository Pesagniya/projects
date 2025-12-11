
# Creates a list of Trues up to limit, then marks non-primes as False by iterating through multiples until the square root of limit
def eratosthenes(limit):

    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]  # 0 and 1 are not prime numbers

    for num in range(2, int(limit**0.5) + 1):
        if sieve[num]:
            for multiple in range(num * num, limit + 1, num):
                sieve[multiple] = False

    return [num for num, is_prime in enumerate(sieve) if is_prime]

limit = int(input())

print(eratosthenes(limit))