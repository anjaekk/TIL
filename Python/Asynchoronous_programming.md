## Coroutine
코루틴은 cooperative routine의 줄인말로 서로 협력하는 루틴이라는 뜻이다. 코루틴이 아닌 함수는 main routine과 sub routine으로 구성되며 서로 종속적인 관계가 된다. 아래의 코드를 보면 calc함수는 main routine이 되고 add, mul함수가 각각 sub routine이 되어 작업 종료시 calc함수로 돌아오게 된다.
```
def add(a, b):
    c = a + b 
    return c
    
def mul(a, b):
	c = a * b
    return c
	
def calc():
    add = add(1, 2)    # add 함수가 끝나면 다시 calc 함수로 돌아옴
 	mul = mul(2, 3)    # mul 함수가 끝나면 다시 calc 함수로 돌아옴
    print(add, mul)
    
    
calc()
```

하지만 coroutine은 종속적인 관계가 아닌 대등한 관계로 main routine의 최초 호출이 있으면 coroutine은 해당 작업을 실행하고 그 직업이 완료되지 않았더라도 main routine으로 다시 돌아가 다음 작업을 실행한다. 이러한 python의 coroutine은 single thread에서 대기시간을 줄여 CPU의 활용을 극대화 시킬 수 있다. 
  

## asyncio
[📂 Asyncio Documentation](https://docs.python.org/ko/3.8/library/asyncio.html)    
asyncio는 python 3.6부터 등장한 동시성 코드를 작성하는 라이브러리이다. asyncio는 async와 await구문을 통해 아래와 같이 간단하게 사용할 수 있다. 

```
import asyncio

async def func():
	await asyncio.sleep(1)
    print('foo foo')

asyncio.run(func())

```
asyncio 함수를 사용하게되면 위에서 정의한 func함수가 실행 완료되기 전에 다른 코드가 실행될 수 있게된다.

## uvloop
asyncio를 보면 uvloop은 asyncio의 이벤트 루프 대체제이다. Cython(python함수를 이용해 C언어 호출)으로 구현되어있으며 asyncio를 더 빠르게 만들어준다. 이 uvloop를 얼마나 잘 만들었느냐에 따라 asyncio의 성능을 효과적으로 끌어올릴 수 있기 때문에 python 비동기 프로그래밍의 핵심적인 역할을 한다.

> _**이벤트 루프란(Event Loop)**_    
> _이벤트 루프는 loop라는 말 그대로 반복문을 돌면서 하나씩 작업을 수행하게 된다.   
> 하나의 작업이 다 완료되지 않았더라도 그 작업은 통제권을 Event loop에 넘겨주므로써 Event loop는 다음 작업을 실행하게 된다._
