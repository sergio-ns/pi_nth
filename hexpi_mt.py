import math
import threading
import time
import sys

TERMS = 5

class S_A (threading.Thread):
    def __init__(self, threadID, name, n, coeff):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.n = n
        self.coeff = coeff
        self.out = 0
    
    def run(self):
        self.out =  self.calc()
        
    def calc(self):
        S_A = 0
        for k in range(0,self.n+1):
            num = 16**(self.n-k) % (8*k + self.coeff)
            den = 8*k + self.coeff
            S_A += num / den

        return S_A

class S_B (S_A):
    def __init__(self, threadID, name, n, coeff):
        S_A.__init__(self, threadID, name, n, coeff)
       
    def calc(self):
        S_B = 0
        for k in range(self.n+1,self.n+TERMS+2):
            num = 16**(self.n-k)
            den = 8*k + self.coeff
            S_B += num / den

        return S_B  

    
def main_mt(n):
    
    n-=1
    threads = []
    S_A1 = S_A(1,'S_A1',n,1)
    S_B1 = S_B(1,'S_B1',n,1)
    
    S_A4 = S_A(1,'S_A4',n,4)
    S_B4 = S_B(1,'S_B4',n,4)
    
    S_A5 = S_A(1,'S_A5',n,5)
    S_B5 = S_B(1,'S_B5',n,5)
    
    S_A6 = S_A(1,'S_A5',n,6)
    S_B6 = S_B(1,'S_B5',n,6)


    S_A1.start()
    S_B1.start()
    S_A4.start()
    S_B4.start()
    S_A5.start()
    S_B5.start()
    S_A6.start()
    S_B6.start()

    threads.append(S_A1)
    threads.append(S_B1)
    threads.append(S_A4)
    threads.append(S_B4)
    threads.append(S_A5)
    threads.append(S_B5)
    threads.append(S_A6)
    threads.append(S_B6)

    # Wait for all threads to complete
    for t in threads:
      t.join()


    # get all outputs and perform final calculation
    p1 = 4 * (S_A1.out + S_B1.out) - 2 * (S_A4.out + S_B4.out) - (S_A5.out + S_B5.out) - (S_A6.out + S_B6.out) 

    p2 = p1 - math.floor(p1)

    p3 = p2 * 16

    pi_th = hex(math.floor(p3))

    print (f"The n-th digit of PI with n = {n+1} in hex is {pi_th}")


if __name__ == '__main__':
    n = int(sys.argv[1:][0])
    print(f"Calculating for n = {n}")
    time_start = time.time()
    main_mt(n)
    time_end = time.time()
    delta = time_end-time_start
    print(f"Executed in {delta} seconds")
