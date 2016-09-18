from math import log, fabs
def fauth(x):
    if x>4:
        return log(x,4)
    elif x >= -4:
        return x/4
    else:
        return - log(fabs(x),4)

print (fauth(-16))
print(pow(2,1))
