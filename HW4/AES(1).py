#!/usr/bin/env python 3.8

import sys
from BitVector import*

AES_modulus = BitVector(bitstring='100011011')

a = BitVector(hexstring = '01')
b = BitVector(hexstring = '02')
c = BitVector(hexstring = '03')

#gen_tables.py
subBytesTable = []
invSubBytesTable = []

def encrypt(file_in_name, keytxt):
    #basically DES encrypt function goes here
    key, keysize = get_encryption_key(keytxt)  #key is already a bv from get_encryption_key
    #key_bv = BitVector(textstring = key)
    gen_subbytes_table()
    round_keys, key_words, numRounds = start(key, keysize)
    #print("round: ",round_keys,"\n\n")

    roundCount = 0

    bv = BitVector( filename = file_in_name)
    while(bv.more_to_read):
        bitvec = bv.read_bits_from_file(128)
        if len(bitvec) < 128:
            hold = BitVector(intVal = 0, size = 128-let(bitvec))
            bitvec = bitvec + hold

        #print(type(round_keys))

        state_array = gen_state_array(bitvec)
        #print(type(state_array))
        state_array = xorRoundKey(round_keys[0], state_array) ##round_key[0]

        state_array = gen_state_array(state_array)
        print(state_array[3][3])
        #if( roundCount == 0):
        #    state_array = xorKey(round_keys, state_array)
        #    roundCount += 1
        
        for x in range(numRounds):
            out1 = subBytes(state_array)
            out2 = shiftRows(out1)
            if x != (numRounds - 1):
                out3 = mixCols(out2)
            out4 = xorRoundKey(round_keys[x+1], out3)
            state_array = gen_state_array(out4)

    return out4



def start(key_bv, keysize):
    key_words = []
    #keysize, key_bv = get_key(keytxt) ## should change
    if keysize == 128:    
        key_words = gen_key_schedule_128(key_bv)
    elif keysize == 192:    
        key_words = gen_key_schedule_192(key_bv)
    elif keysize == 256:    
        key_words = gen_key_schedule_256(key_bv)
    else:
        sys.exit("wrong keysize --- aborting")
    key_schedule = []
    #print("\nEach 32-bit word of the key schedule is shown as a sequence of 4 one-byte integers:")
    for word_index,word in enumerate(key_words):
        keyword_in_ints = []
        for i in range(4):
            keyword_in_ints.append(word[i*8:i*8+8].intValue())
    #    if word_index % 4 == 0: print("\n")
    #    print("word %d:  %s" % (word_index, str(keyword_in_ints)))
        key_schedule.append(keyword_in_ints)
    num_rounds = None
    if keysize == 128: num_rounds = 10
    if keysize == 192: num_rounds = 12
    if keysize == 256: num_rounds = 14
    print("num_rounds: " , num_rounds)
    round_keys = [None for i in range(num_rounds+1)]
    for i in range(num_rounds+1):
        round_keys[i] = (key_words[i*4] + key_words[i*4+1] + key_words[i*4+2] + key_words[i*4+3])    
    #print("\n\nRound keys in hex (first key for input block):\n")
    #for round_key in round_keys:
    #    print(round_key)
    
    return(round_keys,key_words,num_rounds)

#Generate state array
def gen_state_array(bitvec):
    stateArray = [[0 for x in range(4)] for y in range(4)]

    for i in range(4):
        for j in range(4):
            stateArray[i][j] = bitvec[32*i + 8*j: 32*i + 8*(j+1)]  #page 5 of lecture 8
    return stateArray

def subBytes(stateArray):
    for x in range(4):
        for y in range(4):
            stateArray[x][y] = BitVector(intVal=subBytesTable[int(stateArray[x][y])], size=8)
        
    return stateArray

#copied and altered from generate_round_kkeys.py
def get_encryption_key(keytxt):
    key = ""
    FILEIN = open(keytxt)
    #gathered from gen_encryption_key.py will change to work with my script
    key = FILEIN.read()

    #if len(key) != 8:
    #    print("\nKey generation needs 8 characters exactly.  Try again.\n")

    key = BitVector(textstring = key)
    keysize = len(key)          ##might consider changing to just /8 instead of floor divide
    print("keysize: ",keysize, key) ## check
    FILEIN.close
    return key, keysize

