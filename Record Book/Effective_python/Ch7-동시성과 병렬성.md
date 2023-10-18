# 7장-동시성과 병렬성

- 동시성(concurrency): 같은 시간에 여러 작업을 처리하는 것처럼 보이는 것
- 병렬성(paralleism): 같은 시간에 여러 다른 작업을 실제로 처리하는 것
- 병렬적인 프로그램은 항상 동시성 프로그램이지만 동시성 프로그램이 반드시 병렬적인 프로그램은 아니다.
- 파이썬을 이용하면 동시성 프로그램을 쉽게 작성할 수 있다.
- 스레드는 상대적으로 적은 양의 동시성을 제공하지만 코루틴은 수많은 동시성 함수를 상용할 수 있게 해준다.
- 파이썬은 시스템콜(system call), 하위 프로세스(subprocess), C확장(extension)을 사용해 작업을 병렬로 수행할 수 있다.

### 52. 자식 프로세스를 관리하기 위해 subprocess를 사용하라

- 파이썬이 하위 프로세스를 실행하는 방법은 많지만(ex: os.popen, os.exec* 등) 자식프로세스를 관리할 때는 subprocess 내장 모듈을 사용하는 것이 가장 좋다.
- run: 간단하게 자식 프로세스를 실행하고 싶은 경우
- Popen: 유닉스 스타일의 파이프라인이 필요시
    - run함수를 사용해 프로세스를 시작하고 프로세스 출력을 읽고 오류없이 깔끔하게 종료됐는지 검사하는 코드
    
    ```python
    import subprocess
    
    result = subprocess.run(['echo', '자식 프로세스에서 출력한 메시지'],
                         capture_output=True, encoding='utf-8')
    
    result.check_returncode() # 예외가 발생하지 않으면 성공
    print(result.stdout) # 자식 프로세스에서 출력한 메시지 
    ```
    
    - `subprocess`등의 모듈을 통해 시행한 자식 프로세스는 부모 프로세스인 파이썬 인터프리터와 독립적으로 실행된다.
    - `run` 대신 `Popen` 클래스를 사용해 주기적으로 자식 프로세스의 상태를 검사할수 있다. (polling)
    
    ```python
    proc = subprocess.Popen(['sleep', '1'])
    while proc.poll() is None:
        print('작업 중...')
        # CPU를 많이 사용하는 작업을 수행한다.
        # ...
    
    print('종료 상태', proc.poll())
    
    >>> 작업 중...
    >>> 작업 중...
    >>> 작업 중...
    >>> 종료 상태 0
    ```
    
    - Popen 작업을 리스트에 넣고 for문을 동해 communicate()를 실행하여 원하는 개수만큼 많은 자식 프로세스를 병렬로 실행할 수 있다.
    
    ```python
    import time
    
    start = time.time()
    time.sleep(1)
    sleep_procs = []
    for _ in range(10):
        proc = subprocess.Popen(['sleep', '1'])
        sleep_procs.append(proc)
    
    for proc in sleep_procs:
        proc.communicate()
    
    end = time.time()
    delta = end - start
    print(f'총 {delta:.3} 초 만에 끝남.')
    
    >>> 총 1.04 초 만에 끝남.
    # 병렬적으로 실행했기 때문에 10초 이상이 걸리지 않고 1.04초만에 끝남
    ```
    
    - Pipe를 사용해 하위 프로세스로 보내거나 하위 프로세스의 출력을 받을 수 있다.
    
    ```python
    import os
    
    def run_encrypt(data):
        env = os.environ.copy()
        env['password'] = 'zf7Shy'
        proc = subprocess.Popen(
            ['openssl', 'enc', '-des3', '-pass', 'env:password'],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        proc.stdin.write(data)
        proc.stdin.flush() # 자식이 입력을 받도록 보장
        return proc
    
    # 리스트에 작업 목록 추가
    procs = []
    for _ in range(3):
        data = os.urandom(10)
        proc = run_encrypt(data) # 데이터 입력
        procs.append(proc)
    
    for proc in procs:
        out, _ = proc.communicate() # 병렬로 자식프로세스에서 실행 및 결과 받음
        print(out[-10:]) # 암호화된 바이트 문자열 출력
    
    >>> b'\x1c\x8b\x1f\x1c\x1c\x1c\x1c\x1c\x1c\x1c'
    ```
    
    - 실전에서는 파이프를 통해 사용자입력, 파일 핸들, 네트워크 소켓등에서 받은 대이터 암호화 가능
    - 유닉스 파이프라인처럼 한 자식 프로세스의 출력을 다음 프로세스의 입력으로 연결시켜 여러 병렬 프로세스를 연쇄적으로 사용 가능하다.
    - openssl 명령줄 도구를 하위 프로세스로 만들어서 입력 스트림의 월풀(whirlpool) 해시 계산
    
    ```python
    def run_hash(input_stdin):
        return subprocess.Popen(
            ['openssl', 'dgst', '-whirlpool', '-binary'],
            stdin=input_stdin,
            stdout=subprocess.PIPE)
    
    encrypt_procs = []
    hash_procs = []
    for _ in range(3):
        data = os.urandom(100)
        
    		# 표준 출력이 다음 프로세스로 잘 전달될 수 있도록 보장
        encrypt_proc = run_encrypt(data)
        encrypt_procs.append(encrypt_proc)
        
        hash_proc = run_hash(encrypt_proc.stdout)
        hash_procs.append(hash_proc)
    
        encrypt_proc.stdout.close() 
    		# close()가 없으면 파이프라인이 끊어지지 않아서 SIGPIPE가 발생하지 않음
        encrypt_proc.stdout = None
    
    for proc in encrypt_procs:
        proc.communicate()
        assert proc.returncode == 0
    
    for proc in hash_procs:
        out, _ = proc.communicate()
        print(out[-10:])
    
    assert proc.returncode == 0
    ```
    
    - 선행되는 자식 프로세스가 끝나지 않아서 다음 프로세스가 파이프를 기다리며 블록이 된다면 timeout값을 전달하면 된다. (시간이 지나면 예외 발생)
    
    ```python
    proc = subprocess.Popen(['sleep', '10'])
    try:
        proc.communicate(timeout=0.1)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait()
    
    print('종료 상태', proc.poll())
    ```
    

