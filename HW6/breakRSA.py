'''
Homework Number: 6
Name: Alex Goebel
ECN Login: goebel2
Due Date: 3/9/2021
'''

#!/usr/bin/env python3

import sys
from BitVector import *
from solve_pRoot_BST import solve_pRoot
from PrimeGenerator import PrimeGenerator




def gcd(a,b):
    while(b != 0):
        temp = b
        b = a%b
        a = temp
        
    return a

if __name__ == '__main__':
    #TODO: Need to change this check to make sure it accounts for key gen or encrypt/decrypt
    if len(sys.argv) != 7:
        print(len(sys.argv))
        sys.exit('Incorrect number of arguments, please try again')
        
    
        
        
        
    #Encryption
    if sys.argv[1] == '-e':
        
        #Open needed files
        inFile = open(sys.argv[2]).read()
        enc1File = open(sys.argv[3], 'w')
        enc2File = open(sys.argv[4], 'w')
        enc3File = open(sys.argv[5], 'w')
        nValsFile = open(sys.argv[6], 'w')
        
        #Set e to the correct value for this assignment
        e = 3
        
        nVals = []
        #Compute 3 new n values
        count = 0
        while(count < 3):
            #Variables to hold the random numbers generated for p and q
            pNum = 0
            qNum = 0
            
            #Hold generator variable
            generator = PrimeGenerator(bits = 128) 
            while (pNum == qNum):
                pNum = generator.findPrime()
                qNum = generator.findPrime()
                if(gcd((pNum-1), e) != 1):
                    pNum = qNum
                    continue
                if(gcd((qNum-1), e) != 1):
                    pNum = qNum
                    continue 

            
            #Get n from p and q
            nVals.append(pNum * qNum)
            count += 1
            
        for n in nVals:
            nValsFile.write(str(n) + '\n')

        
        
        #Encrypt message once for each of the 3 keys
        for i in range(0, 3):
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
                C = BitVector(intVal = ((M**e)%nVals[i]), size=256)
                if i == 0:   
                    enc1File.write(C.get_bitvector_in_hex())
                elif i == 1:
                    enc2File.write(C.get_bitvector_in_hex())
                else:
                    enc3File.write(C.get_bitvector_in_hex())
                count += 128
                
                
            
            
            
        #Close files
        enc1File.close()
        enc2File.close()
        enc3File.close()
        nValsFile.close()
        
        
        
    #Cracking encryption
    if sys.argv[1] == '-c':
        
        #Open needed files
        enc1 = open(sys.argv[2]).read()
        enc2 = open(sys.argv[3]).read()
        enc3 = open(sys.argv[4]).read()
        C1 = BitVector(hexstring = enc1)
        C2 = BitVector(hexstring = enc2)
        C3 = BitVector(hexstring = enc3)
        nValsFile = open(sys.argv[5]).read()
        crackedOutputFile = open(sys.argv[6], 'w')
        
        

        #Set e to the correct value for this assignment
        e = 3
        
        #Get n vals from file
        nVals = []
        for n in nValsFile.splitlines():
            nVals.append(int(n))
            
            
            
        #Get M value
        M = 1
        for n in nVals:
            M *= n
        
        #Get M_i values
        M1 = nVals[1] * nVals[2]
        M2 = nVals[0] * nVals[2]
        M3 = nVals[0] * nVals[1]
        
        #Get x_i values
        temp = BitVector(intVal = M1)
        temp2 = BitVector(intVal = nVals[0])
        x1 = temp.multiplicative_inverse(temp2).int_val() * M1
        
        temp = BitVector(intVal = M2)
        temp2 = BitVector(intVal = nVals[1])
        x2 = temp.multiplicative_inverse(temp2).int_val() * M2
        
        temp = BitVector(intVal = M3)
        temp2 = BitVector(intVal = nVals[2])
        x3 = temp.multiplicative_inverse(temp2).int_val() * M3
        
    

        #Get 256 bit chunks to decrypt
        count = 0
        while (count < C1.size):
            a1 = C1[count:count+256]
            a2 = C2[count:count+256]
            a3 = C3[count:count+256]
            
            MCubed = ((a1.int_val() * x1) + (a2.int_val() * x2) + (a3.int_val() * x3)) % M
            cubeRoot = solve_pRoot(3, MCubed)
            decrypted = BitVector(intVal = cubeRoot, size=256)
            noPad = decrypted[128:]
            crackedOutputFile.write(noPad.get_bitvector_in_ascii())
            count += 256
            
            
        
        
        
        #Close files
        crackedOutputFile.close()
