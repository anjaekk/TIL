# Concurrency 병행성: 한 컴퓨터가 여러 일을 동시에 수행(내가 어디까지 했는지 마지막 지점을 알아야 함)
# 병행성은 python의 큰 장점(coroutine) 쓰레드는 하나지만 마치 동시에 하는 것처럼 함
# Parallelism 병렬성: 여러 컴퓨터가 여러 작업을 동시에 수행(파이썬은 병행성과 병렬성 둘다 사용)
# 제너레이터 실습
# Yield
# Itertools

def generator_ex1():
    print('Start')
    yield 'A point'
    print('Continue')
    yield 'B point'
    print('End')

temp = iter(generator_ex1())

print(temp) # <generator object generator_ex1 at 0x7fa5d1a65510>

print(next(temp))
# Start
# A point
print(next(temp))
# Continue
# B point

for v in generator_ex1():
    print(v)

print()
print()


temp2 = [x * 3 for x in generator_ex1()]
temp3 = (x * 3 for x in generator_ex1()) # generator

print(temp2) # ['A pointA pointA point', 'B pointB pointB point']
print(temp3)

for i in temp3:
    print(i)

print()
print()

import itertools

gen1 = itertools.count(1, 2.5) # 1에서 2.5씩 증가

print(next(gen1)) # 1
print(next(gen1)) # 3.5
print(next(gen1)) # 6.0


gen2 = itertools.takewhile(lambda n: n < 1000, itertools.count(1, 2.5))
# for i in gen2:
#     print(i)

print()
print()

gen3 = itertools.filterfalse(lambda n: n < 3, [1,2,3,4,5]) # 해당하는 값의 반대값(1, 2를 제외한 반대값 나옴)
for i in gen3:
    print(i) # 3, 4, 5


# 누적합계
gen4 = itertools.accumulate([x for x in range(1, 101)])
for i in gen4:
    print(i) # 1 3 6 10 ....

print()
print()

# 연결1
gen5 = itertools.chain('ABCDE', range(1, 11, 2))
print(list(gen5)) # ['A', 'B', 'C', 'D', 'E', 1, 3, 5, 7, 9]

# 연결2
gen6 = itertools.chain(enumerate('ABCDE'))
print(list(gen6)) # [(0, 'A'), (1, 'B'), (2, 'C'), (3, 'D'), (4, 'E')]

print()
print()

gen7 = itertools.product('ABCDE')
print(list(gen7)) # [('A',), ('B',), ('C',), ('D',), ('E',)]

gen8 = itertools.product('ABCDE', repeat=2)
print(list(gen8)) # [('A', 'A'), ('A', 'B'), ('A', 'C'), ('A', 'D').. 2개 조합으로 모든 경우의 수 찾아줌

# 그룹화
gen9 = itertools.groupby('AAABCCCDD')
#print(list(gen9)) # [('A', <itertools._grouper object at 0x7fac74a27fa0>),...

for chr, group in gen9:
    print(chr, ' : ', list(group))
# A  :  ['A', 'A', 'A']
# B  :  ['B']
# C  :  ['C', 'C', 'C']
# D  :  ['D', 'D']


