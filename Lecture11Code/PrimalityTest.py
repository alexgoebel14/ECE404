#!/usr/bin/env python

##  PrimalityTest.py
##  Author: Avi Kak
##  Date:   February 18, 2011
##  Updated:  February 28, 2016
##  An implementation of the Miller-Rabin primality test

### You can call this script with either no comamnd-line args or with just one
### command-line arg.  If you call it with no args, it returns primality results on a
### set of randomly altered 36 primes.  On the other hand, if you call it with just
### one arg, it returns the answer for that integer.

def test_integer_for_prime(p):                                               #(A1)
    if p == 1: return 0                                                      #(A2)
    probes = [2,3,5,7,11,13,17]                                              #(A3)
    if p in probes: return 1                                                 #(A4)
    if any([p % a == 0 for a in probes]): return 0                           #(A5)
    k, q = 0, p-1        # need to represent p-1 as  q * 2^k                 #(A6)
    while not q&1:                                                           #(A7)
        q >>= 1                                                              #(A8)
        k += 1                                                               #(A9)
    for a in probes:                                                         #(A10)
        a_raised_to_q = pow(a, q, p)                                         #(A11)
        if a_raised_to_q == 1: continue                                      #(A12)
        if (a_raised_to_q == p-1) and (k > 0): continue                      #(A13)
        a_raised_to_jq = a_raised_to_q                                       #(A14)
        primeflag = 0                                                        #(A15)
        for j in range(k-1):                                                 #(A16)
            a_raised_to_jq = pow(a_raised_to_jq, 2, p)                       #(A17)
            if a_raised_to_jq == p-1:                                        #(A18)
                primeflag = 1                                                #(A19)
                break                                                        #(A20)
        if not primeflag: return 0                                           #(A21)
    probability_of_prime = 1 - 1.0/(4 ** len(probes))                        #(A22)
    return probability_of_prime                                              #(A23)

primes = [179, 233, 283, 353, 419, 467, 547, 607, 661, 739, 811, 877, \
          947, 1019, 1087, 1153, 1229, 1297, 1381, 1453, 1523, 1597, \
          1663, 1741, 1823, 1901, 7001, 7109, 7211, 7307, 7417, 7507, \
          7573, 7649, 7727, 7841]                                            #(A24)

if __name__ == '__main__':

    import sys                                                               #(M1)
    import random                                                            #(M2)

    if len(sys.argv) == 1:                                                   #(M3)
        for p in primes:                                                     #(M4)
            p += random.randint(1,10)                                        #(M5)
            probability_of_prime = test_integer_for_prime(p)                 #(M6)
            if probability_of_prime > 0:                                     #(M7)
                print("%d is prime with probability: %f" %(p,probability_of_prime))
                                                                             #(M8)
            else:                                                            #(M9)
                print("%d is composite" % p)                                 #(M10)
    elif len(sys.argv) == 2:                                                 #(M11)
        p = int(sys.argv[1])                                                 #(M12)
        probability_of_prime = test_integer_for_prime(p)                     #(M13)             
        if probability_of_prime > 0:                                         #(M14)
            print("%d is prime with probability: %f" %(p,probability_of_prime))
                                                                             #(M15)
        else:                                                                #(M16)
            print("%d is composite" % p)                                     #(M17)
    else:                                                                    #(M18)
        sys.exit("""You cannot call 'PrimalityTest.py' with more """         #(M19)
                 """than one command-line argument""")
