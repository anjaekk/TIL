# 2장

# 목차

### **2장 리스트와 딕셔너리**

- Better way 11 시퀀스를 슬라이싱하는 방법을 익혀라
- Better way 12 스트라이드와 슬라이스를 한 식에 함께 사용하지 말라
- Better way 13 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라
- Better way 14 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하라
- Better way 15 딕셔너리 삽입 순서에 의존할 때는 조심하라
- Better way 16 in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라
- Better way 17 내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용하라
- Better way 18 __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라

# Summary

### 11. 시퀀스를 슬라이싱하는 방법을 익혀라

- 시각적 잡음을 없애기 위해 슬라이싱시 인덱스 0과 끝인덱스는 생략하는 게 좋습니다.
    
    ```python
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    # worse way
    start = a[0:5]
    end = a[5:8]
    
    # better way
    start = a[:5]
    end = a[5:]
    ```
    
- 슬라이싱의 범위를 넘어가는 인덱스도 허용되기 때문에 길이를 제한할 때 쉽게 표현이 가능합니다.
    
    ```python
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    print(f"결과: {a[30:]}") # 결과: []
    ```
    
- 리스트 슬라이스에 시퀀스 대입이 가능하며 슬라이스 부분과 대입하는 시퀀스의 길이가 달라도 됩니다.
    
    ```python
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    b = [1, 2, 3, 4]
    a[2:6] = b
    
    print(a) # ['a', 'b', 1, 2, 3, 4, 'g', 'h']
    ```
    

### 12. 스트라이드와 슬라이스를 한 식에 함께 사용하지 말라

스트라이드란, 파이썬 리스트를 [시작:끝:증가값] 으로 슬라이싱한 것을 말합니다.

- 스트라이드와 슬라이스를 한 식에 함께 사용하지 말고 분리합니다. (함께 사용시에는 `itertools` 내장 모듈의 `islice`를 사용합니다.)
    
    ```python
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    
    # worse way
    b = a[2::2] # [2, 4, 6, 8, 10, 12]
    
    # better way1
    c = a[::2]
    d = c[1:] # [2, 4, 6, 8, 10, 12]
    
    # better way2
    from itertools import islice
    e = list(islice(a, 2, None, 2)) # [2, 4, 6, 8, 10, 12]
    ```
    
- 증가값에 가급적 음수 사용을 지양합니다.

### 13. 슬라이싱보다는 나머지를 모두 잡아내는 언패킹을 사용하라

- 언패킹 대입에 별표식을 사용하면 언패킹 패턴에서 대입되지 않는 모든부분을 리스트로 잡아낼 수 있습니다. 리스트를 서로 겹치지 않게 여러 조각으로 나눌 경우 슬라이싱과 인덱싱을 사용하기보단 언패킹을 이용하면 실수할 여지가 훨씬 줄어들게 됩니다.
    
    ```python
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    first, second, *others = a
    
    print(first, second, others) 
    # 0 1 [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    
    first, *midles, last = a
    print(first, midles, last)
    # 0 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] 13
    ```
    

### 14. 복잡한 기준을 사용해 정렬할 때는 key 파라미터를 사용하라

- 정수와 같이 자연스러운 순서가 있는 경우를 제외하곤 key 파라미터에 함수를 넘겨서 정렬할 수 있습니다.(원소 애트리뷰트에 접근, 인덱스 값, 원소가 시퀀스 혹은 튜플 혹은 딕셔너리인 경우)
    
    ```python
    class DoubleAlphabet:
        def __init__(self, name: str, value: int) -> None:
            self.name = name
            self.value = value
    
        def __repr__(self) -> str:
            return f"DA({self.name}, {self.value})"
        
    alphabet = [
        DoubleAlphabet("dd", 2),
        DoubleAlphabet("aa", 3),
        DoubleAlphabet("bb", 4),
        DoubleAlphabet("ee", 1),
        DoubleAlphabet("cc", 4),
        ]
    
    print(f"미정렬: {repr(alphabet)}")
    # 미정렬: [DA(dd, 2), DA(aa, 3), DA(bb, 4), DA(ee, 1), DA(cc, 4)]
    
    # 모든 기준 내림차순
    alphabet.sort(key=lambda x: (x.name, x.value), reverse=True)
    print(alphabet) 
    # [DA(ee, 1), DA(dd, 2), DA(cc, 4), DA(bb, 4), DA(aa, 3)]
    
    ```
    
