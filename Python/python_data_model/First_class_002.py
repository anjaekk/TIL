# Closure: 외부에서 호출된 함수의 변수값, 상태(레퍼런스) 복사 후 저장 후에 접근(엑세스) 가능
# Scope
# Global

# 파이썬 변수 범위
b = 20

def func_v1(a):
    print(a)
    print(b)

func_v1(10) # 10 20

c = 30

def func_v2(a):
    global c # 전역변수 참조(전역변수 값을 함수내부에서 수정하는 것은 좋지 않음)
    print(a)
    print(c)
    c = 40 # 전역변수 참조 설정 전 같은 이름으로 변수 설정 시 로컬변수로 인식해서 'unbound local error' 발생

print(c) # 함수실행 전 30
func_v2(10)
print(c) # 함수실행 후 40


# Closure 사용이유: 서버프로그래밍 -> 동시성(Concurrency)제어 -> 메모리 공간에 여러 자원이 접근 -> 교착상태(Dead lock)
# Python의 Dead lock 회피: 메모리를 공유하지 않고 메시지 전달로 처리하기 위한 언어 -> Erlang
# Python Closure는 공유하되 변경되지 않는(Immutable, read only) 적극적 사용 -> 함수형 프로그래밍
# 클로저는 불변자료구조 및 atom, STM을 통해 멀티스레드(Python에서는 Coroutine) 프로그래밍에 강점
a = 100
print(a + 100) # 200
print(a + 1000) # 1100


# 결과누적
# 함수 사용
print(sum(range(1, 51)))
print(sum(range(51, 101)))

# 클래스 사용
class Averager():
    def __init__(self):
        self._series = []

    def __call__(self, v): # 클래스를 함수처럼 사용하기
        self._series.append(v)
        print('inner >> {} / {}'.format(self._series, len(self._series)))
        return sum(self._series) / len(self._series)

# 인스턴스 생성
averager_cls = Averager()
print(dir(averager_cls)) # __call__...

# 누적(상태를 기억하고 있다)
print(averager_cls(10)) # 10.0
print(averager_cls(30)) # 20.0 -> (10 + 20) / (1 + 1)
print(averager_cls(50)) # 30.0 -> (10 + 20 + 50) / (1 + 1 + 1)

print()
print()


# Closure 사용
def closure_ex1():
    # 클로저 영역
    series = [] # 클로저 영역의 자유변수(내가 사용하려는 함수 밖에서 선언된 변수-Free variable)
    def averager(v):
        series.append(v)
        print('inner >>> {} / {}'.format(series, len(series)))
        return sum(series) / len(series)
    return averager

avg_closure1 = closure_ex1()

print(avg_closure1(10)) # 10.0
print(avg_closure1(30)) # 20.0
print(avg_closure1(50)) # 30.0

print()
print()

# function inspection
print(dir(avg_closure1))
print()
print(dir(avg_closure1.__code__)) # 'co_freevars'(자유변수)....
print(avg_closure1.__code__.co_freevars) # ('series',)
print()
print(avg_closure1.__closure__[0].cell_contents) # [10, 30, 50]


print()
print()

# 잘못된 클로저 사용
def closure_ex2():
    # Free variable
    cnt = 0
    total = 0
    def averager(v):
        cnt += 1
        total  += v
        return total / cnt
    return averager

avg_closure2 = closure_ex2()
# print(avg_closure2(10)) # UnboundLocalError: local variable 'cnt' referenced before assignment

def closure_ex3():
    cnt = 0
    total = 0
    def averager(v):
        nonlocal cnt, total # 자유변수라고 알려주기
        cnt += 1
        total  += v
        return total / cnt
    return averager

avg_closure3 = closure_ex3()
print(avg_closure3(10))