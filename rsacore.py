from math import gcd
from random import randrange


class RSACore:
    integer_size = 8
    block_size = 4

    @classmethod
    def extended_euclidean(cls, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = cls.extended_euclidean(b % a, a)
            return g, x - (b // a) * y, y

    @classmethod
    def multiplicative_inverse(cls, e, phi):
        g, x, y = cls.extended_euclidean(e, phi)
        if g != 1:
            return None
        return x % phi

    @classmethod
    def euler_totient(cls, p, q):
        return (p - 1) * (q - 1)

    @classmethod
    def miller_rabin(cls, n, rounds=40):
        if n == 2 or n == 3:
            return True

        if n % 2 == 0:
            return False

        r, s = 0, n - 1
        while s % 2 == 0:
            r += 1
            s //= 2

        for _ in range(rounds):
            a = randrange(2, n - 1)
            x = pow(a, s, n)
            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @classmethod
    def get_random_prime(cls, lower, upper, max_attempts=50):
        for _ in range(max_attempts):
            num = randrange(lower, upper + 1)
            if cls.miller_rabin(num):
                return num
        return None

    @classmethod
    def generate_key_pair(cls):
        p, q = None, None
        while p is None or q is None or p == q:
            p, q = cls.get_random_prime(65536, 4294967295), cls.get_random_prime(65536, 4294967295)

        n = p * q
        phi = cls.euler_totient(p, q)

        e = randrange(1, phi)
        div = gcd(e, phi)

        # Ensure that e and phi are coprime
        while div != 1:
            e = randrange(1, phi)
            div = gcd(e, phi)

        d = cls.multiplicative_inverse(e, phi)

        return (e, n), (d, n)


if __name__ == "__main__":
    print(RSACore.generate_key_pair())
