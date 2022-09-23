[ 결론 ] 

1. CPU 바운드 => Multi Processing
2. I/O 바운드, 빠른 I/O, 제한된 연결 수 => Multi Threading
3. I/O 바운드, 느린 I/O, 많은 연결 => Asyncio

[ 바운드의 종류 ]

1. CPU 바운드
    
    프로그램이 실행될 때 실행 속도가 CPU 속도에 의해 제한됨(= 프로그램이 실행될 때 CPU 때문에 느려질 수 있음). 이유는 CPU의 계산 때문인데 정말 복잡한 수학을 계산하게되면 실행속도는 더 느려질 것이다.
    
2. I/O 바운드 
    
    I는 input, O는 output을 뜻한다. I/O로 인해 프로그램의 실행속도가 제한되는 것을 말한다. 사용자가 입력한 값을 더해주는 프로그램이라고 한다면 사용자가 값을 느리게 입력하거나 빠르게 입력하는 요청의 속도에 따라서 당연히 결과값이 나오는 속도가 달라지게 될 것이다. 이는 연산 속도와는 무관하게 입력속도가 변화되는 것으로 이를 사용자 I/O 바운드라고 한다. 입력을 늘 사용자만 하는 것이 아닌 브라우저에서 요청 속도에 따라 달라지는걸 네트워크 I/O 바운드라고 한다. 
    

[ 블로킹과 넌블로킹 ] 

블로킹이란 바운드에 의해 코드가 멈추게 되는 현상이다. 그렇다면 당연하게 넌블로킹은 바운드에 코드가 멈추지않는 것이다. 

[ 동기와 비동기 ]

1. 동기: 동기적으로 동작하는 코드란 코드가 반드시 작성된 순서 그대로 실행되는 것을 말한다. 
2. 비동기: 비동기적으로 동작하는 코드란 코드가 반드시 작성된 순서대로 실행도지 않는 것을 말한다. 

[ 코루틴 ] 

루틴 : 일련의 명령(코드의 흐름)

1. 메인루틴 : 프로그램 메인코드의 흐름
2. 서브루틴 : 보통의 함수(input과 output존재)나 메소드로 메인루틴을 보조하는 역할
3. 코루틴 : 서브루틴의 일반화된 형태로서 일반적으로 서브루틴이 하나의 진입점과 탈출점이 있다면 코루틴은 다양한 진입점과 다양한 탈출점이 있는경우를 말한다. 비동기 함수를 진행하게되면서 해당 서브루틴에 접근할 수 있는 지점이 다양해지게되고 탈출하게되면 실행할 함수도 달라지게 때문이다. 

[ async, await ]

await 뒤에는 코루틴, Task, Future 이렇게 세가지의 어웨이터블 객체만 들어갈 수 있다. 

asyncio는 파이썬 내장 라이브러리로서 비동기를 더욱 편하게 쓸 수 있게 해준다. 

**asyncio.gather 뒤에 차례로 waitable한 객체를 두게되면 그 객체들을 동시에 처리**하게 된다. (뒤에 설명되어있지만, 싱글스레드에서 동시성프로그래밍을 구현한 것이다.)

```jsx
result = await asyncio.gather(
		delivery("A", 1),
		delivery("B", 1),
		delivery("C", 1),
)
```

[ 컴퓨터 구성요소 ]

CPU: 중앙처리장치

메모리

- 주메모리(RAM): 프로그램과 데이터 저장
- 보조메모리: 저장장치라고 불리며 일시적 또는 영구적으로 저장

시스템버스: 각각의 구성요소들(CPU, 메모리..)을 연결해주고 데이터를 주고받게 해줌

운영체제(OS): 컴퓨터 시스템을 운영하고 관리하는 소프트웨어

[ 프로세스 ]

프로그램의 실행 = 해당하는 코드들이 주메모리로 올라와서 작업이 진행된다.(해당 프로그램은 보조메모리=저장장치에 있다가 주 메모리에 올라와 실행을 하게된다. 이렇게 보조메모리에 있다가 주메모리로 올라가는 것을 프로세스가 생성됐다고 표현한다.) 

이렇게 프로세스가 생성되면 CPU는 프로세스가 해야할 작업을 수행하게 된다.

