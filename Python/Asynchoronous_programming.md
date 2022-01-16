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
