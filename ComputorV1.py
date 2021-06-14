import ply.lex as lex
import ply.yacc as yacc
import sys
import numpy as np
from matplotlib import pyplot as plt


tokens = (
    'NUM', 'VARIABLE', 'PLUS_SIGN', 'MINUS_SIGN', 'MULTIPLICATION_SIGN'
)

t_PLUS_SIGN = r'\+'
t_MINUS_SIGN = r'-'
t_MULTIPLICATION_SIGN = r'\*'
t_ignore = r' '

def t_error(t):
    t.lexer.skip(1)

def t_NUM(t):
    r'-?[0-9]*\.?[0-9]+'
    if "." in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_VARIABLE(t):
    r'X(\^[0-2])?'
    if t.value == "X":
        t.value = "X^1"
    return t


lexer = lex.lex()

values = [0, 0, 0]

precedence = (
    ('left', 'PLUS_SIGN', 'MINUS_SIGN'),
    ('left', 'MULTIPLICATION_SIGN')
)

def p_getValues(p):
    '''
    expression : NUM MULTIPLICATION_SIGN VARIABLE
    | VARIABLE
    '''
    if len(p) == 4:
        values[int(p[3].split('^')[1])] += p[1]
    else:
        values[int(p[1].split('^')[1])] += 1
        print(values)
    p[0] = 0

def p_calcExpNum(p):
    '''
    expression : expression PLUS_SIGN NUM
    | expression MINUS_SIGN NUM
    | NUM
    '''
    if len(p) == 2:
        values[0] += p[1]
    elif p[2] == '+':
        values[0] += p[3]
    else:
        values[0] -= p[3]

def p_summaryExp(p):
    '''
    expression : expression PLUS_SIGN NUM MULTIPLICATION_SIGN VARIABLE
    | expression PLUS_SIGN VARIABLE
    '''
    if len(p) == 6:
        values[int(p[5].split('^')[1])] += p[3]
    else:
        values[int(p[3].split('^')[1])] += 1

def p_subtractionExp(p):
    '''
    expression : expression MINUS_SIGN NUM MULTIPLICATION_SIGN VARIABLE
    | expression MINUS_SIGN VARIABLE
    '''
    if len(p) == 6:
        p[3] = -p[3]
        values[int(p[5].split('^')[1])] += p[3]
    else:
        values[int(p[3].split('^')[1])] += -1

def p_error(p):

    err = str(p)
    print (err)
    if "NUM" in err:
        print("Wrong format of number in ({} sym".format(err.split(',')[3]))
    if "VARIABLE" in err:
        print("Wrong format of number in ({} sym".format(err.split(',')[3]))
    exit()

parser = yacc.yacc()

def ft_sqrt(n):
    return n**0.5

def get_degree(a, b, c):
    if a != 0:
        print("Polynomial degree: 2")
        return 2
    elif b != 0:
        print("Polynomial degree: 1")
        return 1
    else:
        print("Polynomial degree: 0")
        return 0

def solve_second_degree(a, b, c):
    d = b ** 2 - 4 * a * c

    if d > 0:
        x1 = ((-b + ft_sqrt(d)) / (2 * a))
        x2 = ((-b - ft_sqrt(d)) / (2 * a))
        print ("Discriminant is strictly positive, the two solutions are:\n{}\n{}".format(x2, x1))
        return [x1, x2]
    elif d == 0:
        x = -b / (2 * a)
        print ("The solution is:\n{}".format(x))
        return [x]
    elif d < 0:
        y1 = ft_sqrt(-d) / (2 * a)
        if y1 < 0:
            y1 = str(-b / (2 * a)) + ' + ' + "{}i".format(-y1)
        else:
            y1 = str(-b / (2 * a)) + ' - ' + "{}i".format(y1)
        y2 = ft_sqrt(-d) / (2 * a)
        if y2 < 0:
            y2 = str(-b / (2 * a)) + ' - ' + "{}i".format(-y2)
        else:
            y2 = str(-b / (2 * a)) + ' + ' + "{}i".format(y2)
        print("Discriminant is strictly negative, the two complex solutions are:\n{}\n{}".format(y1, y2))
        return [y1, y2]

def solve_first_degree(b, c):
    if c == 0:
        print("The solution is:\n0")
        return [0]
    else:
        print("The solution is:\n{}".format(float(-c/b)))
        return [float(-c/b)]

def solve_zero_degree(c):
    if c != 0:
        print("There is no solution")
    else:
        print("The solution is all real numbers")
    return None


def solve_equation(a, b, c):

    degree = get_degree(a, b, c)
    if degree == 2:
        return solve_second_degree(a, b, c)
    elif degree == 1:
        return solve_first_degree(b, c)
    elif degree == 0:
        return solve_zero_degree(c)


def get_polynom_values(x, coeffs):
    o = get_degree(a, b, c) + 1
    y = 0
    for i in range(o):
        y += coeffs[i]*x**i
    return y

if __name__ == '__main__':
    args = sys.argv
    graf = 0

    if args.__len__() == 1:
        print ("Usage: enter equation\nExample: X^2 + X - 10 = 0\nOptions: -g draw graf")
        exit()
    elif args.__len__() == 3:
        if args[2] == "-g":
            graf = 1
        else:
            print ("Usage: enter equation\nExample: X^2 + X - 10 = 0")
            exit()
    elif args.__len__() > 3:
        print ("Too many args")
        exit()
    s = args[1]
    if '=' in s:
        left, right = s.split('=')
        parser.parse(left)
        values_left = values
        values = [0, 0, 0]
        parser.parse(right)
        values_right = values
        c = values_left[0] - values_right[0]
        b = values_left[1] - values_right[1]
        a = values_left[2] - values_right[2]
        print("Reduced form: {} * X^2 + {} * X^1 + {} * X^0 = 0".format(a, b, c))
        print ("Free form:\n--------------------")
        print(np.poly1d([a, b, c]))
        print("--------------------")
        print ("a = {}\nb = {}\nc = {}\n".format(a, b, c))
        res = solve_equation(a, b, c)

        if graf == 1:
            x = np.linspace(-100, 100, 10)
            coeffs = [a, b, c]
            print (coeffs)
            plt.plot(x, get_polynom_values(x, coeffs))
            plt.show()