- 단항(unary)부호 반전 연산자를 이용해 정렬 순서를 반전시킬 수 있습니다.
- 각각 정렬 조건마다 순서 방향을 다르게 지정하고 싶다면 단항부호 반전연산자를 사용할 수 있는 경우에는 가능하지만 일부 불가능한 조합일 경우에는 sort를 여러번 호출하는 방법을 쓸 수 있습니다.(이때, 정렬 호출 순서는 중요도의 역순으로 호출 해야한다는 것에 주의합니다.)
    
    ```python
    # value는 오름차순, name은 내림차순
    alphabet.sort(key=lambda x: (x.value, -x.name))
    
    # error
    # TypeError: bad operand type for unary -: 'str'
    
    # better way
    alphabet.sort(key=lambda x: x.name, reverse=True)
    alphabet.sort(key=lambda x: x.value)
    print(alphabet)
    ```
    

### 15. 딕셔너리 삽입 순서에 의존할 때는 조심하라

- 파이썬 3.6 이상부터 dict 타입의 삽입 순서가 보존되었습니다.(3.6이전 딕셔너리 구현이 내장 hash 함수와 파이썬 인터프리터가 시작할 때 초기화되는 난수 seed값을 사용하는 해시테이블 알고리즘으로 만들어졌기 때문입니다.)
- 파이썬은 정적타입 언어가 아닌 덕타이핑에 의존하기 때문에 딕셔너리와 비슷한 객체를 만들면 순서가 보장되지 않습니다. 그러므로 순서 보존에 의존하지 않도록 코드를 작성하거나 명시적으로 dict 타입인지 검사를 하는 방법이 있습니다.
    
    

### 16. in을 사용하고 딕셔너리 키가 없을 때 KeyError를 처리하기보다는 get을 사용하라

- 딕셔너리에 키가 있는지 in을 통해 확인하거나 없을 때 KeyError를 처리하는 것보다 get 메서드를 이용하는 것이 효율적입니다.
    
    ```python
    simple_dict = {"a": 1, "b": 2, "c": 3}
    
    # worse way1 - in 사용
    if "d" in simple_dict:
        simple_dict["d"] += 1
    else:
        simple_dict["d"] = 1
    
    # worse way2 - KeyError 사용
    try:
        simple_dict["d"] += 1
    except KeyError:
        simple_dict["d"] = 1
    
    # better way1 = get 사용
    count = simple_dict.get("d", 0)
    simple_dict["d"] = count + 1
    
    # better way2 = defaultdict 사용
    from collections import defaultdict
    
    # 기본값을 0으로 하고 simple_dict의 값을 가지고 있는 defaultdict 생성
    default_dict = defaultdict(int, simple_dict)
    default_dict["d"] = 1
    print(simple_dict) # {'a': 1, 'b': 2, 'c': 3, 'd': 3}
    ```
    

### 17. 내부 상태에서 원소가 없는 경우를 처리할 때는 setdefault보다 defaultdict를 사용하라

- setdefault는 이름은 set이지만 기능은 get or set으로 코드의 동작을 바로 이해하기 어렵고 특정 key값이 있던 없던 set 인스턴스를 만들기 때문에 효율적이지 않습니다.
- defaultdict 클래스는 키가 없을 때 자동으로 디폴트 값을 저장해서 이런 용법을 간단하게 처리할 수 있게 도와주기 때문에 가급적이면 defaultdict을 사용하는 것을 권장합니다.
- 하지만 setdefault가 더 짧은 코드를 만들어 내는 경우에는 setdefault를 사용하는 방안도 고려해보는게 좋습니다.

### 18. __missing__을 사용해 키에 따라 다른 디폴트 값을 생성하는 방법을 알아두라

