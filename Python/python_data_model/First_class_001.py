# 일급함수
# Lambda
# Callable
# Partial

# 일급함수 특징
# 1. 런타임 초기화
# 2. 변수 할당 가능
# 3. 함수 인수 전달 가능
# 4. 함수 결과 반환 가능(return)

def factorial(n):
    '''Factorial Function -> n : int'''
    if n == 1: # n < 2
        return 1
    return n * factorial(n-1)

class A:
    pass

print(factorial(5))
print(factorial.__doc__)
print(type(factorial), type(A)) # <class 'function'> <class 'type'>
# 함수만 가진 속성만 확인
print(set(sorted(dir(factorial))) - set(sorted(dir(A))))
# {'__name__', '__closure__', '__defaults__', '__kwdefaults__', '__get__', '__call__', '__code__', '__qualname__', '__annotations__', '__globals__'}

# 변수 할당
var_func = factorial

print(var_func) # <function factorial at 0x7ff3e97d3160>
print(list(map(var_func, range(1, 11)))) # [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]


# 함수 인수전달 및 함수로 결과 반환 -> 고위함수(Higher-order function)
# map, filter, reduce

# 홀수 팩토리얼
print(list(map(var_func, filter(lambda x: x % 2, range(1, 6)))))
print([var_func(i) for i in range(1, 6) if i % 2]) # [1, 6, 120]

from functools import reduce
from operator import add

# 1~10 까지의 합
print(sum(range(1, 11))) # 55
print(reduce(add, range(1, 11))) # 55


# lambda - 가급적 주석 작성
print(reduce(lambda x, t: x + t, range(1, 11)))

# Callable: 호출연산자 -> 메소드 형태로 호출 가능한지 확인
# 호출 가능한지 확인
print(callable(str), callable(list)) # True True


# Partial: 인수고정 -> 콜백 함수 사용
from operator import mul
from functools import partial

print(mul(10, 10)) # 100
# 앞에 10은 고정하고 뒤는 바뀔 때 사용
five = partial(mul, 5) # 5 * ?
print(five(10)) # 50
print(five(1000)) # 5000

# 고정 추가
six = partial(five, 6)
print(five(10)) # 50
print(six()) # 30

# 5의 배수 구하기
print([five(i) for i in range(1, 11)]) # [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]