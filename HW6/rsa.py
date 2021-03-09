'''
Homework Number: 6
Name: Alex Goebel
ECN Login: goebel2
Due Date: 3/8/2021
'''

#!/usr/bin/env python3

import sys
from BitVector import *
from PrimeGenerator import PrimeGenerator


def getTotient(p, q):
    return ((p-1) * (q-1))


def CRT(C, d, p, q, n):
    
    #Compute Vp and Vq
    Vp = pow(C, d, p)
    Vq = pow(C, d, q)
    
    
    #Create temp BitVector objs for use with multiplicative_inverse()
    tempQ = BitVector(intVal = q)
    tempP = BitVector(intVal = p)
    
    #Compute the multiplicative inverse of q mod p
    tempMI = tempQ.multiplicative_inverse(tempP)
    
    #Find Xp
    Xp = q * tempMI.int_val()
    
    #Compute the multiplicative inverse of p mod q
    tempMI = tempP.multiplicative_inverse(tempQ)
    
    #Find Xq
    Xq = p * tempMI.int_val()
    
    #Compute C^d mod n using CRT
    crtAns = (Vp*Xp + Vq*Xq) % n
    
    return crtAns


def gcd(a,b):
    while(b != 0):
        temp = b
        b = a%b
        a = temp
        
    return a

if __name__ == '__main__':
    #TODO: Need to change this check to make sure it accounts for key gen or encrypt/decrypt
    if len(sys.argv) != 4 and len(sys.argv) != 6:
        print(len(sys.argv))
        sys.exit('Incorrect number of arguments, please try again')
        
    #Key generation
    if sys.argv[1] == '-g':
        
        #Define e for use in this assignment
        e = 65537
        pOutFile = open(sys.argv[2], 'w')
        qOutFile = open(sys.argv[3], 'w')
        
        #Variables to hold the random numbers generated for p and q
        p = 0
        q = 0
        
        #Hold generator variable
        generator = PrimeGenerator(bits = 128) 
        while (p == q):
            p = generator.findPrime()
            q = generator.findPrime()
            if(gcd((p-1), e) != 1):
                print(gcd((p-1), e))
                p = q
                continue
            if(gcd((q-1), e) != 1):
                p = q
                continue
        
        #Write to file
        pOutFile.write(str(p))
        qOutFile.write(str(q))
        
        #Close files
        pOutFile.close()
        qOutFile.close()
        
        
        
    #Encryption
    if sys.argv[1] == '-e':
        
        #Open needed files
        inFile = open(sys.argv[2]).read()
        
                
        pNum = int(open(sys.argv[3]).read())
        qNum = int(open(sys.argv[4]).read())
        outFile = open(sys.argv[5], 'w')
        
        
        #Set e to the correct value for this assignment
        e = 65537
        
        
        #Get n from p and q
        n = pNum * qNum
        
        #Get the totient of n
        totient = getTotient(pNum, qNum)
        
        
        #Get BitVector object from input file
        bv = BitVector(textstring = inFile)
        
        #Check if overall length is a multiple of 128. If it is not, add the appropriate amount of zeros onto the right of the string
        if(len(bv) % 128 != 0):
            temp = 128 - (len(bv) % 128)
            bv.pad_from_right(temp)


        #Because of previous padding, no need to check if the length is less than 128 because we know it will have an exact number of 128-bit blocks.
        #Just need to pad with 128 zeros to make it 256 bits
        count = 0
        while (count < bv.size):
            M = bv[count:count+128]
            M.pad_from_left(128)
            M = int(M)
            C = BitVector(intVal = ((M**e)%n), size=256)
            outFile.write(C.get_bitvector_in_hex())
            count += 128
            
            
        
        
        
        #Close files
        outFile.close()
        
        
        
    #Decryption
    if sys.argv[1] == '-d':
        
        #Open needed files
        encryptedFile = open(sys.argv[2]).read()
        
                
        pNum = int(open(sys.argv[3]).read())
        qNum = int(open(sys.argv[4]).read())
        outFile = open(sys.argv[5], 'w')

        #Set e to the correct value for this assignment
        e = 65537
        
        #Get n from p and q
        n = pNum * qNum
        
        #Get the totient of n
        totient = getTotient(pNum, qNum)
        
        
        #Compute d
        temp = BitVector(intVal = e)
        temp2 = BitVector(intVal = totient)
        d = temp.multiplicative_inverse(temp2)
        d = d.int_val()
        
        
        
        #Get BitVector object from input file
        bv = BitVector(hexstring = encryptedFile)
    

        #Get 256 bit chunks to decrypt
        count = 0
        while (count < bv.size):
            C = bv[count:count+256]
            decrypted = BitVector(intVal = CRT(C.int_val(), d, pNum, qNum, n), size=256)
            noPad = decrypted[128:]
            outFile.write(noPad.get_bitvector_in_ascii())
            count += 256
            
            
        
        
        
        #Close files
        outFile.close()