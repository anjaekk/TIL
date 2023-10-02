### 37. 내장 타입을 여러 단계로 내포시키기보다는 클래스를 합성하라

- 딕셔너리, 긴 튜플, 다른 내장 타입이 복잡하게 내포된 데이터 값으로 사용하는 딕셔너리는 만들지 말라
- 완전한 클래스가 제공하는 유연성이 필요하지 않고 가벼운 불변데이터 컨테이너가 필요하면 namedtuple 타입을 고려하라
    - namedtuple에는 디폴트 인자 값을 지정할 수 없기 때문에 선택적인 property가 많은 데이터에 namedtuple을 사용하긴 어렵다. ⇒ 프로퍼티가 4~5개면 dataclasses 사용 권장
    - namedtuple의 인덱스로 값 접근과 이터레이션도 가능하므로 외부에 제공하는 API같은 경우 실제 클래스로 변경하기 어려울 수 있다.
- 내부 상태를 표현하는 딕셔너리가 복잡해지면 이 데이터를 관리하는 코드를 여러 클래스로 나눠서 재작성하라

### 38. 간단한 인터페이스의 경우 클래스 대신 함수를 받아라

- 함수는 클래스보다 정의하거나 기술하기가 더 쉬우므로 훅으로 사용하기엔 함수가 이상적이다.
    - 함수가 파이썬에서 일급 시민 객체(언어안에서 아무런 제약없이 사용할 수 있는 데이터 값)이기 때문에 훅으로 사용할 수 있음
- call 을 사용하면 객체를 함수처럼 호출할 수 있다.
    
    ```python
    
    class BetterCountMissing:
    	def __init__(self):
    		self.added = 0
    
    	def __call__(self):
    		self.added += 1
    		return 0
    
    counter = BetterCountMissing()
    result = defaultdict(counter, current) # callable한 counter
    ```
    
- 상태를 유지하기 위한 함수가 필요한 경우에는 상태가 있는 클로저를 정의하는 대신 call 메서드가 있는 클래스를 정의할지 고려하라

### 39. 객체를 제너릭하게 구성하려면 @classmethod를 통한 다형성을 활용하라

- 제네릭(Generic)
    - 파라미터 타입을 나중에 지정하게 되어 재활용성을 높일 수 있는 프로그래밍 스타일
- 파이썬에서는 객체뿐 아니라 클래스도 다형성을 지원한다.
- 아래와 같이 하위 클래스에서 다시 정의 해야만 사용 가능한 공통 클래스가 있을 때 아 클래스는 객체를 생성해 활용해야만 한다.
    
    ```python
    #InputData 상위 클래스
    class InputData:
        def read(self):
            raise NotImplementedError
    
    #InputData 하위 클래스
    class PathInputData(InputData):
        def __init__(self, path):
            super().__init__()
            self.path = path
    
        def read(self):
            with open(self.path) as f:
                return f.read()
    
    class Worker:
        def __init__(self, input_data):
            self.input_data = input_data
            self.result = None
        
        def map(self):
            raise NotImplementedError
        
        def reduce(self, other):
            raise NotImplementedError
    
    class LineCountWorker(Worker):
        def map(self):
            data = self.input_data.read()
            self.result = data.count('\n')
    
        def reduce(self, other):
            self.result += other.result
    ```
    
- 아래는 위의 클래스를 실행하고 멀티 쓰레드를 사용하도록 추가한다.
    
    ```python
    # input 값들 받아서 객체 만드는 도우미 함수
    import os
    
    def generate_inputs(data_dir):
        for name in os.listdir(data_dir):
            yield PathInputData(os.path.join(data_dir, name))
    
    def create_workers(input_list):
        workers = []
        for input_data in input_list:
            workers.append(LineCountWorker(input_data))
        return workers
    
    # 멀티쓰레드
    form threading import Thread
    
    def execute(workers):
        threads = [Thread(target=w.map) for w in workers]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        
        first, *rest = workers
        for worker in rest:
            first.reduce(worker)
        return first.result
    
    # 실행
    def mapreduce(data_dir):
        inputs = generate_inputs(data_dir)
        workers = create_workers(inputs)
        return execute(workers)
    ```
    
    - 정상작동
