다른 파이썬 파일에 있는 변수, 함수, 클래스를 사용하기위해서는 해당 변수, 함수, 클래스가 들어있는 Module과 Package를 아래와 같은 방법으로 import해야한다. 
```python
from [모듈이나 패키지] import [원하는 변수, 함수, 클래스]
```

## Module과 Package 임포트 서치 순서
---

`import` 할때 Module과 Package를 찾기위해서 아래와 같은 장소 `search 순서`가 존재한다. 아래의 순서대로 `search` 후 해당 `Module`이나 `Package`가 없으면 `ModuleNotFoundError`가 발생한다.
>1. sys.modules
>
>2. built-in modules
>
>3. sys.path

각각의 장소가 무엇인지에 대해 알아보자.
### 1. sys.modules
파이썬이 모듈이나 패키지를 찾기위해 가장 먼저 확인하는 곳으로 이미 `import`된 모듈과 패키지를 저장하고 있는 `dictionary`이다. 이미 한번 `import`된 모듈과 패키지는 파이썬이 다시 찾지 않도록 하기위해 가장먼저 이전에 `import`된 목록을 확인하는 것이다. _(새롭게 `import`하는 모듈이나 패키지는 여기 없다!)_

### 2. built-in modules
두번째로 확인하는 곳인 `uilt-in modules`은 파이썬에서 제공하는 공식 라이브러리이다. 이러한 빌트인 모듈은 이미 파이썬을 설치할 때부터 함께 포함되어 있기 때문에 쉽게 찾을 수 있다.

### 3. sys.path
마지막을 확인하는 `sys.path`는 `str`요소들을 가지고있는 `list`이다. 이 list에는 로컬 프로젝트들의 경로들이 적혀있는데 파이썬 모듈이나 패키지를 import하게되면 이 경로들을 하나하나 살펴보며 어느 경로인지 확인하는 것이다.sys또한 파이썬에 기본으로 내장되어있는 built-in modules이다. 이 sys모듈을 import하여 path를 출력하거나 수정할 수 있다.

- **`sys` 모듈의 위치**
`sys` 모듈을 사용하기위해서는 파이썬은 built-in modules에서 찾아 사용하게 된다.

- **`sys.modules` 와 `sys.path`의 차이점**
`sys.modules`은 이미 한번 import된 dictionary구조의 목록
`sys.path`는 패키지의 **경로**가 적혀있는 list구조의 목록

> 참조
>
>🔗 [python 공식 홈페이지](https://docs.python.org/3/tutorial/modules.html#intra-package-references)