def shiftRows(stateArray):
    trans = [list(x) for x in zip(*stateArray)]
    for n in range(4):
        trans[n] = trans[n][n:] + trans[n][:n]
    fixTrans = [list(x) for x in zip(*trans)] ## is rows trans if so remove
    print(trans)
    return fixTrans

def mixCols(stateArray):
    finalArray =[[0 for x in range(4)] for y in range(4)]
    n = 8

    transposed = [list(x) for x in zip(*stateArray)]

    for x in range(4):
        if x == 0:
            for j in range(4):
                finalArray[x][j] = (b.gf_multiply_modular(transposed[0][j], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][j], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][j], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][j], AES_modulus, n))
            #finalArray[i][0] = (b.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            #finalArray[i][1] = (b.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            #finalArray[i][2] = (b.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            #finalArray[i][3] = (b.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][3], AES_modulus, n)
        if x == 1:
            for i in range(4):
                finalArray[x][i] = (a.gf_multiply_modular(transposed[0][i], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][i], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][i], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][i], AES_modulus, n))
            #finalArray[i][0] = (a.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            #finalArray[i][1] = (a.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            #finalArray[i][2] = (a.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            #finalArray[i][3] = (a.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if x == 2:
            for t in range(4):
                finalArray[x][t] = (a.gf_multiply_modular(transposed[0][t], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][t], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][t], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][t], AES_modulus, n))
            #finalArray[i][0] = (a.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            #finalArray[i][1] = (a.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            #finalArray[i][2] = (a.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            #finalArray[i][3] = (a.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (c.gf_multiply_modular(transposed[3][3], AES_modulus, n))
        if x == 3:
            for c in range(4):
                finalArray[i][c] = (c.gf_multiply_modular(transposed[0][c], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][c], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][c], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][c], AES_modulus, n))
            #finalArray[i][0] = (c.gf_multiply_modular(transposed[0][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][0], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][0], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][0], AES_modulus, n))
            #finalArray[i][1] = (c.gf_multiply_modular(transposed[0][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][1], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][1], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][1], AES_modulus, n))
            #finalArray[i][2] = (c.gf_multiply_modular(transposed[0][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][2], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][2], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][2], AES_modulus, n))
            #finalArray[i][3] = (c.gf_multiply_modular(transposed[0][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[1][3], AES_modulus, n)) ^ (a.gf_multiply_modular(transposed[2][3], AES_modulus, n)) ^ (b.gf_multiply_modular(transposed[3][3], AES_modulus, n))
    revert = [list(y) for y in zip(*endArray)]
    return revert



def gee(keyword, round_constant, byte_sub_table):
    '''
    This is the g() function you see in Figure 4 of Lecture 8.
    '''
    rotated_word = keyword.deep_copy()
    rotated_word << 8
    newword = BitVector(size = 0)
    for i in range(4):
        newword += BitVector(intVal = byte_sub_table[rotated_word[8*i:8*i+8].intValue()], size = 8)
    newword[:8] ^= round_constant
    round_constant = round_constant.gf_multiply_modular(BitVector(intVal = 0x02), AES_modulus, 8)
    return newword, round_constant

def gen_key_schedule_128(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 44 keywords in the key schedule for 128 bit AES.  Each keyword is 32-bits
    #  wide. The 128-bit AES uses the first four keywords to xor the input block with.
    #  Subsequently, each of the 10 rounds uses 4 keywords from the key schedule. We will
    #  store all 44 keywords in the following list:
    key_words = [None for i in range(44)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(4):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(4,44):
        if i%4 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-4] ^ kwd
        else:
            key_words[i] = key_words[i-4] ^ key_words[i-1]
    return key_words

def gen_key_schedule_192(key_bv):
    byte_sub_table = gen_subbytes_table()
    #  We need 52 keywords (each keyword consists of 32 bits) in the key schedule for
    #  192 bit AES.  The 192-bit AES uses the first four keywords to xor the input
    #  block with.  Subsequently, each of the 12 rounds uses 4 keywords from the key
    #  schedule. We will store all 52 keywords in the following list:
    key_words = [None for i in range(52)]
    round_constant = BitVector(intVal = 0x01, size=8)
    for i in range(6):
        key_words[i] = key_bv[i*32 : i*32 + 32]
    for i in range(6,52):
        if i%6 == 0:
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-6] ^ kwd
        else:
            key_words[i] = key_words[i-6] ^ key_words[i-1]
    return key_words

