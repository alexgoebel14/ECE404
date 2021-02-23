'''
Homework Number: 4
Name: Alex Goebel
ECN Login: goebel2
Due Date: 2/23/2021
'''

#!/usr/bin/env python3

import sys
from BitVector import *

#AES irreducible polynomial
AES_modulus = BitVector(bitstring='100011011')

subBytesTable = []        # SBox for encryption
invSubBytesTable = []     # SBox for decryption


#This function was taken from the Lecture 8 code "gen_key_schedule.py" and modified to fit this assignment
def key_schedule_main(key_bv):
    key_words = []
    key_words = gen_key_schedule_256(key_bv, subBytesTable)
    key_schedule = []
    print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
        if word_index % 4 == 0: print("\n")
        print("word %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    num_rounds = 14
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
    
    return round_keys

#This function was taken from the Lecture 8 code "gen_key_schedule.py"
def gee(keyword, round_constant, subBytesTable):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = subBytesTable[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant


#This function was taken from the Lecture 8 code "gen_key_schedule.py" and modified to fit this assignment
def gen_key_schedule_256(key_bv, subBytesTable):
    #  We need 60 keywords (each keyword consists of 32 bits) in the key schedule for
    #  256 bit AES. The 256-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 14 rounds uses 4 keywords from the key
    #  schedule. We will store all 60 keywords in the following list:
    key_words = [None for i in range(60)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(8):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(8,60):
        if i%8 == 0:
            print(key_words[7])
            kwd, round_constant = gee(key_words[i-1], round_constant, subBytesTable)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 subBytesTable[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

#This function was taken from the Lecture 8 code "gen_key_schedule.py" and modified to fit this assignment
def gen_subbytes_table():
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))



#This function was taken from the Lecture 8 code "gen_tables.py" and modified to fit this assignment
def gen_decrypt_table():
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))


#Generate state array
def gen_state_array(inputBlock):
    stateArray = [[0 for x in range(4)] for x in range(4)]
    
    for i in range(4):
        for j in range(4):
            stateArray[i][j] = inputBlock[32*i + 8*j: 32*i + 8*(j+1)]
    return stateArray


#This function is for step 1, substituting the bytes of the state array with the corresponding bytes of the SBox
def subBytes(stateArray):
    for i in range(4):
        for j in range(4):
            temp1 = stateArray[i][j]
            [row, col] = temp1.divide_into_two()
            stateArray[i][j] = subBytesTable[(row*16)+col]
            
    return stateArray



#This function is for step 2, shifts the rows of the state array
def shiftRows(stateArray):
    #Row 0 doesn't get shifted
    #Row 1 shifts to the left by 1
    temp = stateArray[1][0]
    stateArray[1][0] = stateArray[1][1]
    stateArray[1][1] = stateArray[1][2]
    stateArray[1][2] = stateArray[1][3]
    stateArray[1][3] = temp
    
    #Row 2 shifts to the left by 2
    temp = stateArray[2][1]
    stateArray[2][0] = stateArray[2][2]
    stateArray[2][1] = stateArray[2][3]
    stateArray[2][2] = stateArray[2][0]
    stateArray[2][3] = temp
    
    #Row 3 shifts to the left by 3
    temp = stateArray[3][0]
    temp2 = stateArray[3][1]
    stateArray[3][0] = stateArray[3][3]
    stateArray[3][1] = temp
    stateArray[3][3] = stateArray[3][2]
    stateArray[3][2] = temp2
    
    return stateArray
    


#This function is for step 3, mix the colums
def mixColumns(stateArray):
    #Create array to place new values after column mix
    endArray = [[0 for x in range(4)] for x in range(4)]
    n = 8
    a = BitVector(hexstring = '0x01')
    b = BitVector(hexstring = '0x02')
    c = BitVector(hexstring = '0x03')
    for i in range(4):
        if i == 0:
            endArray[i][0] = (b.gf_multiply_modular(stateArray[0][0], AES_modular, n)) ^ (c.gf_multiply_modular(stateArray[1][0], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[2][0], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[3][0], AES_modular, n))
            endArray[i][1] = (b.gf_multiply_modular(stateArray[0][1], AES_modular, n)) ^ (c.gf_multiply_modular(stateArray[1][1], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[2][1], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[3][1], AES_modular, n))
            endArray[i][2] = (b.gf_multiply_modular(stateArray[0][2], AES_modular, n)) ^ (c.gf_multiply_modular(stateArray[1][2], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[2][2], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[3][2], AES_modular, n))
            endArray[i][3] = (b.gf_multiply_modular(stateArray[0][3], AES_modular, n)) ^ (c.gf_multiply_modular(stateArray[1][3], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[2][3], AES_modular, n)) ^ (a.gf_multiply_modular(stateArray[3][3], AES_modular, n))
    

if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Incorrect number of arguments, please try again')
    if sys.argv[1] == '-e':
        #Open plaintext file and put it into an array of hexadecimal.
        inFileName = sys.argv[2]
        inFile = open(inFileName)
        plainText = inFile.read()
        plainTextArray = plainText.encode("utf-8").hex()
        plainTextBV = BitVector(textstring = plainText)
        plaintextarray = BitVector(hexstring = plainTextBV.get_bitvector_in_hex())
        
        # bv = BitVector(filename = inFileName)
        # while (bv.more_to_read):
        #     bitvec = bv.read_bits_from_file(128)
        # if len(bitvec) < 128:
        #     temp = BitVector(intVal = 0, size = 128-len(bitvec))
        #     bitvec = bitvec + temp
            
        #Generate SBox for encryption
        gen_subbytes_table()
        
        
        #Get the encryption key from the text file
        encryptionKeyFile = sys.argv[3]
        encryptionKeyFile = open(encryptionKeyFile)
        encryptionKey = encryptionKeyFile.read()
        key_bv = BitVector(textstring = encryptionKey)
        
        #Generate the round keys
        round_keys = key_schedule_main(key_bv)
        
        
        #14 round of AES encryption
        for i in range(0,len(plaintextarray),128):
            inputBlock = plaintextarray[i:i+128]
            for j in range(14):
                outputBlock = subBytes(inputBlock)
                output2 = shiftRows(outputBlock)
                output3 = mixCols(output2)
                output4 = addRoundKey(output3)
            #write output4 to the outfile or add to one var to create one big var to output after all loops are done
        finalOutput += output4
        
                
        
        
        
        
        
        
        output = encrypt(inFileName, encryptionKey)
        outFile = sys.argv[4]
        outFile = open(outFile, 'w')
        outFile.write(output.get_hex_string_from_bitvector())
        outFile.close()
        encryptionKeyFile.close()
    