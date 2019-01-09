#
# BBP Formula implementation
#
import math
import time
import sys

TERMS = 5

def Sa_n (n,coeff):

    Sa = 0
    r = range(0,n+1)
    l = list(map(lambda k: (16**(n-k) % (8*k + coeff)) / (8*k + coeff) ,r))
    Sa = sum(l)

    #for k in range(0,n+1):
    #    num = 16**(n-k) % (8*k + coeff)
    #    den = 8*k + coeff
    #    Sa+= num / den

    return Sa

def Sb_n (n,coeff):
    Sb = 0
    for k in range(n+1,n+TERMS+2):
        num = 16**(n-k)
        den = (8*k + coeff)
        Sb += num / den

    return Sb

def main_st(n):

    n-=1

    p1 = 4*(Sa_n(n,1) + Sb_n(n,1) ) - 2*(Sa_n(n,4) + Sb_n(n,4)) - (Sa_n(n,5) + Sb_n(n,5)) - (Sa_n(n,6) + Sb_n(n,6))

    p2 = p1 - math.floor(p1)

    p3 = p2 * 16

    pi_th = hex(math.floor(p3))

    print (f"The n-th digit of PI with n = {n+1} in hex is {pi_th}")

if __name__ == '__main__':
    n = int(sys.argv[1:][0])
    print(f"Calculating for n = {n}")
    time_start = time.time()
    main_st(n)
    time_end = time.time()
    delta = time_end-time_start
    print(f"Executed in {delta} seconds")