def gen_key_schedule_256(key_bv):
    byte_sub_table = gen_subbytes_table()
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
            kwd, round_constant = gee(key_words[i-1], round_constant, byte_sub_table)
            key_words[i] = key_words[i-8] ^ kwd
        elif (i - (i//8)*8) < 4:
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        elif (i - (i//8)*8) == 4:
            key_words[i] = BitVector(size = 0)
            for j in range(4):
                key_words[i] += BitVector(intVal = 
                                 byte_sub_table[key_words[i-1][8*j:8*j+8].intValue()], size = 8)
            key_words[i] ^= key_words[i-8] 
        elif ((i - (i//8)*8) > 4) and ((i - (i//8)*8) < 8):
            key_words[i] = key_words[i-8] ^ key_words[i-1]
        else:
            sys.exit("error in key scheduling algo for i = %d" % i)
    return key_words

#generate s box for sub bytes 
def gen_subbytes_table():
    subBytesTable = []
    c = BitVector(bitstring='01100011')
    for i in range(0, 256):
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
    return subBytesTable

def genTables():        #decrypt function
    c = BitVector(bitstring='01100011')
    d = BitVector(bitstring='00000101')
    for i in range(0, 256):
        # For the encryption SBox
        a = BitVector(intVal = i, size=8).gf_MI(AES_modulus, 8) if i != 0 else BitVector(intVal=0)
        # For bit scrambling for the encryption SBox entries:
        a1,a2,a3,a4 = [a.deep_copy() for x in range(4)]
        a ^= (a1 >> 4) ^ (a2 >> 5) ^ (a3 >> 6) ^ (a4 >> 7) ^ c
        subBytesTable.append(int(a))
        # For the decryption Sbox:
        b = BitVector(intVal = i, size=8)
        # For bit scrambling for the decryption SBox entries:
        b1,b2,b3 = [b.deep_copy() for x in range(3)]
        b = (b1 >> 2) ^ (b2 >> 5) ^ (b3 >> 7) ^ d
        check = b.gf_MI(AES_modulus, 8)
        b = check if isinstance(check, BitVector) else 0
        invSubBytesTable.append(int(b))

#def xorKey(round_keys, state_array):
#    for x in range(4):
#        for y in range(4):
#            state_array[x][y] ^= key_words[x][8*y : 8+(8*y)]
#    return state_array

def xorRoundKey(round_key, state_array):
    tempKey = BitVector(size = 0)
    #print(type(tempKey))
    for x in range(4):
        for y in range(4):
            tempKey += state_array[x][y]

    #print(type(tempKey))
    #print("temp: ",tempKey)
    #print("\nround:",round_key)
    tempKey ^= round_key
    
    return tempKey

if __name__ == '__main__':
    if(len(sys.argv) != 5):
        sys.exit('Wrong number of inputs')
    action = sys.argv[1]
    file_in_name = sys.argv[2]
    keytxt = sys.argv[3]
    file_out_name = sys.argv[4]
    #print(action, file_in_name, keytxt, file_out_name)

    if (action == "-e"):             #encryption
        #rnd_key = start(keytxt)
        encryptedMessage = encrypt(file_in_name, keytxt)
        #hexMessage = encryptedMessage.get_bitvector_in_hex()#BitVector(hexstring = str(encryptedMessage))
        #print('hexMessage: ', hexMessage)
        FILEOUT = open(file_out_name, 'wb')
        FILEOUT.write(encryptedMessage)
        FILEOUT.close

    elif (action == "-d"):        #decryption
        decryptedMessage = decrypt(file_in_name, keytxt)
        print(type(decryptedMessage))
        FILEOUT = open(file_out_name, 'w')
        #decryptedMessage.write_to_file(FILEOUT)
        finishedMessage = decryptedMessage.get_bitvector_in_ascii()
        #print(type(decryptedMessage))
        #FILEOUT = open(file_out_name, 'wb')
        FILEOUT.write(finishedMessage)
        FILEOUT.close
    else:
        print('second argument needs to be -e or -d')