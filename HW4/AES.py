'''
Homework Number: 4
Name: Alex Goebel
ECN Login: goebel2
Due Date: 2/23/2021
'''

#!/usr/bin/env python3

import sys
from BitVector import *

if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Incorrect number of arguments, please try again')
    if sys.argv[1] == '-e':
        inFileName = sys.argv[2]
        encryptionKeyFile = sys.argv[3]
        encryptionKeyFile = open(encryptionKeyFile)
        encryptionKey = encryptionKeyFile.read()
        output = encrypt(inFileName, encryptionKey)
        outFile = sys.argv[4]
        outFile = open(outFile, 'w')
        outFile.write(output.get_hex_string_from_bitvector())
        outFile.close()
        encryptionKeyFile.close()
    