# 4장 - 컴프리헨션과 제너레이터

### 27. map과 filter 대신 컴프리헨션을 사용하라

- 리스트컴프리헨션은 lambda식을 사용하지 않기 때문에 같은 일을 하는 map과 filter내장 함수를 사용하는 것보다 명확하다
    
    ```python
    # worse way
    a = [1, 2, 3, 4, 5, 6]
    squares = []
    for x in a:
    	squares.append(x**2)
    
    # better way
    squares = [x**2 for x in a]
    ```
    

### 28. 컴프리헨션 내부에 제어 하위 식을 세 개 이상 사용하자 말라

- 컴프리헨션 내부에서 제어 하위 식이 3개 이상인 경우에는 이해하기 어려우므로 가능하면 피해야한다.
    
    ```python
    # Good
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat = [x for row in matrix for x in row]
    print(flat) # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Bad
    my_list = [[[1, 2, 3], [4, 5, 6]]]
    flat = [x for sublist1 in my_list for sublist2 in sublist1 for x in sublist2]
    print(flat) # [1, 2, 3, 4, 5, 6]
    ```
    

### 29. 대입식을 사용해 컴프리헨션 안에서 반복 작업을 피하라

- 조건이 아닌 부분에 대입식을 사용하는건 회피해야 한다.
- 컴프리헨션 평가 순서로 인해 생기는 오류
    
    ```python
    # f 절은 for .. 과 변수 영역이 같은데 tenth는 for … 내부에서 정의하지 않아서 오류 발생
    result = {name: (tenth := count // 10)
    					for name, count in stock.items() if tenth > 0} # 오류
    
    # 대입식을 조건쪽으로 옮기고 대입식에서 만들어진 변수 이름을 컴프리헨션 값식에서 참조하여 해결
    result = {name: tenth for name, count in stock.items()
              if (tenth := count // 10) > 0}
    ```
    
- 루프 밖 변수 누출
    
    ```python
    # last 변수 사용
    half = [(last := count // 2) for count in stock.values()]
    print(f"{half}의 마지막 원소는 {last}") #[62, 17, 4, 12]의 마지막 원소는 12
    
    # 일반적인 for문에서 루프 변수 누출
    for count in stock.values():
       pass
    print(count) # 가능
    
    # 컴프리헨션에서는 불가능
    half = [count // 2 for count in stock.values()]
    print(count) # 불가능
    ```
    

### 30. 리스트를 반환하기보다는 제너레이터를 사용하라

- 제너레이터를 사용하면 작업 메모리에 모든 입력과 출력을 저장할 필요가 없으므로 입력이 아주 커도 출력 시퀀스를 만들 수 있다.

### 31. 인자에 대해 이터레이션할 때는 방어적이 돼라

- 제너레이터를 사용하여 이터레이션할 때 이미 StopIteration 예외가 발생한 이터레이터나 제너레이터를 다시 이터레이션하면 아무 결과도 얻을 수 없다.
    
    ```jsx
    def some_iter(data_path):
    	with open(data_path) as f:	
    		for line in f:
    			yield int(line)
    
    print(list(some_iter(path)) # [15, 30, 80]
    print(list(some_iter(path)) # []
    ```
    
- 이럴 때는 `이터레이터 프로토콜`을 구현한 새로운 컨테이너 클래스를 제공하여 사용하는게 좋다.
    - 이터레이터 프로토콜: 파이썬의 for 루프나 그와 연관된 식들이 컨테이너 타입의 내용을 방문할 때 사용하는 절차
    - 파이썬에서 이터레이터를 사용할 때 실제 내부에서 사용하는 iter, next 등 매직메소드로 구현되어있는데 이를 제너레이터로 구현하면 나만의 이터러블 객체 클래스를 정의할 수 있다.
    - 이방법의 단점은 입력데이터를 여러번 읽게 된다.

### 32. 긴 리스트 컴프리헨션보다는 제너레이터 식을 사용하라

- 제너레이터 식: 리스트 컴프리헨션과 제너레이터를 일반화 한 것
- 큰 입력 스트림에 대해 여러 기능을 합성해 적용해야 한다면 제너레이터 식을 사용하라

### 33. yield from을 사용해 여러 제너레이터를 합성하라

- yield from은 고급 제너레이터 기능으로 제어를 부모 제너레이터에게 전달하기 전에 내포된 제너레이터가 모든 값을 내보낸다.
- yield from은 파이썬 인터프리터가 사용자 대신 for 루프를 내포시키고 yield 식을 처리하도록 만든다.
- 직접 내포된 제너레이터를 이터레이션하면서 각 제너레이터의 출력을 내보내는 것보다 yield from을 사용하는 것이 성능면에서 더 좋다.

