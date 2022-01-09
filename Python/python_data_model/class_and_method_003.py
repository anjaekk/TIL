#Class method
#Instance method
#Static method


class Car():
    """
    Car class
    Author: An
    Date : 2021.12.22
    """

    price_per_raise = 1.0

    def __init__(self, company, details):
        self._company = company
        self._details = details

    def __str__(self):
        return 'str : {} - {}'.format(self._company, self._details)

    def __repr__(self):
        return 'repr : {} - {}'.format(self._company, self._details) 

    #Instance method
    #self: 객체 고유한 속성 값을 사용
    def detail_info(self):
        print('Currendt ID : {}'.format(id(self)))
        print('Car Detail Info : {} {}'.format(self._company, self._details.get('price')))

    #Instance method
    def get_price(self):
        return 'Before Car Price -> company : {}, price : {}'.format(self._company, self._details.get('price'))
    
    #Instance method
    def get_price_culc(self):
        return 'After Car Price -> company : {}, price : {}'.format(self._company, self._details.get('price') * Car.price_per_raise)

    #Class method
    @classmethod # 클래스변수는 모두가 참조하기 떄문에 데코레이터 표시해야함
    def raise_price(cls, per): #cls == Car
        if per <= 1:
            print('Please Enter 1 Or More')
            return
        cls.price_per_raise = per
        print('Succed! price increased.')
    
    #Static method -> 아무런 인자를 받지 않을 수 있음
    #Static method는 주로 class 내부 요소들과 공통적 역할을 하는 함수에 사용
    @staticmethod
    def is_bmw(inst): #임의로 넣어준 인스턴스
        if inst._company == 'Bmw':
            return 'OK! This car is {}'.format(inst._company)
        return 'It is not Bmw'
        


car1 = Car('Ferrari', {'color': 'White', 'horsepower':400, 'price':8000})
car2 = Car('Bmw', {'color': 'Black', 'horsepower':270, 'price':5000})


# 가격정보 get을 이용해 딕셔너리에서 직접 가져와 활용은 변동의 우려가 있어 좋지않음 -> method활용
print(car1._details.get('price'))
print(car2._details['price'])


# 가격정보(인상 전)
print(car1.get_price()) # Before Car Price -> company : Ferrari, price : 8000

# 인상(직접접근이라 좋지 않음 -> 메소드 활용)
Car.price_per_raise = 1.4

# 가격정보(인상 후)
print(car1.get_price_culc()) # After Car Price -> company : Ferrari, price : 11200.0

# Class method활용 = 클래스 변수 핸들링할 때
Car.raise_price(1) # Please Enter 1 Or More
Car.raise_price(1.86)

print(car1.get_price_culc()) #After Car Price -> company : Ferrari, price : 14880.0


# Static method활용
print(car1.is_bmw(car1)) #It is not Bmw
# Static method는 클래스 호출도 가능
print(Car.is_bmw(car2)) #OK! This car is Bmw