CPU가 처리하는 작업의 단위 = 스레드 = 프로세스 내에서 실행되는 작업 단위

[ 스레드 갯수에 따른 분류 ]

- 싱글스레드: 스레드 한개로 동작
- 멀티스레드: 여러개의 스레드가 동작(멀티스레드에서 스레드는 서로 메모리공유와 통신이 가능하다, 마치 스레드는 팔이고 메모리는 뇌) → 장점: 자원의 낭비를 막고 효율성 향상, 단점: 한스레드에 문제가 생기면 전체 프로세스에 영향을 미침

[ 스레드 종류 ]

- 사용자 수준 스레드(파이썬은 사용자 수준 스레드에서 동작)
- 커널 수준 스레드

[ 동시성(병행성), 병렬성 ] 

*동시성과 병렬성은 상반되는 개념이아닌 함께 사용될 수 있는 개념이다.*

동시성(Concurrency)

- 한 번에 여러 작업을 동시에 다루는 것으로 여러개의 작업이 주어졌을 때 한 작업을 하고 작업을 스위칭(swiching)하여 다른 작업을 수행, 계속해서 작업을 변경하며 수행하게 된다. 여기서 시간이 오래 걸리는 작업이 있다면 비동기적으로 수행을 하고 다음 작업으로 스위칭을 하여 수행한다.
- 동시성 프로그래밍은 논리적 개념으로 멀티 스레딩, 멀티코어에서 사용되기도하고 싱글 스레드, 싱글 코어에서 사용될 수도 있다.

병렬성(Parallelism)

- 한번에 여러 작업을 병렬적, 동시적(= at the same time, not concurrency)으로 처리하는 것으로 CPU코어 단위로 병렬적 작업수행을 Multi cores이라고 하고 쓰레드 단위에서는 Multi threads라고 한다.
- 병렬성은 물리적 개념으로 CPU단위라면 CPU가 1개이상 있어야하고 쓰레드 단위라면 쓰레드가 1개이상 있어야 병렬적 수행이 가능하다.
- 파이썬에서는 GIL(global interpreter lock)으로 인해 쓰레드단위로 병렬성을 구현할 수없다. 그러므로 파이썬에서는 Multi threads가 동시성으로 구현되어야 한다.

```python
import requests
import time
import os
import threading

def fetcher(session, url):
	print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
	with session.get(url) as response:
		return response.text

def main():
	urls = ["https://naver.com", "https://daum.net", "https://google.com"] * 20

	with requests.Session() as session:
		result = [fetcher(session, url) for url in urls]
		print(result)

if __name__ == "__main__":
	start = time.time()
	main()
	end = time.time()
	print(end - start) # 수행시간 출력
```

fetcher 함수가 어떤 Thread에서 실행되는지 확인 

```python
print(f"{os.getpid()} process | {threading.get_ident() url : {url}")
```

getpid(): 현재 process id 반환

**process는 각각의 id가 존재하는데 그 id를 pid라고 함*

