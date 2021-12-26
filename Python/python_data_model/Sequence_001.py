# 시퀀스형
# 컨테이너(Container: 서로 다른 자료형[list, tuple, collections.deque])
# 플랫(Flat: 한개의 자료형[str, bytes, bytearray, array.array, memoryview])
# 가변형: list, bytearray, array.array, memoryview, deque
# 불변: tuple, str, bytes


# 지능형 리스트(Comprehending Lists)

chars = '+_)(*&^%$#@!' # 임의의 문자
code_list1 = []

for s in chars:
    code_list1.append(ord(s))

print(code_list1)  # [43, 95, 41, 40, 42, 38, 94, 37, 36, 35, 64, 33]

# 지능형 리스트 변경
code_list2 = [ord(s) for s in chars]
print(code_list2)

# Comprehending Lists + Map, Filter
code_list3 = [ord(s) for s in chars if ord(s) > 40]
print(code_list3) # [43, 95, 41, 42, 94, 64]

code_list4 = list(filter(lambda x : x > 40, map(ord, chars)))
print(code_list4) # [43, 95, 41, 42, 94, 64]