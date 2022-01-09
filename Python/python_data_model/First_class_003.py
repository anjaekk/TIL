# Decorator

# 장점
# 1. 중복제거, 코드 간결, 공통함수 작성
# 2. 로깅, 프레임워크, 유효성 체크 -> 공통함수

# 단점
# 디버깅의 불편함

import time

# 특정함수의 실행시간, 종료시간등 로그파악 함수
def perf_clock(func):
    def perf_clocked(*args):
        # 함수 시작 시간
        st = time.perf_counter()
        # 함수실행
        result = func(*args) # 부모함수 실행
        # 함수 종료 시간
        et = time.perf_counter() - st
        # 실행 함수명
        name = func.__name__
        # 함수 매개변수
        arg_str = ', '.join(repr(arg) for arg in args)
        # 결과 출력
        print('[%0.5fs] %s(%s) -> %r' % (et, name, arg_str, result))
        return result
    return perf_clocked


def time_func(seconds):
    time.sleep(seconds)

def sum_func(*numbers):
    return sum(numbers)

# 데코레이터 미사용 = 클로져 사용
none_deco1 = perf_clock(time_func)
none_deco2 = perf_clock(sum_func)

print(none_deco1, none_deco1.__code__.co_freevars) # <function perf_clock.<locals>.perf_clocked at 0x7fc092a623a0> ('func',)
print(none_deco2, none_deco2.__code__.co_freevars) # <function perf_clock.<locals>.perf_clocked at 0x7fc092a62430> ('func',)

print('-' * 40, 'Called None Decorator -> time_func')
print()
none_deco1(1.5)

print('-' * 40, 'Called None Decorator -> sum_func')
print()
none_deco2(100, 200, 300, 400, 500)

print()
print()


@perf_clock
def time_func(seconds):
    time.sleep(seconds)

@perf_clock
def sum_func(*numbers):
    return sum(numbers)

print('-' * 40, 'Called Decorator -> time_fumc')
print()
time_func(1.5)

print('-' * 40, 'Called Decorator -> sum_fumc')
print()
sum_func(100, 200, 300, 400, 500)