#!/usr/bin/env python 3

## FindMI.py
'''
Homework Number: 3
Name: Alex Goebel
ECN Login: goebel2
Due Date: 2/11/2021
'''

import sys
import math

def MI(num, mod):
    '''
    This function uses ordinary integer arithmetic implementation of the
    Extended Euclid's Algorithm to find the MI of the first-arg integer
    vis-a-vis the second-arg integer.
    '''
    NUM = num; MOD = mod
    x, x_old = 0, 1
    y, y_old = 1, 0
    while mod:
        q = bDivide(num, mod)
        num, mod = mod, num % mod
        x, x_old = bMult(x, x_old, q)
        y, y_old = bMult(y, y_old, q)
    if num != 1:
        print("\nNO MI. However, the GCD of %d and %d is %u\n" % (NUM, MOD, num))
    else:
        MI = (x_old + MOD) % MOD
        print("\nMI of %d modulo %d is: %d\n" % (NUM, MOD, MI))

def bDivide(num, mod):
    #During TA office hours this is what resulted from the conversation
    ans = 0
    while (num >= mod):
        num -= mod
        ans += 1
    return ans


def bMult(x, xOld, q):
    temp = x
    neg = 0
    #If the x value is negative, set a flag variable and use bitwise negation
    if(x < 0):
        neg = 1
        x = (~(x) + 1)
    else:
        neg = 0
    #Found of GeeksForGeeks
    product = 0
    counter = 0
    #While x has a value, continue to perform multiplicaiton. If there is a remainder, then carry out a left shift
    while(x):
        if(x % 2 == 1):
            product += q << counter
        
        counter += 1
        x = bDivide(x,2)
        
    #If the x value was negative, multiply the final product by -1, otherwise don't touch it
    if(neg == 1):
        x = xOld - (product * -1)
    else:
        x = xOld - product
    xOld = temp
    return x, xOld
    
if __name__ == '__main__':
    if len(sys.argv) != 3:  
        sys.stderr.write("Usage: %s   <integer>   <modulus>\n" % sys.argv[0]) 
        sys.exit(1) 
        
    NUM, MOD = int(sys.argv[1]), int(sys.argv[2])
    MI(NUM, MOD)