- 디폴트 값을 만드는 계산 비용이 높거나 만드는 과정에서 예외가 발생할 수 있는 상황에서는 setdefault를 사용하지 말아야 합니다.
- defaultdict에 전달되는 함수는 인자를 따로 받지 않아서 해당 key에 맞는 디폴트 값을 생성하는 것은 불가능 합니다.
- 디폴트 키를 만들 때 어떤 키를 사용했는지 알아야 하는 상황이라면 직접 dict의 하위 클래스에 `__missing__`메서드를 정의하면 됩니다.
- 코드보기
    
    ```python
    # 필요할 때 파일을 읽고 쓰기 위해
    # 프로필 사진의 경로와 열린파일 핸들을 연관시켜주는 딕셔너리
    
    # 일반
    pictures = {}
    path = 'profile_1234.png'
    
    if (handle := pictures.get(path)) is None: # pictures에 경로가 없다면
        try:
            handle = open(path, 'a+b') # a+b 읽기 쓰기
        except OSError:
            print(f'경로를 열 수 없습니다: {path}')
            raise
        else:
            pictures[path] = handle
    
    handle.seek(0) # 파일안에서 포인터를 맨 앞으로 이동
    image_data = handle.read()
    
    # worse way1 - setdefault
    # setdefault와 open이 던지는 예외를 분리할 수 없음
    try:
        handle = pictures.setdefault(path, open(path, 'a+b'))
    except OSError:
        print(f'경로를 열 수 없습니다: {path}')
        raise
    else:
        handle.seek(0)
        image_data = handle.read()
    
    # worse way2 - defaultdict
    from collections import defaultdict
    
    def open_picture(profile_path):
        try:
            return open(profile_path, 'a+b')
        except OSError:
            print(f'경로를 열 수 없습니다: {profile_path}')
            raise
    
    # defaultdict의 첫번째 아규먼트는 callable 객체이거나 None이여야 한다
    pictures = defaultdict(open_picture) # callable 객체 전달
    handle = pictures[path] # openpicture에 파라미터를 전달하지 않아서 오류 발생
    handle.seek(0)
    image_data = handle.read()
    # TypeError: open_picture() missing 1 required positional argument: 'profile_path'
    
    # better way - __missing__
    class Pictures(dict): # dict 상속
        def __missing__(self, key):
            value = open_picture(key)
            self[key] = value
            return value
            
    pictures = Pictures()
    handle = pictures[path]
    handle.seek(0)
    image_data = handle.read()
    ```
    

## 추가

### 12장 - 동일성과 동등성

슬라이싱에서 시작과 끝 인덱스를 모두 생략한 리스트 복사 부분에서 나왔던 코드입니다.

```python
b = a[:]
assert b == a and b is not a
```

여기서 == 는 동등성(Equality)를 뜻하고 is 는 동일성(Identity)를 뜻합니다. 값만 동일하다면 동등성을 비교하면 되고 메모리 주소까지 동일하게 본다면 동일성을 확인하면 됩니다. 

### 12장 - 깊은 복사(deep copy)와 얕은 복사(shallow copy)

우선 깊은 복사는 참조된 객체 자체를 복사하는 것이고 얕은 복사는 원본 객체의 주소값을 복사하는 것입니다. 객체는 Mutable(변하는) 객체와 Immutable(불변하는) 객체가 있습니다. Mutable 객체로는  list, set, dict가 있고 Immutable한 객체로는 bool, str, int, float 등이 있습니다. 

mutable한 객체는 다른 변수에 할당시 주소값을 복사하기 때문에 원본 객체가 변경되면 함께 변경된다(얕은 복사)는 특징이 있는데요. 다음 코드를 통해 확인해 볼 수 있습니다. 

- mutable 객체

```python
>>> a = [1, 2, 3]
>>> b = a
>>> 
>>> a.append(4) # a값 변경
>>> a
[1, 2, 3, 4]
>>> b
[1, 2, 3, 4]
```

Mutable한 리스트 a에 4를 추가했더니 b에도 함께 추가된 것을 확인할 수 있습니다. 

- Immutable 객체

```python
>>> a = 1
>>> b = a  # a값 변경
>>>
>>> a = 4
>>> a
4
>>> b
1
```

a값이 변경되었지만 b의 값은 변경되지 않았습니다. 

### 15장 - OrderedDict의 필요성

dict도 순서를 보장한다면 OrderedDict는 언제 사용되는 것인지 궁금했습니다. 

확인해 보니 다음 3가지의 사항에 해당될 때 OrderedDict를 사용한다고 합니다.

1) 순서가 중요한 dict일 경우 명시적으로 알려주기 위해서

2) dict의 순서를 재배열하거나 정렬할 때 move_to_end()와 popitem() 메서드를 이용하는 것이 편할 때

```python
from collections import OrderedDict

order_dict1 = OrderedDict({"a":1, "b":2, "c":3})
order_dict1.move_to_end("b", last=False) # 맨 첫번째로 이동
# OrderedDict([('b', 2), ('a', 1), ('c', 3)])

order_dict1.move_to_end("b") # 마지막으로 이동
# OrderedDict([('a', 1), ('c', 3), ('b', 2)])

order_dict1.popitem() # 마지막 아이템 삭제
# OrderedDict([('a', 1), ('c', 3)])
```

3) dict의 순서를 포함한 동등성을 확인할 때

