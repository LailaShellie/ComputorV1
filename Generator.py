import random

if __name__ == '__main__':
    a = random.uniform(-100, 100)
    b = random.uniform(-100, 100)
    c = random.uniform(-100, 100)
    print("{0:.2f} * X^2 + {1:.2f} * X^1 + {2:.2f} * X^0 = 0".format(a, b, c))
