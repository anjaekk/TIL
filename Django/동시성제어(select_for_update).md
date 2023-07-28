## 옵션

### nowait

- False는 해당 row가 lock이 잡혀있으면 대기, True는 `django.db.utils.OperationalError: could not obtain lock on row in relation` 에러 발생(default: False)

### skip_locked

- False는 locked가 걸려 있을 경우 이를 기다리고 True는 조회한 row가 lock이 걸려있을 경우 이를 무시한다. (default: False)

```python
skip_locked와 nowait은 상호 배타적이라 두 옵선을 모두 활성화 하면 ValueError가 발생한다.
```

### of

기본적으로 select_for_update는 쿼리에서 선택한 행을 모두 잠그게 된다. 만약 select_related()를 함께 사용해서 조회를 하게되면 해당 행들을 모두 locking하게 되는데 이때 of 옵션을 통해 조회는 selected_related로 하되, locking은 특정 모델만 하도록 지정할 수 있다. 

상위 모델을 locking하기 위해서는 “<부모 모델 이름>_ptr” 로 자정하여 사용하면 된다.

```python
Restaurant.objects.select_for_update(of=("self", "place_ptr"))
```

## Select_for_update 작동 확인

원 진행자 A, 후발 간섭자 B가 있을 때 A가 먼저 같은 table의 row를 변경하고 save전 대기시 B를 실행 한다고 가정 시 어떻게 진행되는지 확인

<wallet의 기존 값은 10으로 가정>

### 1. A = select_for_update사용, B = 단순 update

- A코드 + 3
    
    ```python
    import time
    from django.db import transaction
    from account.models import Wallet
    
    with transaction.atomic(using='default'):
        wallet = Wallet.objects.select_for_update(nowait=False).get(user_id=1)
        print(f"A started amount = {wallet.amount}") # 10
        wallet.amount += 3
        time.sleep(15)
        wallet.save()
        print(f"A finished amount = {wallet.amount}") # 13
    ```
    

- B코드 - 10
    
    ```python
    from account.models import Wallet
    
    wallet = Wallet.objects.get(user_id=1)
    print(f"B started amount = {wallet.amount}") # 10
    wallet.amount -= 10
    wallet.save()
    print(f"B finished amount = {wallet.amount}") # 0
    ```
    

- 결과
    
    A와 B의 결과가 상이하게 나온다. 하지만 다시 django get으로 조회해보면 B에 맞는 값인 0으로 나오게 된다.  15초 뒤에 증가한 3은 적용되지 않았다.
    

### 2. A = 단순 update, B = select_for_update 사용

- A코드
    
    ```python
    import time
    from account.models import Wallet
    
    wallet = Wallet.objects.get(user_id=1)
    print(f"A started amount = {wallet.amount}") # 10
    wallet.amount += 3
    time.sleep(15)
    wallet.save()
    print(f"A finished amount = {wallet.amount}") # 13
    ```
    

- B코드
    
    ```python
    import time
    from django.db import transaction
    from account.models import Wallet
    
    with transaction.atomic(using='default'):
        wallet = Wallet.objects.select_for_update(nowait=False).get(user_id=1)
        print(f"B started amount = {wallet.amount}") # 10
        wallet.amount -= 10
        wallet.save()
        print(f"B finished amount = {wallet.amount}") # 0
    ```
    

- 결과
    
    이 경우도 결과가 상이하게 나오고 결과를 검색해보면 A애 맞는 값인 13으로 나온다
    

### 3. A = select_for_update, B = select_for_update 사용

- A코드
    
    ```python
    import time
    from django.db import transaction
    from account.models import Wallet
    
    with transaction.atomic(using='default'):
        wallet = Wallet.objects.select_for_update(nowait=False).get(user_id=1)
        print(f"A started amount = {wallet.amount}") # 10
        wallet.amount += 3
        time.sleep(15)
        wallet.save()
        print(f"A finished amount = {wallet.amount}") # 13
    ```
    

- B코드
    
    ```python
    import time
    from django.db import transaction
    from account.models import Wallet
    
    with transaction.atomic(using='default'):
        wallet = Wallet.objects.select_for_update(nowait=False).get(user_id=1)
        print(f"B started amount = {wallet.amount}") # 13
        wallet.amount -= 10
        wallet.save()
        print(f"B finished amount = {wallet.amount}") # 3
    ```
    

- 결과
    
    B의 시작 값이 A의 저장 전 값으로 가져온다. 결과적으로는 A와 B가 모두 반영된 값으로 최종 값은 3이 된다. 
    

### 4. A = 단순 업데이트, B = 단순 업데이트

- A코드
    
    ```python
    import time
    from account.models import Wallet
    
    wallet = Wallet.objects.get(user_id=1)
    print(f"A started amount = {wallet.amount}") # 10
    wallet.amount += 3
    time.sleep(15)
    wallet.save()
    print(f"A finished amount = {wallet.amount}") # 13
    ```
    

- B코드
    
    ```python
    from account.models import Wallet
    
    wallet = Wallet.objects.get(user_id=1)
    print(f"B started amount = {wallet.amount}") # 10
    wallet.amount -= 10
    wallet.save()
    print(f"B finished amount = {wallet.amount}") # 0
    ```
    

- 결과
    
    마지막으로 저장된 13으로 조회가 된다. 
    

## 결론

동시성 제어를 위해 row lock을 걸게된다면 해당 row를 참조하여 변경하는 row가 모두 select_for_update로 제어가 걸려있어야 한다. 일부만 select_for_update로 변경시 select_for_update로 하지 않는 업데이트에 의해서 의도한 결과를 반영하지 못하게 된다. 

### 주의할 점

1. select_for_update는 transaction 내부에서만 사용 가능하다
    
    `transaction.atomic`
    
    - 에러 메세지
    
    ```python
    django.db.transaction.TransactionManagementError: select_for_update cannot be used outside of a transaction.
    ```
