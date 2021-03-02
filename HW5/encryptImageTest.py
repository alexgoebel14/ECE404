from AES_image import ctr_aes_image
from BitVector import *
iv = BitVector(textstring='computersecurity') #iv will be 128 bits
ctr_aes_image(iv, 'image.ppm', 'enc_image.ppm', 'keyCTR.txt')
