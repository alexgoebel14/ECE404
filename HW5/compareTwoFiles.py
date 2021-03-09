'''
Compare 2 files
'''

import sys


def compare(file1, file2, file3):
    with open(file1, 'rb') as f1:
        d = set(f1.readlines())
        
    with open(file2, 'rb') as f2:
        e = set(f2.readlines())
        
    open(file3, 'wb').close()
    
    with open(file3, 'ab') as f3:
        for line in list(d-e):
            f3.write(line)
            
            
if __name__ == '__main__':
    if(len(sys.argv) != 4):
        sys.exit("Wrong number of input arguments\n\n")
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    file3 = sys.argv[3]
    compare(file1,file2,file3)
    
    print("Comparison finished\n")
