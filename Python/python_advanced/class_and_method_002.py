class Car():
    """
    Car class
    Author: An
    Date : 2021.12.22
    """

    #클래스 변수(모든 인스턴스가 공유)
    car_count = 0

    def __init__(self, company, details):
        self._company = company #클래스 변수인 걸 표시하기위해 언더바로 시작(관례)
        self._details = details
        Car.car_count += 1

    def __str__(self):
        return 'str : {} - {}'.format(self._company, self._details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self._company, self._details) 

    def __del__(self):
        Car.car_count -= 1

    def detail_info(self):
        print('Currendt ID : {}'.format(id(self)))
        print('Car Detail Info : {} {}'.format(self._company, self._details.get('price')))


car1 = Car('Ferrari', {'color': 'White', 'horsepower':400, 'price':8000})
car2 = Car('Bmw', {'color': 'Black', 'horsepower':270, 'price':5000})
car3 = Car('Audi', {'color': 'Silver', 'horsepower':300, 'price':6000})


# ID 확인
print(id(car1)) # 140590800175056
print(id(car2)) # 140590800174960
print(id(car3)) # 140590800174672

print(car1._company == car2._company) # 값 비교
print(car1 is car2) # ID비교

# 비교
print(id(car1.__class__) == id(car2.__class__)) # True
print(id(car1.__class__), id(car2.__class__))  # 140469409551008 140469409551008

# dir & __dict__ 확인
print(dir(car1)) # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_company', '_details']


car1.detail_info()
# 클래스로 호출 car1.detail_info()와 동일
Car.detail_info(car1)


print(Car.car_count) # 3개 넣었으니 3

# 삭제 확인
del car2
print(Car.car_count) # 2 __del__메소드 적용


# 인스턴스 네임스페이스 없으면 상위에서 검색
# 즉, 동일한 이름으로 변수 생성 가능함(인스턴스 검색 후 -> 상위(클래스 변수, 부모 클래스 변수) 확인)
print(car1.car_count) # 인스턴스 검색(인스턴스에 없으니 상위 클래스 검색)
print(Car.car_count) # 클래스 검색

print(Car.__doc__) # 클래스에 남긴 주석 나옴 Car class  Author: An Date : 2021.12.22