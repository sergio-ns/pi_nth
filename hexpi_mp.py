import math
import multiprocessing
import time
import sys

TERMS = 5

class S_A (multiprocessing.Process):
    def __init__(self, queue, name, n, coeff):
        multiprocessing.Process.__init__(self)
        self.name = name
        self.n = n
        self.coeff = coeff
        self.queue = queue
    
    def run(self):
        self.queue.put(self.calc())

        
    def calc(self):
        S_A = 0
        for k in range(0,self.n+1):
            num = 16**(self.n-k) % (8*k + self.coeff)
            den = 8*k + self.coeff
            S_A += num / den

        return S_A

class S_B (S_A):
    def __init__(self, queue, name, n, coeff):
        S_A.__init__(self, queue, name, n, coeff)
       
    def calc(self):
        S_B = 0
        for k in range(self.n+1,self.n+TERMS+2):
            num = 16**(self.n-k)
            den = 8*k + self.coeff
            S_B += num / den

        return S_B  

    
def main_mp(n):
    
    n-=1
    jobs = []
    q_A1 = multiprocessing.Queue()
    S_A1 = S_A(q_A1,'S_A1',n,1)

    q_B1 = multiprocessing.Queue()
    S_B1 = S_B(q_B1,'S_B1',n,1)
    
    q_A4 = multiprocessing.Queue()
    S_A4 = S_A(q_A4,'S_A4',n,4)

    q_B4 = multiprocessing.Queue()
    S_B4 = S_B(q_B4,'S_B4',n,4)
    
    q_A5 = multiprocessing.Queue()
    S_A5 = S_A(q_A5,'S_A5',n,5)

    q_B5 = multiprocessing.Queue()
    S_B5 = S_B(q_B5,'S_B5',n,5)
    
    q_A6 = multiprocessing.Queue()
    S_A6 = S_A(q_A6,'S_A6',n,6)

    q_B6 = multiprocessing.Queue()
    S_B6 = S_B(q_B6,'S_B6',n,6)

    jobs.append(S_A1)
    S_A1.start()

    jobs.append(S_B1)
    S_B1.start()

    jobs.append(S_A4)
    S_A4.start()

    jobs.append(S_B4)
    S_B4.start()
    
    jobs.append(S_A5)
    S_A5.start()
    
    jobs.append(S_B5)
    S_B5.start()
    
    jobs.append(S_A6)
    S_A6.start()
    
    jobs.append(S_B6)
    S_B6.start()

    # Wait for all threads to complete
    for j in jobs:
      j.join()

    # get all outputs and perform final calculation
    p1 = 4 * (q_A1.get() + q_B1.get()) - 2 * (q_A4.get() + q_B4.get()) - (q_A5.get() + q_B5.get()) - (q_A6.get() + q_B6.get()) 

    p2 = p1 - math.floor(p1)

    p3 = p2 * 16

    pi_th = hex(math.floor(p3))

    print (f"The n-th digit of PI with n = {n+1} in hex is {pi_th}")


if __name__ == '__main__':
    n = int(sys.argv[1:][0])
    print(f"Calculating for n = {n}")
    time_start = time.time()
    main_mp(n)
    time_end = time.time()
    delta = time_end-time_start
    print(f"Executed in {delta} seconds")
