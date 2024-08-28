def fan(a) :
    sum = 1
    for i in range(1,a+1) :
        sum = sum * i
    return sum
print(fan(10))