```python
dict1 = {"a":1, "b":2, "c":3}
dict2 = {"b":2, "a":1, "c":3}
assert dict1 == dict2

from collections import OrderedDict

order_dict1 = OrderedDict({"a":1, "b":2, "c":3})
order_dict2 = OrderedDict({"b":2, "a":1, "c":3})
assert order_dict1 == order_dict2 # AssertionError
```

### 18장 - 딕셔너리 자체 할당

- 아래처럼 pictures 딕셔너리에 open_picture 자체를 할당하면 어떻게 되는지 궁금해서 확인해 봤습니다.  pictures 딕셔너리에 open_picture 자체를 할당한다고해도 해당 path가 없으면 자동으로 해당 key를 생성해주고 있다면 해당 key에 파일을 넣어줄 것이라고 예상했기 때문입니다.
    
    ```python
    pictures[path] = open_picture(path)
    handle = pictures[path]
    handle.seek(0)
    image_data = handle.read()
    # {'profile_1234.png': <_io.BufferedRandom name='profile_1234.png'>}
    ```
    
- 예상대로 결과는 Pictures 클래스를 사용하여 딕셔너리를 생성한 다음 `__missing__`  메서드를 사용하여 파일을 핸들하는 방법과 동일한 결과를 얻을 수 있습니다.
- 그런데 위에처럼 open_picture 함수에서 파일을 열고 닫는 메소드를 호출하지 않았을 때 Pictures 클래스는 열린 파일을 재사용하고 pictures[path] 딕셔너리는 명시적으로 닫지 않는 이상 메모리에 남아있게 됩니다.
- 그래서 만약 파일을 여는 것에 리소스가 많이 들고 많은 파일을 여는 게 아니라면 일반 딕셔너리 할당 방법을 사용하고 파일을 열고 닫는데 오버헤드가 적으면서 동시에 여러 파일들을 다뤄야 한다면 클래스 재정의 방법을 사용하는게 효율적 입니다. (위와 같이 SNS의 프로필 사진을 관리한다면 클래서 재정의가 맞겠네요:>)
- 이 외에에도 클래스 재정의 방식은 확장성 측면에서의 이점도 있습니다.
    - 직접 테스트 해본 코드
        - 메모리 사용량 확인을 위해 psutil 라이브러리를 설치했습니다.(https://pypi.org/project/psutil/)
        - 아래 코드에서 반복 횟수를 10번 → 500,000번 이렇게 비교했습니다.
        
        ```python
        import os
        
        def open_picture(profile_path):
            try:
                return open(profile_path, 'a+b')
            except OSError:
                print(f'경로를 열 수 없습니다: {profile_path}')
                raise
        
        class Pictures(dict):
            def __missing__(self, key):
                value = open_picture(key)
                self[key] = value
                return value
        
        pictures = Pictures()
        
        # 여러 번 파일 핸들을 얻고 사용하는 시나리오
        for _ in range(500_000):
            handle = pictures['/Users/mac/Desktop/49fk01sh4d53wdqr4o6t.jpeg']
            handle.seek(0)
            image_data = handle.read()
            print(f'메모리 주소: {id(handle)}')
        
        # 메모리 사용량 확인
        import psutil
        
        process = psutil.Process(os.getpid())
        print(f'현재 프로세스 메모리 사용량: {process.memory_info().rss / (1024 * 1024):.2f} MB')
        
        import os
        import psutil
        
        def open_picture(profile_path):
            try:
                return open(profile_path, 'a+b')
            except OSError:
                print(f'경로를 열 수 없습니다: {profile_path}')
                raise
        
        # 딕셔너리를 직접 할당
        pictures_direct = {}
        path = '/Users/mac/Desktop/49fk01sh4d53wdqr4o6t.jpeg'
        
        # 여러 번 파일 핸들을 얻고 사용하는 시나리오
        for _ in range(500_000): 
            if path not in pictures_direct:
                try:
                    handle = open(path, 'a+b')
                    pictures_direct[path] = handle
                except OSError:
                    print(f'경로를 열 수 없습니다: {path}')
                    raise
            else:
                handle = pictures_direct[path]
            handle.seek(0)
            image_data = handle.read()
            print(f'메모리 주소: {id(handle)}, 이미지 데이터 길이: {len(image_data)}')
        
        # 메모리 사용량 확인
        process = psutil.Process(os.getpid())
        print(f'직접 할당한 딕셔너리 메모리 사용량: {process.memory_info().rss / (1024 * 1024):.2f} MB')
        ```
