"""BBP Formula implementation
   It calculates the n-th digit of PI in hexadecimal base
   Ref: https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
   
   This is the multi-process implementation of the formula

   Author: Sergio N.
   Date: January 2019
   TODO: 
   - Enhance parallelization using Pool to bind processes to different CPU cores

   Performance:
   1000     ~  145ms
   5000     ~  150ms
   10000    ~  154ms
   20000    ~  168ms
   50000    ~  215ms
   100000   ~  305ms
   200000   ~  500ms
   500000   ~ 1090ms
   1000000  ~ 2012ms
   
"""

import math
import multiprocessing
import time
import sys

# number of terms to be calculated in the second term of the summation which is supposed to summate over infinite
# it is a rapidly converging series and the contribution to the overall result is minimal so TERMS = 5 is a good choice
TERMS = 5

class S (multiprocessing.Process):
    """ Class used to calculate each term in the main sum of the formula,
        which can be expressed as:

         n
        ---     n-k
        \     16   mod (8k+coeff)
        /    ---------------------        +
        ---         8k + alpha
        k=0

         ∞
        ---              n-k
        \              16 
        /     --------------------
        ---         8k + alpha
        k=n+1

        where alpha can be one of: 1,4,5,6
        
        Subclassed from Process in order to implement parallelization
    """
    def __init__(self, queue, name, n, alpha):
        """ Constructor of the class:
            queue : object used to deliver the final result after the calculation completes and the process is destroyed
            name  : name of the process, for diagnostic purposes
            n     : number of required digits
            alpha : coefficient used in the formula
        """
        multiprocessing.Process.__init__(self)
        self.name = name
        self.n = n
        self.alpha = alpha
        self.queue = queue
    
    def run(self):
        """
        Process method that start the execution
        """
        self.queue.put(self.calc())

        
    def calc(self):
        """ Performs the actual calculation of the term
        """
        S_res = 0
        for k in range(0,self.n+1):
            # Modulus using exponentiation
            num = pow(16,self.n-k,8*k + self.alpha)
            den = 8*k + self.alpha
            S_res += num / den

        for k in range(self.n+1,self.n+TERMS+2):
            num = 16**(self.n-k)
            den = 8*k + self.alpha
            S_res += num / den

        return S_res


    
def main_mp(n):
    
    n-=1
    jobs = []
    q_1 = multiprocessing.Queue()
    S_1 = S(q_1,'S_1',n,1)

    q_4 = multiprocessing.Queue()
    S_4 = S(q_4,'S_4',n,4)
    
    q_5 = multiprocessing.Queue()
    S_5 = S(q_5,'S_5',n,5)

    q_6 = multiprocessing.Queue()
    S_6 = S(q_6,'S_6',n,6)


    jobs.append(S_1)
    S_1.start()

    jobs.append(S_4)
    S_4.start()

    jobs.append(S_5)
    S_5.start()
    
    jobs.append(S_6)
    S_6.start()
    

    # Wait for all threads to complete
    for j in jobs:
      j.join()

    # get all outputs and perform final calculation
    p1 = 4 * q_1.get()  - 2 * q_4.get()  - q_5.get() - q_6.get()

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