### 53. 블로킹 I/O의 경우 스레드를 사용하고 병렬성을 피하라

### GIL

- Cpython의 실행단계
    1. 소스코드를 분석해서 바이트코드로 변환한다. (3.6 이상부터는 16비트 명령어를 사용해서 워드코드라고 불러야하지만 보통 바이트코드라고 부름)
    2. 바이트코드를 스택 기반 인터프리터를 통해 실행한다. 
- 바이트코드 인터프리터에는 파이썬 프로그램이 실행되는 동안 일관성있게 유지해야 하는 상태가 존재하는데 이를 Cpython에서는 전역 인터프리터 락(Global Interpreter Lock, GIL)을 이용해 일관성을 강제로 유지한다.

### GIL의 존재 이유

- 근본적으로 GIL은 상호배제락(mutual exclusion lock)(뮤텍스) 이며, Cpython이 선점형(preemptive) 멀티스레드로 인해 영향을 받는 것을 방지한다.
- 선점형 멀티스레드에서는 한 스레드가 다른 스레드의 실행을 중간에 인터럽트 시키고 제어를 가져올 수 있다.
- 이런 인터럽트가 예기치 못하게 발생시 인터프리터의 상태가 오염될 수 있다. (GC의 참조 카운팅 등)
- GIL은 인터럽트가 함부로 발생하는 것을 방지해 인터프리터 상태가 제대로 유지되고 바이트코드 명령들이 제대로 실행되도록 만든다.

### 파이썬의 멀티스레드

- 파이썬도 다중 실행 스레드를 지원하지만, GIL로 인해 여러 스레드 중 어느 하나만 앞으로 진행할 수 있다.
- 계산량이 매우 많은 작업은 스레드 생성과 스레드 실행 조정에 따른 부가 비용이 들어서 스레드를 하나만 썼을 때보다 시간이 더 오래걸릴 수 있다. (GIL로 인해(Lock 충돌과 스케줄링 부가비용)
- Cpython에서도 concurrent.futures를 사용하면 다중 코어를 사용할 수 있다.
- 이런 한계에도 파이썬이 스레드를 지원하는 이유
    1. GIL로 인해 스레드 중 하나만 앞으로 진행할 수 있음에도 Cpython이 어느정도 균일하게 각 스레드를 실행시켜주므로 다중 스레드를 통해 여러 함수를 동시에 실행할 수 있다. 
    2. 블로킹 I/O를 다루기 위해서다. 
        - 블로킹 i/O는 파이썬이 특정 시스템 콜을 사용할 때 일어난다. (파이썬 프로그램은 시스템 콜을 사용해 컴퓨터 운영체제가 자기 대신 외부 환경과 상호작용하도록 의뢰한다. )파일 읽기, 쓰기, 네트워크와 상호작용하기, 디스플레이 장치와 통신하기 등 작업
        - 코드를 가급적 손보지 않고 블로킹 i/O를 병렬로 실행하고 싶을 때 스레드를 사용하는 것이 가장 간편하다.

### 54. 스레드에서 데이터 경합을 피하기 위해 Lock를 사용하라

- 파이썬 인터프리터에서 어떤 스레드가 데이터 구조에 대해 한 번에 단 하나만 실행될 수 있지만, 파이썬 인터프리터에서 어떤 스레드가 데이터 구조에 대해 수행하는 연산은 연속된 두 바이트 코드 사이에서 언제든 인터럽트 될 수 있다. (GIL은 동시접근을 보장하는 Lock 역할을 하지 못한다. )
