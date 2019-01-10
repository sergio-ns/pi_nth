#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""BBP Formula implementation
   It calculates the n-th digit of PI in hexadecimal base
   Ref: https://en.wikipedia.org/wiki/Bailey%E2%80%93Borwein%E2%80%93Plouffe_formula
   
   This is the multi-process implementation of the formula

   Author: Sergio N.
   Date: January 2019
   TODO: 
   - Optmize mod using exponentiation
   - Add performance over 10000 digits in the header as a reference
   - Enhance parallelization using Pool to bind processes to different CPU cores
   - Unify S_A and S_B
   
"""

import math
import multiprocessing
import time
import sys

# number of terms to be calculated in the second term of the summation which is supposed to summate over infinite
# it is a rapidly converging series and the contribution to the overall result is minimal so TERMS = 5 is a good choice
TERMS = 5

class S_A (multiprocessing.Process):
    """ Class used to implement one of the two generic terms in the formula.
        This one comes in the form:

         n
        ---    n-k
        \     16   mod (8k+coeff)
        /    ---------------------
        ---         8k + coeff
        k=0
        where coeff can be one of: 1,4,5,6
        
        Subclassed from Process in order to implement parallelization
    """
    def __init__(self, queue, name, n, coeff):
        """ Constructor of the class:
            queue : object used to deliver the final result after the calculation completes and the process is destroyed
            name  : name of the process, for diagnostic purposes
            n     : number of required digits
            coeff : coefficient used in the formula
        """
        multiprocessing.Process.__init__(self)
        self.name = name
        self.n = n
        self.coeff = coeff
        self.queue = queue
    
    def run(self):
        """
        Process method that start the execution
        """
        self.queue.put(self.calc())

        
    def calc(self):
        """ Performs the actual calculation of the term
        """
        S_A = 0
        for k in range(0,self.n+1):
            num = 16**(self.n-k) % (8*k + self.coeff)
            den = 8*k + self.coeff
            S_A += num / den

        return S_A

class S_B (S_A):
    """ Class used to implement the second one of the two generic terms in the formula.
        This one comes in the form:

         ∞
        ---                n-k
        \               16 
        /     --------------------
        ---         8k + coeff
        k=n+1
        where coeff can be one of: 1,4,5,6
        
        Subclassed from S_A as the only thing that is different is S_B
        As a matter of fact, the two classes could be combined into one 
        because the computation of S_B is orders of magnitude faster than S_A
        and there is no point in parallelizing its calculation
    """
    def __init__(self, queue, name, n, coeff):
        S_A.__init__(self, queue, name, n, coeff)
       
    def calc(self):
        """ Performs the actual calculation of the term
        """
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
