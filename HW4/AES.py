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
    #print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
        #if word_index % 4 == 0: print("\n")
        #print("word %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    num_rounds = 14
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])
    
    
    return round_keys, key_words

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
            kwd, round_constant = gee(key_words[i-1], round_constant, subBytesTable)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = subBytesTable[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
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
    stateArray = [[0 for x in range(4)] for y in range(4)]
    
    for i in range(4):
        for j in range(4):
            stateArray[i][j] = inputBlock[32*i + 8*j: 32*i + 8*(j+1)] #Help from lecture 8
    return stateArray


#This function is for encrypt step 1, substituting the bytes of the state array with the corresponding bytes of the SBox. TA Helped with this
def subBytes(stateArray):
    for i in range(4):
        for j in range(4):
            stateArray[i][j] = BitVector(intVal=subBytesTable[int(stateArray[i][j])], size = 8)

    return stateArray

#This function is for decrypt step 2, substituting the bytes of the state array with the corresponding bytes of the SBox. TA Helped with this
def invSubBytes(stateArray):
    for i in range(4):
        for j in range(4):
            stateArray[i][j] = BitVector(intVal=invSubBytesTable[int(stateArray[i][j])], size = 8)

    return stateArray



#This function is for encrypt step 2, shifts the rows of the state array
def shiftRows(stateArray):
    
    #Transpose the stateArray. Found this method on stackoverflow 
    transposed = [list(x) for x in zip(*stateArray)]
    #Row 0 doesn't get shifted
    #Row 1 shifts to the left by 1
    temp = transposed[1][0]
    transposed[1][0] = transposed[1][1]
    transposed[1][1] = transposed[1][2]
    transposed[1][2] = transposed[1][3]
    transposed[1][3] = temp
    
    #Row 2 shifts to the left by 2
    temp = transposed[2][0]
    temp1 = transposed[2][1]
    transposed[2][0] = transposed[2][2]
    transposed[2][1] = transposed[2][3]
    transposed[2][2] = temp
    transposed[2][3] = temp1
    
    #Row 3 shifts to the left by 3
    temp = transposed[3][0]
    temp2 = transposed[3][1]
    transposed[3][0] = transposed[3][3]
    transposed[3][1] = temp
    transposed[3][3] = transposed[3][2]
    transposed[3][2] = temp2
       
    #Untransposed using the same method as before, again found on stackoverflow
    untransposed = [list(x) for x in zip(*transposed)]
    return untransposed
    

#This function is for decrypt step 1, shifts the rows of the state array
def invShiftRows(stateArray):
    
    #Transpose the stateArray. Found this method on stackoverflow 
    transposed = [list(x) for x in zip(*stateArray)]
    #Row 0 doesn't get shifted
    #Row 1 shifts to the right by 1
    temp = transposed[1][0]
    temp2 = transposed[1][1]
    transposed[1][0] = transposed[1][3]
    transposed[1][1] = temp
    transposed[1][3] = transposed[1][2]
    transposed[1][2] = temp2
    
    #Row 2 shifts to the right by 2
    temp = transposed[2][0]
    temp1 = transposed[2][1]
    transposed[2][0] = transposed[2][2]
    transposed[2][1] = transposed[2][3]
    transposed[2][2] = temp
    transposed[2][3] = temp1
    
    #Row 3 shifts to the right by 3
    temp = transposed[3][0]
    transposed[3][0] = transposed[3][1]
    transposed[3][1] = transposed[3][2]
    transposed[3][2] = transposed[3][3]
    transposed[3][3] = temp
       
    #Untransposed using the same method as before, again found on stackoverflow
    untransposed = [list(x) for x in zip(*transposed)]
    return untransposed

#This function is for encrypt step 3, mix the columns
def mixColumns(stateArray):
    #Create array to place new values after column mix
    endArray = [[0 for x in range(4)] for x in range(4)]
    n = 8
    a = BitVector(hexstring = '01')
    b = BitVector(hexstring = '02')
    c = BitVector(hexstring = '03')
    
    #Transpose the stateArray. Found this method on stackoverflow 
    transposed = [list(x) for x in zip(*stateArray)]
    
    for i in range(4):
        if i == 0:
            endArray[i][0] = (b.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (b.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (b.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (b.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if i == 1:
            endArray[i][0] = (a.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (a.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (a.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (a.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if i == 2:
            endArray[i][0] = (a.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (a.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (a.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (a.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if i == 3:
            endArray[i][0] = (c.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (c.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (c.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (c.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][3], AES_modulus, n))

    #Untransposed using the same method as before, again found on stackoverflow
    untransposed = [list(x) for x in zip(*endArray)]
    return untransposed

#Function for decrypt step 4, mixing the columns
def invMixColumns(stateArray):
    #Create array to place new values after column mix
    endArray = [[0 for x in range(4)] for x in range(4)]
    n = 8
    a = BitVector(hexstring = '0E')
    b = BitVector(hexstring = '0B')
    c = BitVector(hexstring = '0D')
    d = BitVector(hexstring = '09')
    
    #Transpose the stateArray. Found this method on stackoverflow 
    transposed = [list(x) for x in zip(*stateArray)]
    
    for i in range(4):
        if i == 0:
            endArray[i][0] = (a.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (a.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (a.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (a.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if i == 1:
            endArray[i][0] = (d.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (d.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (d.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (d.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if i == 2:
            endArray[i][0] = (c.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (c.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (c.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (c.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if i == 3:
            endArray[i][0] = (b.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            endArray[i][1] = (b.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            endArray[i][2] = (b.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            endArray[i][3] = (b.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (d.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][3], AES_modulus, n))

    #Untransposed using the same method as before, again found on stackoverflow
    untransposed = [list(x) for x in zip(*endArray)]
    return untransposed

    
#Function for adding the round key to the output of the previous step
def addRoundKey(roundKey, state_array):
    tempVar = BitVector(size=0)
    for x in range(4):
        for y in range(4):
            tempVar += state_array[x][y]
            
    tempVar ^= roundKey

       
    return tempVar
    
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Incorrect number of arguments, please try again')
    if sys.argv[1] == '-e':
        #Open plaintext file
        inFileName = sys.argv[2]
        
        #Open the output file
        outFile = sys.argv[4]
        outFile = open(outFile, 'w')
        
        #Get the encryption key from the text file
        encryptionKeyFile = sys.argv[3]
        encryptionKeyFile = open(encryptionKeyFile)
        encryptionKey = encryptionKeyFile.read()
        key_bv = BitVector(textstring = encryptionKey)
        
        
        #Generate SBox for encryption
        gen_subbytes_table()
        
        
        #Generate the round keys
        round_keys, key_words = key_schedule_main(key_bv)

        #Variable to keep track of what round of AES it's on
        numRound = 0
        #Get BitVector object from input file
        bv = BitVector(filename = inFileName)
        while (bv.more_to_read):
            bitvec = bv.read_bits_from_file(128)
            if len(bitvec) < 128:
                temp = BitVector(intVal = 0, size = 128-len(bitvec))
                bitvec = bitvec + temp
   
    
            #Generate state array
            state_array = gen_state_array(bitvec)
            
            #Pre encrypt task of XOR
            state_array = addRoundKey(round_keys[0], state_array)
            
            #Get state_array back to an actual state_array
            state_array = gen_state_array(state_array)
            
            
            #14 rounds of AES encryption
            for j in range(14):
                outputBlock = subBytes(state_array)
                output2 = shiftRows(outputBlock)
                if j != 13:
                    output3 = mixColumns(output2)
                    output4 = addRoundKey(round_keys[j+1], output3)
                else:
                    output4 = addRoundKey(round_keys[j+1], output2)

                state_array = gen_state_array(output4)

            #write output4 to the outfile or add to one var to create one big var to output after all loops are done
            for u in range(4):
                for v in range(4):
                    outFile.write(state_array[u][v].get_bitvector_in_hex())

            
        
                
        
        outFile.close()
        encryptionKeyFile.close()
        
        
    #Decrypt
    if sys.argv[1] == '-d':
        #Open plaintext file
        inFileName = sys.argv[2]
        inFile = open(inFileName)
        inFileHex = inFile.read()
        
        #Open the output file
        outFile = sys.argv[4]
        outFile = open(outFile, 'w')
        
        #Get the encryption key from the text file
        encryptionKeyFile = sys.argv[3]
        encryptionKeyFile = open(encryptionKeyFile)
        encryptionKey = encryptionKeyFile.read()
        key_bv = BitVector(textstring = encryptionKey)
        
        
        #Generate SBox for encryption
        gen_subbytes_table()
        
        
        #Generate SBox for decryption
        gen_decrypt_table()
        
        
        #Generate the round keys
        round_keys, key_words = key_schedule_main(key_bv)

        #Variable to keep track of what round of AES it's on
        numRound = 0
        #Get BitVector object from input file
        bv = BitVector(hexstring = inFileHex)
        count=0
        while (count < bv.size):
            bitvec = bv[count:count+128]
            if len(bitvec) < 128:
                temp = BitVector(intVal = 0, size = 128-len(bitvec))
                bitvec = bitvec + temp
                    
                    
            #Generate state array
            state_array = gen_state_array(bitvec)
                    
            #Pre decrypt task of XOR
            state_array = addRoundKey(round_keys[14], state_array)
            
            #Get state_array back to an actual state_array
            state_array = gen_state_array(state_array)
                    
                    
            #14 rounds of AES decryption
            for j in range(0,1):
                outputBlock = invShiftRows(state_array)
                output2 = invSubBytes(outputBlock)
                output3 = addRoundKey(round_keys[13-j], output2)
                state_array = gen_state_array(output3)
                if j != 13:
                    output4 = invMixColumns(state_array)
                    tempVar = BitVector(size=0)
                    for x in range(4):
                        for y in range(4):
                            tempVar += output4[x][y]
                    print(tempVar.get_bitvector_in_hex())
                else:
                    output4 = addRoundKey(round_keys[j+1], output2)
                                
                state_array = gen_state_array(output4)
                                
                #write output4 to the outfile or add to one var to create one big var to output after all loops are done
                for u in range(4):
                    for v in range(4):
                        outFile.write(state_array[u][v].get_bitvector_in_hex())
                count+= 128                        
                                        
                
        
        outFile.close()
        encryptionKeyFile.close()
    
    