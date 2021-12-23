# 객체지향 프로그래밍(OOP)
# 클래수 구조
# 재사용 용이, 코드 반복 최소화, 메소드 활용

class Car():
    def __init__(self, company, details):
        self._company = company
        self._details = details

    # string format을 이용해 내용 확인(사용자 레벨)
    def __str__(self):
        return 'str : {} - {}'.format(self._company, self._details)

    # 자료형 타입에 따른 객체 출력
    def __repr__(self):
        return 'repr : {} - {}'.format(self._company, self._details) 

car1 = Car('Ferrari', {'color': 'White', 'horsepower':400, 'price':8000})

print(car1) # __str__ 없이 클래스 정보 출력 <__main__.Car object at 0x7fec70b1bfd0>
print(car1.__dict__) # 딕셔너리 전체 출력


# 리스트 선언
car_list = []

car_list.append(car1) # repr method값이 들어감

print(car_list) # 출력결과  [repr : Ferrari - {'color': 'White', 'horsepower': 400, 'price': 8000}]