### 34. send로 제너레이터에 데이터를 주입하지 말라

- 파이썬 제너레이터는 send 메서드를 지원한다. 이 메서드는 yield식을 양향 채널로 만들어 준다.
- yield식에 도달하지 못하고 방금 시작한 제너레이터에는 None 밖에 전송하지 못한다.
- 여러 yield from 식을 선언한 복잡한 제너레이터에 send를 사용할 경우 부모 제너레이터가 자식 제너레이터로 옮겨갈 때마다 None이 출력되게 된다.
- 이러한 복잡성이 있기 때문에 send 사용보다는 합성할 제너레이터의 입력으로 이터레이터를 전달하는 방식을 사용하라

### 35. 제너레이터 안에서 throw로 상태를 변화시키지 말라

- 제너레이터 안에서 throw 가 호출되면 exception을 던지도록 할 수 있다.
- thorw 메서드를 사용하면 제너레이터가 마지막으로 실행한 yield 식의 위치에서 예외를 다시 발생시킬 수 있다.
    
    ```python
    class MyError(Exception):
    	pass
    
    def my_generator():
    	yield 1
    	yield 2
    	yield 3
    
    it = my_generator()
    print(next(it))
    print(next(it))
    print(it.throw(MyError('test error')))
    ```
    
- 하지만 throw를 사용하면 예외를 잡아내고 다시 발생시키는데 준비 코드가 필요하기 때문에 가독성이 나빠진다.
- 컨테이너 객체를 사용해 상태가 있는 클로저를 정의하는 방법으로 더 깔끔하게 사용 가능하다.
    - 비동기 기능을 사용하면 더 좋게 구현할 수 있는 경우가 많다.

### 36. 이터레이터나 제너레이터를 다룰 때는 itertools를 사용하라

1. 여러 이터레이터 연결하기
    - chain
        - 여러 이터레이터를 하나의 순차적인 이터레이터로 합치고 싶을 때
    - repeat
        - 한 값을 계속 반복해 내놓고 싶을 때(최대 횟수 지정 가능)
    - cycle
        - 이터레이터가 내놓는 원소들을 계속 반복하고 싶을 때
    - tee
        - 한 이터레이터를 병렬적으로 두 번째 인자로 지정된 개수의 이터레이터로 만들고 싶을 때
        - tee로 만들어진 이터레이터를 소비하는 속도가 같지 않으면 처리가 덜 된 이터레이터의 원소를 큐에 담아둬야 하므로 메모리 사용량이 늘어난다.
    - zip_longset
        - zip의 변종으로, 여러 이터레이터 중 짧은 이터레이터의 원소를 다 사용한 경우 fillvalue로 지정한 값을 채워준다,
2. 이터레이터에서 원소 거르기
    - islice
        - 이터레이터를 복사하지 않으면서 원소 인덱스를 이용해 슬라이싱 하고 싶을 때
        - islice의 동작은 시퀀스 슬라이싱이나 스트라이딩과 비슷하다.
    - takewhile
        - 이터레이터에서 주어진 술어(predicate)가 False를 반환하는 첫 원소가 나타날 때까지 원소를 돌려준다.
    - dropwhile
        - takewhile의 반대
        - 주어진 술어가 False를 반환하는 첫 번째 원소를 찾을 때까지 이터레이터의 원소를 건너뛴다.
    - filterfalse
        - filter 내장함수의 반대
        - 이터레이터에서 술어가 False를 반환하는 모든 원소를 돌려준다.
3. 이터레이터에서 원소의 조합 만들어내기
    - accumulate
        - 파라미터를 두 개 받는 함수(이항 함수)를 반복 적용하면서 이터레이터 원소를 값 하나로 줄여준다.I
        - accumulate가 반환하는 이터레이터는 원본 이터레이터의 각 원소에 대해 누적된 결과를 내놓는다.
    - product
        - 하나 이상의 이터레이터에 들어있는 아이템들의 데카르트 곱(Cartesian product)를 반환한다.
    - permutations
        - 이터레이터가 내놓는 원소들로부터 만들어낸 길이 N인 순열을 돌려준다.
    - combinations
        - 이터레이터 내놓는 원소들로부터 만들어낸 길이 N인 조합을 돌려준다.
    - combinations_with_replacement
        - combinations와 같지만 원소의 반복을 허용(중복조합 리턴)
