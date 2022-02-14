# Concourrency
# Coroutine(코루틴)

# 쓰레드: os에서 관리, CPU 코어에서 실시간, 시분할 비동기 작업 -> 멀티 쓰레드
# 코루틴: 싱글 쓰레드에서 스텍 기반 비동기 작업

# yield: 코루틴 제어, 상태, 양방향 전송

# 서브루틴: 메인루틴에서 호출하면 서브루틴에서 실행(흐름제어)
# 코루틴: 루틴 실행 중 중지 후 재시작 가능(동시성 프그래밍) -> 쓰레드에 비해 오버헤드 감소
# 멀티쓰레드: 코딩하기 복잡(공유되는 자원 때문에 교착상태 발생가능성, 컨텍스트 스위칭 비용이 큼, 자원 소비 가능성 큼)



# Coroutine
from types import coroutine


def coroutine1():
    print(">>> coroutine started.")
    i = yield
    print(">>> coroutine received: {}".format(i))

# mian routine
# 제너레이터 선언
cr1 = coroutine1()

print(cr1, type(cr1))

next(cr1)

#cr1.send(100) # 값 전송

# 코루틴 상태 값 확인
# GEN_CREATED: 처음 대기 상태
# GEN_RUNNING: 실행 상태
# GEN_SUSPENDED: yield 대기 상태
# GEN_CLOSED: 실행 완료 상태

def coroutine2(x):
    print(">>> coroutine started: {}".format(x))
    y = yield x
    print(">>> coroutine received: {}".format(x))
    z = yield x + y
    print(">>> coroutine received: {}".format(z))

cr3 = coroutine2(10)

from inspect import getgeneratorstate

print(getgeneratorstate(cr3)) #GEN_CREATED

print(next(cr3)) # y값을 받을 대기상태

print(getgeneratorstate(cr3)) #GEN_SUSPENDED

cr3.send(100) # >>> coroutine received: 10

print(getgeneratorstate(cr3)) #GEN_SUSPENDED

print()
print()