![image](https://user-images.githubusercontent.com/74139727/191920427-a4873103-1d65-429d-a73a-35cbde71b302.png)


pid가 97744 process인 프로세스 한 개에서 작업 수행 확인

수행시간을 살펴보면 20초가 걸린걸 확인할 수 있다.

![image](https://user-images.githubusercontent.com/74139727/191920464-fd9c914e-e1b6-486a-b152-0221240caa8f.png)

```python
import requests
import time
import aiohttp
import asyncio
import os
import threading

async def fetcher(session, url):
	print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
	async with session.get(url) as response:
		return await response.text()

async def main():
	urls = ["https://naver.com", "https://daum.net", "https://google.com"] * 20

	async with aiohttp.ClientSession() as session:
		result = await asyncio.gather(*[fetcher(session, url) for url in urls])
		print(result)

if __name__ == "__main__":
	start = time.time()
	asyncio.run(main())
	end = time.time()
	print(end - start) # 수행시간 출력
```

위의 코드를 실행하게되면 비동기적으로 작업을 수행하게되어 수행시간이 기존 동기적방식으로 실행한 20초의 절반값인 10초로 단축된걸 확인할 수 있다.

![image](https://user-images.githubusercontent.com/74139727/191920659-3317b3f0-f851-42c2-a77e-bfb5c240b3eb.png)

이를 httpio를 사용하지않고 멀티쓰레딩으로 구현하면

```python
import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor

def fetcher(params):
	session = params[0]
	url = params[1]
	print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
	with session.get(url) as response:
		return response.text

def main():
	urls = ["https://naver.com", "https://daum.net", "https://google.com"] * 20

	executor = ThreadPoolExecutor(max_workers=1) # 사용할 최대 쓰레드 갯수

	with requests.Session() as session:
		#result = [fetcher(session, url) for url in urls]
		#print(result)
		params = [(session, url) for url in urls]
		results = list(executor.map(fetcher, params))
		print(results)
		

if __name__ == "__main__":
	start = time.time()
	main()
	end = time.time()
	print(end - start) # 수행시간 출력
```

[exetutor.map](http://exetutor.map) 매서드는 각각 fetcher와 원소들을 이어주는 역할을 하는데 즉, 각각의 함수를 쓰레드에 작업을 배분해주면서 동시성 구현이 가능해진다.  

```python
executor.map( fetch, params(list) )
```

우리는 fetcher함수의 인자가 2개임으로 아래와 같이 묶어서 파라미터 자리에 넣어주고 fecher함수에서 파라미터를 받아 각각의 인자를 변수에 넣어주도록 한다. 

```python
params = [(session, url) for url in urls]
```

```python
def fetcher(session, url):
```

```python
def fetcher(params):
	session = params[0]
	url = params[1]
```

멀티 쓰레드를 사용하다가 하나의 쓰레드에 이상이 생기면 쓰레드들 끼리 메모리를 공유하기때문에 다른 쓰레드에도 영향을 미치게된다. 그래서 도입되게 된게 GIL(Global interpreter lock; 전역 인터프리터 잠금)이다. 한 번에 한개의 스레드만 유지하는 락으로 한스레드가 다른 스레드를 차단하여 제어하는 것을 막아주어 병렬성이 불가능하게 한다. 이는 멀티 스레딩의 위험으로부터 보호하는 것으로 GIL로 인해 파이썬에서는 스레드로 병렬성 연산이 불가능하게 된다. 그래서 파이썬의 멀티 쓰레딩은 동시성을 사용하여 네트워크 i/o 바운드 코드에서 유용하게 사용가능하지만 CPU 바운드 코드(연산만 하는 코드)에서는 GIL로 인해 동시성밖에 구현하지 못해 원하는 결과를 얻을 수 없다.  

멀티 프로세싱은 프로세스를 복제하는데 각각의 프로세스들은 메모리를 공유하지 않기 때문에 통신을 해야하여 그에 대한 비용이 증가하게 된다. 

아래의 코드는 단순히 cpu 연산만하는 cpu 바운드 코드이다.

```python
import time
import os
import threading

# nums = [50, 63, 32]
nums = [30] * 100

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total

def main():
    results = [cpu_bound_func(num) for num in nums]
    print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 49.37, 34
```

아래는 위 코드를 멀티 쓰레딩으로 구현한 코드이다.

```python
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor

nums = [30] * 100
# nums = [50, 63, 32]

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread, {num}")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total

def main():
    executor = ThreadPoolExecutor(max_workers=10)
    results = list(executor.map(cpu_bound_func, nums))
    print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 50, 36
```

일반 CPU 바운드 코드와 이를 멀티쓰레딩으로 구현한 코드의 실행시간 비교를 했을 때 49.37초와 50초로 차이가 거의 나지 않는 것을 확인 할 수 있다. 연산을 하는데 있어서 동시성을 사용할 필요가 없는 것을 알 수 있다. 

nums = [30] * 100으로 변경 후 멀티 쓰레딩으로 실행하면 36초 멀티 프로세싱으로 구현시 22초인걸 확인 할 수 있다. 

```python
import time
import os
import threading
from concurrent.futures import ProcessPoolExecutor

nums = [30] * 100

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} thread, {num}")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total

def main():
    executor = ProcessPoolExecutor(max_workers=10)
    results = list(executor.map(cpu_bound_func, nums))
    print(results)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 22
```
