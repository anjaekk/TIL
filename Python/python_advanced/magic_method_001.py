# Magic method(=special method)
# 클래스 안에 정의할 수 있는 특별한(Built-in) 메소드


print(int) # <class 'int'> -> 클래스
print(dir(int)) #['__abs__', '__add__', '__and__', '__bool__',...

n = 10

print(n + 100) # 110
print(n.__add__(100)) # 110
print(n * 100, n.__mul__(100)) # 1000 1000

print()
print()