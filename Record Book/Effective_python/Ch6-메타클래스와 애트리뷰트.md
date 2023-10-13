# 6장-메타클래스와 애트리뷰트

*최소놀람의 법칙: 코드가 코드 읽는 사람을 놀라게 해는 안된다. 

### 44. 세터와 게터 메서드 대신 평범한 애트리뷰트를 사용하라

- 파이선에서는 게터와 세터 메서드를 구현할 필요가 없이 다음과 같이 공개 애트리뷰트로 구현하면 된다.
    - 파이써닉 하지 않은 코드
        
        ```python
        class OldResistor:
            def __init__(self, ohms):
                self._ohms = ohms
                
            def get_ohms(self):
                return self._ohms
                
            def set_ohms(self, ohms):
                self._ohms = ohms
        ```
        
        - 수정(공개 애트리뷰트)
        
        ```jsx
        class Resistor:
        	def __init__(self, ohms):
        		self.ohms = ohms
        		self.voltage = 0
        		self.current = 0
        
        r1 = Resistor(50e3)
        r1.ohms = 10e3
        ```
        
- 게터나 세터를 정의할 때 가장 좋은 정책은 관련이 있는 객체 상태를 @property.setter 메서드 안에서만 변경하는 것이다.
- @property의 단점은 애트리뷰트를 처리하는 메서드가 하위 클래스 사이에서만 공유될 수 있다는 것이다. (서로 관련이 없는 클래스 사이에 같은 프로퍼티 게터나 세터 구현을 공유할 수 없다.
- 파이썬에서는 재사용 가능한 프로퍼티 로직을 구현할 때처럼 다른 용도에도 사용할 수 있는 디스크립터를 제공한다.
- @property 메서드를 만들 때는 최소 놀람의 법칙을 따르고 이상한 부작용을 만들어내지 말라.
    
    ```python
    class MysteriousResistor(Resistor):
        @property
        def ohms(self):
            self.voltage = self._ohms * self.current
            return self._ohms
            
        @ohms.setter
        def ohms(self, ohms):
            self._ohms = ohms
    
    r7 = MysteriousResistor(10)
    r7.current = 0.01
    print(f'이전: {r7.voltage:.2f}') # 이전: 0.00
    r7.ohms
    print(f'이후: {r7.voltage:.2f}') # 이후: 0.10
    ```
    
- @property 메서드가 빠르게 실행되도록 유지하라. 느리거나 복잡한 작업의 경우(특히 I/O를 수행하는 등의 부수 효과가 있는 경우)에는 프로퍼티 대신 일반적인 메서드를 사용하라.

### 45. 애트리뷰트를 리팩터링하는 대신 @property를 사용하라

- @property를 사용하면 겉으로는 단순한 애트리뷰트처럼 보이지만 실제로는 지능적인 로직을 수행하는 애트리뷰트를 정의할 수 있다. (ex. 간단한 수치 애트리뷰트를 그때그때 요청에 따라 계산해 제공하도록 바꾸는 것)
- 리키버킷(leaky bucket) 흐름제어 알고리즘 예시
    - API 게이트웨이에서 처리율 제한할 때등 사용하는 알고리즘
    - 가용 용량을 소비할 때마다 시간을 검사해서 주기가 달라질 경우에는 이전 주기에 미사용한 가용 용량이 새로운 주기로 넘어오지 못하게 막는다.
    
    ```python
    from datetime import datetime, timedelta
    
    class Bucket:
        def __init__(self, period):
            self.period_delta = timedelta(seconds=period) #처리율(지정된 시간당 몇개의 항목을 처리할지 지정하는 값)
            self.reset_time = datetime.now() # 주기 시작 시간
            self.quota = 0 # 현재 가용량
    
        def __repr__(self):
            return f'Bucket(quota={self.quotat})'
    
    def fill(bucket, amount):
    """도우미 함수: 용량을 채운다."""
        now = datetime.now()
    		# 현재 시간 - 주기 시작 시간 > 지정해놓은 주기
        if (now - bucket.reset_time) > bucket.period_delta: 
            bucket.quota = 0 # 가용용량 초기화
            bucket.reset_time = now # 주기 초기화
        bucket.quota += amount # 버킷에 가용용량을 할당량(amount)만큼 채워 넣는다.
    
    def deduct(bucket, amount):
    """도우미 함수: 용량을 사용한다."""
        now = datetime.now()
        if (now - bucket.reset_time) > bucket.period_delta:
            return False    # 새 주기가 시작됐는데 아직 버킷 할당량이 재설정되지 않았다.
        if bucket.quota - amount < 0:
            return False    # 용량 부족
        else:
            bucket.quota -= amount
            return True     # 용량 사용 가능
    ```
    
    - 사용
    
    ```python
    bucket = Bucket(60)
    fill(bucket, 100)       
    print(bucket) # quota = 100
    
    # 용량 사용
    deduct(bucket, 99) # True
    print(bucket) # quota = 1
    
    # 가용량 이상 사용
    deduct(bucket, 3) # False
    print(bucket) # quota = 1 (동일)
    ```
    
    - 구현의 문제점
        - 버킷이 시작할 때 가용 용량이 얼마인지 알수 없음
        - deduct 에서 False 반환시 1. bucket에 할당된 가용 용량을 소진했기 때문인지 2. 새로 시작한 주기에서 가용 용량을 추기받지 못했기 때문인지 알 수 없다.
    
    - 가용 용량(max_quota)와 소비용량의 합계(quota_consumed)를 추적하도록 변경
    - fill과 deduct 도우미 함수는 그대로 사용
        
        ```python
        class NewBucket:
            def __init__(self, period):
                self.period_delta = timedelta(seconds=period)
                self.reset_time = datetime.now()
                self.max_quota = 0  # 가용 용량
                self.quota_consumed = 0  # 누적 소비 용량
        
            def __repr__(self):
                return f'NewBucket(max_quota={self.max_quota}, ' 
        							 f'consumed={self.quota_consumed})')
        
        		@property
            def quota(self):
        		"""현재 가용 용량"""
                return self.max_quota - self.quota_consumed
        
        		@quota.setter
            def quota(self, amount):
                delta = self.max_quota - amount
                if amount == 0: # 초기화
                    self.quota_consumed = 0
                    self.max_quota = 0
                elif delta < 0: # 새로운 주기 시작시 가용 용량 추가
                    assert self.quota_consumed == 0
                    self.max_quota = amount
                else:  # 용량 소비시
                    assert self.max_quota >= self.quota_consumed
                    self.quota_consumed += delta
        
        ```
        
    - 사용
        
        ```python
        # 최초
        bucket = NewBucket(60)
        print(bucket) # max_quota=0, quota_consumed=0
        
        # 용량 보충
        fill(bucket, 100)       
        print(bucket) # max_quota=100, quota_consumed=0
        
        # 용량 사용
        deduct(bucket, 99) # True
        print(bucket) # max_quota=100, quota_consumed=99
        
        # 가용량 이상 사용
        deduct(bucket, 3) # False
        print(bucket) # max_quota=100, quota_consumed=99
        ```
        
        - property 사용 장점
            - bucket.quota를 사용하는 코드를 변경할 필요 없음
            - 이 클래스 구현이 변경됐음을 알 필요가 없음
- @property를 너무 과하게 쓰고 있다면 클래스와 클래스를 사용하는 모든 코드 리팩터링을 고려하라

### 46. 재사용 가능한 @property 메서드를 만들려면 디스크립터를 사용하라

- @property의 가장 큰 문제점은 재사용성이다.
    - @property가 데코레이션하는 메서드를 같은 클래스에 속하는 여러 애트리뷰트로 사용할 수 없다.
    - 서로 무관한 클래스 사이에서 @property 데코레이터를 적용한 메서드를 재사용할 수 없다.
    - 점수가 0~100 사이의 값인지 확인하는 클래스
        
        ```python
        class Exam:
            def __init__(self):
                self._writing_grade = 0
                self._math_grade = 0
            
        
            @staticmethod
            def _check_grade(value):
                if not (0 <= value <= 100):
                    raise ValueError("점수는 0과 100 사이입니다.")
        
            @property
            def writing_grade(self):
                return self._writing_grade
            
        
            @writing_grade.setter
            def writing_grade(self, value):
                self._check_grade(value)
                self._writing_grade = value
            
        
            @property
            def math_grade(self):
                return self._math_grade
            
        
            @math_grade.setter
            def math_grade(self, value):
                self._check_grade(value)
                self._math_grade = value
        ```
        
        - 문제점: 시험 과목이 늘어날 때마다 @property와 setter 메서드를 생성해야 한다.
- 디스크립터 프로토콜
    - 파이썬 언어에서 애트리뷰트 접근을 해석하는 방법 정의
    - 디스크립터 클래스는 `__getter__` 와 `__setter__` 메서드를 제공한다.
    - 디스크립터 프로토콜을 구현한 Grade 클래스
        
        ```python
        class Grade:
            def __get__(self, instance, instance_type):
                ...
        
            def __set__(self, instance, value):
                ...
        
        class Exam:
        		# 클래스 애트리뷰트들
            math_grade = Grade()
            writing_grade = Grade()
            science_grade = Grade()
        ```
        
        - `__getattribute__` 메서드로 인해 Exam 인스턴스에 writing_grade라는 이름의 애트리뷰트가 없으면 파이썬은 Exam 클래스의 애트리뷰트를 대신 사용한다.
        
        ```python
        exam = Exam()
        
        # set
        exam.writing_grade = 40 
        # Exam.__dict__['writing_grade'].__set__(exam, 40)
        
        # get
        exam.writing_grade
        # Exam.__dict__['writing_grade'].__get__(exam, Exam)
        ```
        
        - Grade 선언
        
        ```python
        class Grade:
            def __init__(self):
                self._value = 0
        
            def __get__(self, instance, instance_type):
                return self._value
        
            def __set__(self, instance, value):
                if not (0 <= value <= 100):
                    raise ValueError("점수는 0과 100 사이입니다")
                self._value = value
        ```
        
        - 첫번째 시험
        
        ```css
        class Exam:
            math_grade = Grade()
            writing_grade = Grade()
            science_grade = Grade()
        
        first_exam = Exam()
        first_exam.math_grade = 80
        
        print(first_exam.math_grade) # 80
        ```
        
        - 두번째 시험
        
        ```css
        second_exam = Exam()
        second_exam.math_grade = 90
        
        print(first_exam.math_grade) # 90 -> 틀림(80이여야 함)
        print(second_exam.math_grade) # 90
        ```
        
        - 문제점
            - math_grade를 클래스 애트리뷰트로 한 Grade 인스턴스를 모든 Exam 인스턴스가 공유한다.
    - 인스턴스별 상태를 딕셔너리로 관리
        
        ```python
        class Grade:
            def __init__(self):
                self._values = {}
        
            def __get__(self, instance, instance_type):
                if instance is None:
                    return self
                return self._values.get(instance, 0) # 생성할때마다 딕셔너리에 저장한다. 
        
            def __set__(self, instance, value):
                if not (0 <= value <= 100):
                    raise ValueError(
                        '점수는 0과 100 사이입니다')
                self._values[instance] = value
        ```
        
        - 문제점: 프로그램이 실행되는 동안 `__setter__` 호출에 전달된 모든 Exam 인스턴스에 대한 레퍼런스 카운팅이 절대로 0이 될 수 없기 때문에 GC가 메모리를 재활용할 수 없다.
    - weakref 내장모듈을 이용한 약한참조 저장
        
        ```python
        from weakref import WeakKeyDictionary
        
        class Grade:
            def __init__(self):
                self._values = WeakKeyDictionary() # 약한참조 딕셔너리 사용
        
            def __get__(self, instance, instance_type):
                if instance is None:
                    return self
                return self._values.get(instance, 0)
        
            def __set__(self, instance, value):
                if not (0 <= value <= 100):
                    raise ValueError(
                        '점수는 0과 100 사이입니다')
                self._values[instance] = value
        ```
        
        - 해당 weakKeyDictionary의 강한참조를 모두 사용하면 GC가 해당 메모리를 재활용한다.

- python 약한참조, 강한참조
    - 약한참조: 참조 수를 올리지 않아서 GC에서 매번 제거
    - 강함참조: 참조 수가 0이 되거나 메모리에서 해제될 때 제거
