# 데이터 모델 추상화
# 데이터 모델 설계
# NamedTuple, Model Unpacking

# 두점사이의 거리 구하기

pt1 = (1.0, 5.0)
pt2 = (2.5, 1.5)

from math import sqrt # 루트 함수

l_leng1 = sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) # 두점사이 거리 공식

print(l_leng1)



# NamedTuple - 튜플인데 딕셔너리의 형태를 가지고 있음(key, value, index)
from collections import namedtuple

# 네임드 튜플 선언
Point = namedtuple('Point', 'x y')

pt3 = Point(1.0, 5.0)
pt4 = Point(2.5, 1.5)

print(pt3)  # Point(x=1.0, y=5.0)

l_leng2 = sqrt((pt3.x - pt4.x) ** 2 + (pt3.y - pt4.y) ** 2)

print(l_leng2)

# 네임드 튜플 선언 방법
Point1 = namedtuple('Point', ['x', 'y'])
Point2 = namedtuple('Point', 'x, y')
Point3 = namedtuple('Point', 'x y')
Point4 = namedtuple('Point', 'x y x class', rename=True) # Default = False, 중복, 예약어(class) 허용 -> 이름을 난수로 바꿔버림

print(Point4) # <class '__main__.Point'>
p = Point4(10, 20, 30, 40)
print(p)  # Point(x=10, y=20, _2=30, _3=40)



# Dict to Unpacking
tmp_dict = {'x':75, 'y':55}
du = Point1(**tmp_dict)
print(du) # Point(x=75, y=55)



# 네임드 튜플 메소드

# _make() 리스트 -> 네임드 튜플객체 생성
tmp_list = [52, 38]
m = Point2._make(tmp_list) 
print(m) # Point(x=52, y=38)

# _fields() 필드 네임 확인
print(du._fields, m._fields) # ('x', 'y') ('x', 'y')

# _asdict() 정렬된 딕셔너리 반환(OrderedDict 반환)
print(du._asdict()) # {'x': 75, 'y': 55}