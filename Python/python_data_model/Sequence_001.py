# 시퀀스형
# 컨테이너(Container: 서로 다른 자료형[list, tuple, collections.deque])
# 플랫(Flat: 한개의 자료형[str, bytes, bytearray, array.array, memoryview])
# 가변형: list, bytearray, array.array, memoryview, deque
# 불변: tuple, str, bytes


# 지능형 리스트(Comprehending Lists)

chars = '+_)(*&^%$#@!' # 임의의 문자
code_list1 = []

for s in chars:
    code_list1.append(ord(s)) # ord() 문자 -> 유니코드

print(code_list1)  # [43, 95, 41, 40, 42, 38, 94, 37, 36, 35, 64, 33]

# 지능형 리스트 변경
code_list2 = [ord(s) for s in chars]
print(code_list2)

# Comprehending Lists + Map, Filter
code_list3 = [ord(s) for s in chars if ord(s) > 40]
print(code_list3) # [43, 95, 41, 42, 94, 64]

code_list4 = list(filter(lambda x : x > 40, map(ord, chars)))
print(code_list4) # [43, 95, 41, 42, 94, 64]



# Generator 생성 - 다음에 반환할 값만 가지고 있음(메모리 유지를 하지 않아 메모리 사용량이 적음)
import array 

tuple = [ord(s) for s in chars] 
print(tuple) # [43, 95, 41, 40, 42, 38, 94, 37, 36, 35, 64, 33]

tuple_g = (ord(s) for s in chars)
print(tuple_g) # <generator object <genexpr> at 0x7fa9cf32f9e0>
print(next(tuple_g)) # 43
print(next(tuple_g)) # 95
print(next(tuple_g)) # 41
print(next(tuple_g)) # 40
print(next(tuple_g)) # 42
print(next(tuple_g)) # 38
print(next(tuple_g)) # 94
print(next(tuple_g)) # 37
print(next(tuple_g)) # 36
print(next(tuple_g)) # 35
# generator 모두 출력시 print(next(tuple_g)) StopIteration 예외 발생

array_g = array.array('I', (ord(s) for s in chars))
print(type(array_g)) # <class 'array.array'>
print(array_g.tolist()) # array -> list 변환


print(('%s' % c + str(n) for c in ['A', 'B', 'C', 'D'] for n in range(1, 21)))
for s in ('%s' % c + str(n) for c in ['A', 'B', 'C', 'D'] for n in range(1, 21)):
    print(s)

print()
print()

# list 주의(깊은복사, 얕은복사)
marks1 = [['~'] * 5 for n in range(3)]
marks2 = [['~'] * 5] * 3  # 하나의 주소 값 복사
print(marks1) # [['~', '~', '~', '~', '~'], ['~', '~', '~', '~', '~'], ['~', '~', '~', '~', '~']]
print(marks2) # [['~', '~', '~', '~', '~'], ['~', '~', '~', '~', '~'], ['~', '~', '~', '~', '~']]


# 수정
marks1[0][1] = 'X'
marks2[0][1] = 'X'
print(marks1) # [['~', 'X', '~', '~', '~'], ['~', '~', '~', '~', '~'], ['~', '~', '~', '~', '~']]
print(marks2) # [['~', 'X', '~', '~', '~'], ['~', 'X', '~', '~', '~'], ['~', 'X', '~', '~', '~']]


#증명
print([id(i) for i in marks1]) # [140470640892928, 140470640892864, 140470640892672]
print([id(i) for i in marks2]) # [140470640892608, 140470640892608, 140470640892608]

# list vs array
# 리스트 기반일때: 융통성(컨테이너라 다양한 데이터 타입 사용 가능), 다양한 자료형, 범용적 사용
# 숫자 기반일떄: 배열(리스트와 거의 호환)-array