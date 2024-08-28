def Caculators(a,b,c):
    if b=='+' :
        result = a+c
    elif b=='-':
        result = a-c
    elif b=='*':
        result = a*c
    elif b=='/':
        result = a/c
    else :
        print("Illegal Entry!!!")
        return None
    return result
a=float(input("请输入一个数字："))
b=input("请输入一个字符：")
c=float(input("请输入一个数字："))
result = Caculators(a,b,c)
if result is not None :
    print("输出结果为：",result)#test
