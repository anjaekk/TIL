# 6장-메타클래스와 애트리뷰트

*최소놀람의 법칙: 코드가 코드 읽는 사람을 놀라게 해는 안된다. 

### 44. 세터와 게터 메서드 대신 평범한 애트리뷰트를 사용하라

- 파이선에서는 게터와 세터 메서드를 구현할 필요가 없이 다음과 같이 공개 애트리뷰트로 구현하면 된다.
    
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

### 45. 애트리뷰트를 리팩터링하는 대신 @property를 사용하라

- @property를 사용하면 겉으로는 단순한 애트리뷰트처럼 보이지만 실제로는 지능적인 로직을 수행하는 애트리뷰트를 정의할 수 있다. (ex. 간단한 수치 애트리뷰트를 그때그때 요청에 따라 계산해 제공하도록 바꾸는 것)
- 리키버킷(leaky bucket) 흐름제어 알고리즘 예시
    - API 게이트 웨이에서 처리율 제한할 때등 사용하는 알고리즘
    - 가용 용량을 소비할 때마다 시간을 검사해서 주기가 달라질 경우에는 이전 주기에 미사용한 가용 용량이 새로운 주기로 넘어오지 못하게 막는다.
    
    ```jsx
    from datetime import datetime, timedelta
    
    class Bucket:
        def __init__(self, period):
            self.period_delta = timedelta(seconds=period) #처리율(지정된 시간당 몇개의 항목을 처리할지 지정하는 값)
            self.reset_time = datetime.now() # 주기 시작 시간
            self.quota = 0      # 현재 가용량
    
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
    
    ```jsx
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
        bucket = Bucket(60)
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
