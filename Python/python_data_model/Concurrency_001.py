# Concurrency(병행성)
# 병행성, 흐름제어
# Iterator
# Generator(Iterator를 만드는 것)
# 클래스기반 제너레이터


# 반복가능한 이유: iter(x) 함수 호출했기 떄문에
t = 'ABCD'

# for c in t:
#     print(c)

# while
w = iter(t)

# print(next(w)) # A
# print(next(w)) # B
# print(next(w)) # C
# print(next(w)) # D

while True:
    try:
        print(next(w))
    except StopIteration:
        break


# 반복형 확인 방법
from collections import abc  # abstract class(상속을 받았는지 확인)
print(dir(t))
print(hasattr(t, '__iter__')) # True
print(isinstance(t, abc.Iterable)) # True

print()
print()


class WordSplitter:
    def __init__(self, text):
        self._idx = 0
        self._text = text.split(' ')

    def __next__(self):  # 위에서 썼던 이 next 함수 'print(next(w))'
        print('Called __next__')
        try:
            word = self._text[self._idx]
        except IndexError:
            raise StopIteration('Stopped Iteration')
        self._idx += 1
        return word

    def __repr__(self):
        return 'WordSplit(%s)' % (self._text)

wi = WordSplitter('Do today what you could do tommorrow')
print(next(wi)) # Do
print(next(wi)) # today
print(next(wi)) # what
print(next(wi)) # you

print()
print()


# Generator 패턴
# 1. 지능형 리스트, 딕셔너리, 집합 -> 데이터 양 증가 후 메모리 사용량 증가(제너레이터 사용 권장)
# 2. 단위 실행 가능한 코루틴(Coroutine) 구현과 연동
# 3. 작은 메모리 조각 사용

class WordSplitGenerator:
    def __init__(self, text):
        self._text = text.split(' ')

    def __iter__(self):
        for word in self._text:
            yield word # 제너레이터, 인덱스를 사용하지않아도 그 값의 상태, 레퍼런스를 기억
        return 
    
    def __repr__(self):
        return 'WordSplitGenerator(%s)' % (self._text)
    
wg = WordSplitGenerator('Do today what you could do tommorrow')

wt = iter(wg)

print(wt, wg)




