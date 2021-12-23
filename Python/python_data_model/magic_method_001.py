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


class Fruit:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    def __str__(self):
        return 'Fruit Class Info : {}, {}'.format(self._name, self._price)

    def __add__(self, x):
        return self._price + x._price
    
    def __sub__(self, x):
        return self._price - x._price

    # 대소비교
    def __le__(self, x):
        if self._price <= x._price:
            return True
        else:
            return False
    
    # 대소비고
    def __ge__(self, x):
        if self._price >= x._price:
            return True
        else:
            return False


# 인스턴스 생성
s1 = Fruit('Orange', 7500)
s2 = Fruit('Banana', 3000)

# magic method 미사용
print(s1._price + s2._price)

# magic method 
print(s1 + s2) 

print(s1 >= s2) # True