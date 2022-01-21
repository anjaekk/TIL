

이번에 Redis와 Fastapi로 api개발을 하면서 비동기에 대한 공부가 필요하다고 생각되어 정리해본다.

## 동기(Synchronous)와 비동기(Asynchronous)
_함수의 작업완료 여부를 신경 쓰는가 안쓰는가_

**동기(Synchronous)**
- 현재 작업의 응답 결과가 나오고 난 뒤 순차적으로 다음 작업이 요청된다. 
- 작업의 결과가 나왔는지 계속 확인한다.

**비동기(Asynchronous)**
- 현재 작업의 응답 결과가 나오기전 다음 작업을 요청한다.
- 작업의 결과를 확인하지 않는다.

~~_아래 그림을 보면 좀 더 이해하기가 쉽다._~~
![](https://images.velog.io/images/anjaekk/post/e43402ad-ebb7-48b2-8c0c-94d59faf7c1a/image.png)
> 📂 [Image Source-toolsqa](https://www.toolsqa.com/cypress/cypress-asynchronous-nature)

<br/>

## Blocking과 Non-blocking
_함수 리턴 시점과 제어권을 넘겨주느냐 안넘겨주느냐_
**블로킹(Blocking)**
- 제어권을 가지고 있는 함수가 어떤 함수를 호출하여 제어권을 넘겨줬을 때 그 호출된 함수가 완료될 때까지 제어권을 기존 함수에게 주지 않고 기다리게 만든다.

**논블로킹(Non-blocking)**
- 제어권을 가지고 있는 함수가 어떤 함수를 호출했을 때 그 함수의 리턴결과가 바로 나와 제어권이 바로 기존 제어권을 가지고 있는 함수가 가지게되어 다른 작업을 할 수 있된 경우를 말한다.

비동기와 Non-blocking은 헷갈리기 쉽다. 만약 blocking I/O 를 사용했으나 별도의 채널을 통해서 작업을 해서 어떤 프로그램의 실행을 막지 않았다면 비동기(Async)적으로 개발을 했다고 말할 수 있다. 즉 blocking은 주로 I/O 관해 이야기할 때 사용되며 Async는 프로그래밍 방법이다. 이 4가지는 각각 조합하여 각기 다른 4가지 방법으로 프로그래밍 할 수 있다.

<br/>

## Coroutine
코루틴은 `cooperative routine`의 줄인말로 서로 협력하는 루틴이라는 뜻이다. 코루틴이 아닌 함수는 `main routine`과 `sub routine`으로 구성되며 서로 종속적인 관계가 된다. 아래의 코드를 보면 calc함수는 main routine이 되고 add, mul함수가 각각 sub routine이 되어 작업 종료시 calc함수로 돌아오게 된다.
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

하지만 `coroutine`은 종속적인 관계가 아닌 대등한 관계로 main routine의 최초 호출이 있으면 `coroutine`은 해당 작업을 실행하고 그 직업이 완료되지 않았더라도 main routine으로 다시 돌아가 다음 작업을 실행한다. 이러한 python의 `coroutine`은 single thread에서 대기시간을 줄여 CPU의 활용을 극대화 시킬 수 있다.


<br/>

## asyncio
[📂 Asyncio Documentation](https://docs.python.org/ko/3.8/library/asyncio.html)
asyncio는 python의 동시성 코드를 작성하는 라이브러리이다. asyncio는 async와 await구문을 통해 아래와 같이 간단하게 사용할 수 있다. 
```
import asyncio

async def func():
	await asyncio.sleep(1)
    print('foo foo')

asyncio.run(func())

```
asyncio 함수를 사용하게되면 위에서 정의한 func함수가 실행 완료되기 전에 다른 코드가 실행될 수 있게된다.


<br/>

## uvloop
asyncio와 함께 짝꿍으로 자주 보이는 uvloop은 asyncio의 이벤트 루프 대체제이다. Cython(python함수를 이용해 C언어 호출)으로 구현되어있으며 asyncio를 더 빠르게 만들어준다. 이 uvloop를 얼마나 잘 만들었느냐에 따라 asyncio의 성능을 효과적으로 끌어올릴 수 있기 때문에 python 비동기 프로그래밍의 핵심적인 역할을 한다.
> _**이벤트 루프란(Event Loop)**_
> _이벤트 루프는 loop라는 말 그대로 반복문을 돌면서 하나씩 작업을 수행하게 된다. 하나의 작업이 다 완료되지 않았더라도 그 작업은 통제권을 Event loop에 넘겨주므로써 Event loop는 다음 작업을 실행하게 된다._




<br>


> 참조   
> 🔗 [PyCon.KR 2019 | 파이썬으로 서버를 극한까지 끌어다 쓰기: Async I/O의 밑바닥 - 한섬기](https://youtu.be/zAvWv_Wi0z0)   
> 🔗 [Blocking-NonBlocking-Synchronous-Asynchronous](https://homoefficio.github.io/2017/02/19/Blocking-NonBlocking-Synchronous-Asynchronous/)  
> 🔗 [히데쿠마 개발 블로그 | Python: asyncio를 더 빠르게 만드는 uvloop 살펴보기](https://hidekuma.github.io/python/uvloop/#:~:text=uvloop%EB%8A%94%20asyncio%EC%9D%98%20%EC%9D%B4%EB%B2%A4%ED%8A%B8,%EB%B0%B0%EC%9D%B4%EC%83%81%EC%9D%98%20%ED%8D%BC%ED%8F%AC%EB%A8%BC%EC%8A%A4%EB%A5%BC%20%EB%B3%B4%EC%97%AC%EC%A4%80%EB%8B%A4.)   
> 🔗 [코딩도장 | 코루틴에 값 보내기](https://dojang.io/mod/page/view.php?id=2418)  