- 하지만 위의 함수는 제네릭하지 않다. (다른 InputData나 Worker 하위 클래스를 사용하고 싶다면 각각의 gerate_inputs, create_workers, mapreduce를 재정의 해줘야 한다.
- 다른 언어에서는 이를 해결하기위해 특별 생성자들을 사용해서 해결하지만 파이썬에서 생성자는 init밖에 없기 때문에 클래스 메서드로 다형성을 사용한다.
    
    ```python
    class GenericInputData:
        def read(self):
            raise NotImplementedError
        
        @classmethod
        def generate_inputs(cls, config):
            raise NotImplementedError
    
    class PathInputData(GenericInputData):
        ...
        
        @classmethod
        def generate_inputs(cls, config):
            data_dir = config['data_dir']
            for name in os.listdir(data_dir):
                yield cls(os.path.join(data_dir, name))
    
    class GenericWorker:
        def __init__(self, input_data):
            self.input_data = input_data
            self.result = None
        
        def map(self):
            raise NotImplementedError
        
        def reduce(self, other):
            raise NotImplementedError
        
        @classmethod
        def crate_workers(cls, input_class, config):
            workers = []
            for input_data in input_class.generate_inputs(config):
                workers.append(cls(input_data))
            return workers
    
    #LineCountWorker 선언할때 상위 클래스를 GenericWorker로 지정
    class LineCountWorker(GenericWorker):
        ...
    ```
    
    - 완전한 제너릭 함수
- @classmethod를 사용해 클래스에 다른 생성자를 정의할 수 있다.

### 40. super로 부모 클래스를 초기화하라-super, MRO

- 자식클래스에서 부모 클래스를 초기화할 때 보통 init__ 메서드를 사용하지만 다중 상속일 경우 예측할 수 없는 방식으로 동작할 수 있다.
    - 다중상속에서 하위클래스의 init__호출순서가 정해져 있지 않기 떄문에
- 다이아몬드 상속이 이루어지면 공통 조상 클래스의 init__ 메서드가 여러번 호출될 수 있기 때문에 코드를 예측할 수 없다.
    - 다이아몬드 상속: 어떤 클래스가 두 가지 서로 다른 클래스를 상속하는데, 두 상위 클래스의 상속 계층에 같은 조상 클래스가 존재하는 경우
- 이 문제 해결을 위해 파이썬에서는 super와 표준 메서드 결정순서(MRO; Method Resolution Order)가 있다.
    - super: 다이아몬드 계층의 공통 상위 클래스를 한번만 호출하도록 보장한다.
    - MRO: 상위 클래스를  초기화하는 순서를 정의한다.
        - C3 선형화(Linearization) 알고리즘 사용
    - 호출 순서는 이 클래스에 대한 MRO 정의를 따른다. MRO 순서는 `mro`라는 클래스 메서드를 통해 살펴볼 수 있다.
        
        ```python
        mro_str = '\n'.join(repr(cls) for cls in GoodWay.mro())
        
        >>>
        <class '__main__.GoodWay'> # 4
        <class '__main__.TimesSevenCorrect'> # 3
        <class '__main__.PlusNineCorrect'> # 2
        <class '__main__.MyBaseClass'> # 1
        <class 'object'>
        ```
        
- super 함수의 두가지 인자
    - 첫번째 파라미터: MRO 뷰를 제공할 부모 타입
    - 두번째 파라미터: 첫 번째 파라미터로 지정한 타입의 MRO 뷰에 접근할 때 사용할 인스턴스

### 41. 기능을 합성할 때는 믹스인 클래스를 사용하라

- 믹스인의 가장 큰 장점은 제네릭 기능을 쉽게 연결할 수 있고 필요할 때 기존 기능을 다른 기능으로 오버라이드(override)해 변경할 수 있다는 것이다.
- 믹스인을 사용해 구현할 수 있는 기능을 인스턴스 애트리뷰트와 init__ 을 사용하는 다중 상속을 통해 구현하지 말라
- 믹스인 클래스가 클래스 별로 특화된 기능을 필요로 한다면 인스턴스 수준에서 끼워넣을 수 있는 기능을 활용하라
- 믹스인에는 필요에 따라 인스턴스 메서드는 물론 클래스메서드도 포함할 수 있다.
- 믹스인을 합성하면 단순한 동작으로부터 더 복잡한 기능을 만들어 낼 수 있다.

### 42. 비공개 애트리뷰트보다는 공개 애트리뷰트를 사용하라

- 파이썬 컴파일러는 비공개 애트리뷰트를 자식 클래스나 클래스 외부에서 사용하지 못하도록 엄격히 금지하지 않는다.
- 비공개 애트리뷰트로 접근을 막으려고 시도하기보다는 보호된 필드를 사용하면서 문서에 적절한 가이드를 남겨라
- 코드 작성을 제어할 수 없는 클래스에서 이름 충돌이 일어나는 경우를 막고 싶을 때만 비공개 애트리뷰트를 사용할 것을 권한다.

### 43. 커스텀 컨테이너 타입은 collections.abc를 상속하라

- 간편하게 사용할 경우에는 파이썬 컨테이너타입(리스트나 딕셔너리 등)을 직접 상속하라
- 커스텀 컨테이너를 제대로 구현혀려면 수많은 메서드를 구현해야 한다.
- 커스텀 컨테이너 타입이 [collections.abc](http://collections.abc)에 정의된 인터페이스를 상속하면 컨테이너 타입이 정상적으로 작동하기 위해 필요한 인터페이스와 기능을 제대로 구현하도록 보장할 수 있다.
