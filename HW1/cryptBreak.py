'''
Homework Number: 1
Name: Alex Goebel
ECN Login: goebel2
Due Date: 1/28/2021
'''

#!/usr/bin/env python3
import sys #Do I need this or was this only for the example? Do the arguments need to be checked?
from BitVector import *


def cryptBreak(ciphertextFile, key_bv):
    PassPhrase = "Hopes and dreams of a million years"
    BLOCKSIZE = 16
    numbytes = BLOCKSIZE // 8
    
    
    bv_iv = BitVector(bitlist = [0]*BLOCKSIZE)
    for i in range(0, len(PassPhrase) // numbytes):
        textstr = PassPhrase[i*numbytes:(i+1)*numbytes]
        bv_iv ^= BitVector(textstring = textstr)
    
    inFile = open(ciphertextFile)
    encrypted_bv = BitVector(hexstring = inFile.read())
    
    decryptedMessage_bv = BitVector(size = 0)
    
    previousDecryptedBlock = bv_iv
    
    for i in range(0, len(encrypted_bv) // BLOCKSIZE):
        bv = encrypted_bv[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
        temp = bv.deep_copy()
        bv ^= previousDecryptedBlock
        previousDecryptedBlock = temp
        bv ^= key_bv
        decryptedMessage_bv += bv
        
    
    outputText = decryptedMessage_bv.get_text_from_bitvector()
    
    
    inFile.close()
    return outputText
    
    


if __name__ == '__main__':
    
        
    ciphertextFile = 'encrypted.txt'
        
    keyRangeMax = 2 ** 16

    for i in range(20000, keyRangeMax):
        key_bv = BitVector(intVal = i, size=16)
        decryptedMessage = cryptBreak(ciphertextFile, key_bv)
        if 'Yogi Berra' not in decryptedMessage:
            print('Not decrypted yet')
            print(key_bv)
        else:
            print('Encryption broken!')
            print(key_bv)
            print(decryptedMessage)
            break
            
        
        
    
