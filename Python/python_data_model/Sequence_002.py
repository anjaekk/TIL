# Tuple Advanced
# Mutable, Immutable
# Sort, Sorted


# Tuple Advanced
# Unpacking

print(divmod(100, 9)) # (11, 1) 몫과 나머지 반환
# 값을 튜플로 반환하고 싶을 때 
# print(divmod((100, 9))) # TypeError: divmod expected 2 arguments, got 1

# Unpacking
print(divmod(*(100, 9))) # (11, 1)
print(type(divmod(*(100, 9)))) # <class 'tuple'>

# 결과 값을 Unpacking
print(*(divmod(100, 9))) # 11 1

# x, y , rest = range(10)  # ValueError: too many values to unpack (expected 3)
x, y , *rest = range(10)
print(x, y, rest) # 0 1 [2, 3, 4, 5, 6, 7, 8, 9]

print()
print()

# Mutable(가변), Immutable(불변)
l = (15, 20, 25) # tuple - immutable
m = [15, 20, 25] # list - mutable

print(id(l)) # 140247201485888
print(id(m)) # 140247201943744

l = l * 2
m = m * 2
print(l, id(l)) # (15, 20, 25, 15, 20, 25) 140247201686240 id값 변경
print(m, id(m)) # [15, 20, 25, 15, 20, 25] 140247201943616 id값 변경

l *= 2
m *= 2
print(l, id(l)) # (15, 20, 25, 15, 20, 25, 15, 20, 25, 15, 20, 25) 140564080622464 id값 변경
print(m, id(m)) # [15, 20, 25, 15, 20, 25, 15, 20, 25, 15, 20, 25] 140247201943616 id값 동일


# sort: 정렬 후 객체 직접 변경
# sorted: 정렬 후 새로운 객체 반환
# reverse, key=len, key=str.lower, key=func
f_list = ['orange', 'apple', 'mango']
print(sorted(f_list, key = lambda x: x[-1])) # ['orange', 'apple', 'mango'] 맨 끝 글자를 기준으로 정렬