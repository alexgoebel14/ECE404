ho = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]

'''
#For inverse element checking of modulo addition
identity = 0
for a in ho:
    for b in ho:
        x = (a+b)%18
        if x==identity:
            print(a, " Has the inverse element of ", b)
            break
        if(b == 17) and x != identity:
            print(a, " Has no inverse element")
'''

'''
#For inverse element checking of modulo multiplication
identity = 1
for a in ho:
    for b in ho:
        x = (a*b)%18
        if x==identity:
            print(a, " Has the inverse element of ", b)
            break
        if(b == 17) and x != identity:
            print(a, " Has no inverse element")
'''

#Question 2
def gcd(a,b):
    if a <= b:
        print("Look at values")
        exit
    elif (b == 0):
        print("The GCD is: ", a)
        exit
    else:
        temp = b
        b = a%b
        a = temp
        print("gcd(",a,",",b,")")
        gcd(a,b)

if __name__ == '__main__':
    a = int(input("\n Enter a value for gcd: "))
    b = int(input("\n Enter b value for gcd: "))
    gcd(a,b)

