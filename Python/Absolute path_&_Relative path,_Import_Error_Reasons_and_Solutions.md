# Absolute path & Relative path
---

파이썬에서 경로를 표시하는 방법에는 2가지 방법이 있는데 첫 번째는 `Absolute path`(절대경로)와 두 번째는 `Relative path`(상대경로)이다. (참고로 파이썬은 `.`으로 경로를 표현한다.)

### 1. Absolute path(절대경로)
절대경로는 말그대로 변하지않는 고유경로이다.  **`import`를 행하는 파일의 위치가 어디있던 무조건 그 패키지의 시작은 그 패키지의 최상위 디렉토리로부터 시작하기때문에 변하지 않는다.** 일반적으로 로컬패키지를 `import`할 때 절대경로를 사용하게되는데 한가지 단점이라면 그 경로의 길이가 길어질 수 있다는 단점이 있다.

### 2. Relative path(상대경로)
상대경로는 내위치를 중심으로 표현한 경로를 말한다. **본인보다 상위 디렉토리로 접근시에는 `..`을 사용하고 현재는 `.`라고 표현하고 현재 위치로부터 시작하기때문에 경로 표시방식이 상대적으로 표현**된다. 상대경로의 단점은 절대경로에 비해 직관적이지 않기 때문에 명확성이 떨어진다는 것이다.

# python3의 상대경로 import
---

우선 다음과 같은 구조의 프로젝트가 있다고 하자.

![](https://images.velog.io/images/anjaekk/post/b9e7cd05-0925-4b65-8a7d-8856514ca75e/image.png)

- **main.py**
```python
from .calculator.add_and_multiply import add_and_multiply


if __name__ == '__main__':
    print(add_and_multiply(1,2))
```

- **add_and_multiply.py**
```python
from .multiplication import multiply
# from calculator.multiplication import multiply

def add_and_multiply(a,b):
    return multiply(a,b) + (a+b)
```

- **multiplication.py**
```python
def multiply(a,b):
    return(a*b)
```

### `__intit__.py`과 `__name__` 개념

- **`__intit__.py`의 역할**
패키지의 구조는 파일 시스템의 디렉토리와 같으며 디렉토리 아래에  `__intit__.py` 파일은 해당 디렉토리가 패키지의 일부임을 알려주는 역할을 한다.(`__intit__.py` 파일이 없으면 패키지로 인식되지 않음) 하지만 `python3.3`버전부터는 `__intit__.py`파일 없이도 패키지로 인식하는데 하위버전 호환을 위해 `__intit__.py`파일을 생성하는 것이 안전하다.

- **`__name__`의 역할**
python의 `__name__`은 모듈이 저장되는 변수이며 `import`로 모듈을 가져왔을 때 모듈의 이름이 들어간다. **파이썬 인터프리터를 통해 파이썬파일을 직접실행할 경우에는 파이썬에서 알아서 그파일의 `name`은 `main`이 된다.** 파이썬 모듈을 `import`해서 사용할 경우에는 `name`은 원래 모듈 이름으로 설정된다. (즉, `add_and_mutiply.py`파일을 직접실행하면 `main`, 다른 곳에서 불러와서 실행하면 `name`은 `add_and_mutiply`가 된다.) 그러므로 **만약 해당 파일의 특정 부분이 직접 실행시킬 때에만 실행되도록 설정하고 싶다면 `if __name__ == '__main__':`이렇게 사용하면 된다.** `if문`에 해당하는 부분은 다른 파일에서 `import`하여 사용하고자 할때에는 실행되지 않게 된다. 그런데 여기서 '직접 실행'이라는 부분을 잘 생각해보면 파이썬 인터프리터가 **최초로 실행한 스크립트 파일의 `__name__`에는 `__main__`이 들어간다고 할 수 있다.** 어떤 스크립트 파일이든지 파이썬의 시작점이 될 수 있기때문에 **파이썬은 이  `__name__`변수를 통해 현재 스크립트 파일이 시작점인지 `import`해온 모듈인지 판단할 수 있게 된다. **

### `main.py`에서 상대경로를 이용하여 `add_and_mutiply`를 import
`main.py`에서 상대경로를 이용하여 `add_and_mutiply`를 `import`해보겠다. 상대경로를 이용하여 `main.py`를 실행하니 `ImportError: attempted relative import with no known parent package`라고 에러로그가 나온다. 해석하자면 **"알려진 상위 패키지없이 상대 가져 오기를 시도했습니다."**라고 하는데 그 이유는 [python 공식 홈페이지](https://docs.python.org/3/tutorial/modules.html#intra-package-references)와 [PEP 328-imports](https://www.python.org/dev/peps/pep-0328/) 읽어보면 알 수 있다. 

- **`Intra-package References`**
> Note that relative imports are based on the name of the current module. Since the name of the main module is always "__main__", modules intended for use as the main module of a Python application must always use absolute imports.

- **`PEP 328-imports(Relative Imports and __name__)`**
> Relative imports use a module's __name__ attribute to determine that module's position in the package hierarchy. If the module's name does not contain any package information (e.g. it is set to '__main__') then relative imports are resolved as if the module were a top level module, regardless of where the module is actually located on the file system.

해석하자면 상대경로를 이용하여 `import`하게되면 현재 모듈의 이름을 기반으로 한다. 메인모듈의 이름은 항상 `__main__`이기 때문에 항상 절대경로를 사용해야한다고 적혀있다. (???) `__main__`인거랑 절대 경로를 사용하는거랑 무슨관계가 있을까? 

### 원인
1. 상대경로를 이용하여 `import` 하기: `__name__`변수에 값으로 해당 모듈의 위치를 파악함
2. 만약 `__main__`으로 설정 될 경우(실행하는 주 스크립트 파일로 직접 실행할 경우) 패키지의 구조가 실제 파일 시스템에 있는 위치에 관계없이 최상위 모듈인 것처럼 된다.(즉, `__main__`이 최상위 파일인 것처럼)
3. 그렇게되면 현재 `main.py`는 `add_and_multiply.py`가 있는 `calculator`패키지와 구분되게 된다.
4. 그러므로 실행을 시키면 내가 제일 최상위 모듈 라는 의미로 **"알려진 상위 패키지없이 상대 가져 오기를 시도했습니다."**라는 에러로그를 띄우는 것이다.

### 해결
1. 아래와 같이 **절대경로로 표현**하여 최상위 폴더가 `calculator`라는 것을 알려준다.
```python
from calculator.add_and_multiply import add_and_multiply
```

## `add_and_multiply.py`에서 `multiply`를 import
좀 더 확실하게 이해하기 위해서 `add_and_multiply.py`에서 `multiply`를 `import`해보겠다. 

### 상대경로 이용
```python
from .multiplication import multiply
```
- **결과**
![](https://images.velog.io/images/anjaekk/post/23ca217f-191e-4f26-8051-f0df0f7b3c90/image.png)
`ImportError: attempted relative import with no known parent package` 아까와 동일하게 **`add_and_multiply.py`가 `__main__`이 되므로 상대경로를 사용할 수 없게 된다.**

### 절대경로 이용
```python
from calculator.multiplication import multiply
```

- **결과**
![](https://images.velog.io/images/anjaekk/post/79a7c2d8-8061-4960-b932-259fbb793a65/image.png)
`ModuleNotFoundError: No module named 'calculator'`가 발생한다. (???) 왜 분명 `calculator`폴더가 있는데 그런 모듈이름은 없다고 하는걸까? 절대경로를 `import`할때에는 현재의 디렉토리가 `sys.path`에 포함되게 된다. 
>자세한 내용은 아까 설명했던 [PEP 328-imports](https://www.python.org/dev/peps/pep-0328/) 참조

지금 `import`하려는 `multiply`는 같은 디렉토리내에 있음으로 아래와 같이 실행하면 된다.
```python
from multiplication import multiply
```

### `main`입장
`add_and_multiply.py`에서 `multiply`를 `import`하기위해 계속해서 경로 입력방식을 변경해왔다. 그 때 `main`입장은 어떤지 확인해 보기 위해 `main.py`를 실행하여 결과를 확인해 보자.(당연히 `main`안에서 `add_and_multiply.py`를 import할 때 절대경로로 알맞게 입력한 상황에서)

- **상대경로 ImportError에러**
결과: `5`
- **절대경로 ModuleNotFoundError에러**
결과: `5`
- **절대경로 최상위 디렉토리명 삭제(`calculator`)**
결과: `5`

위와 같이 파이썬 인터프리터를 실행한 `main.py`가 `main`이 되므로 **`main`에서만 절대경로로 경로를 잘 설정해주면 `main`외의 모듈들은 절대경로, 상대경로 상관없이 실행이 올바르게 된다.**


## 결론
파이썬 인터프리터를 실행하는 `__name__`이 `main`인 스크립트에서는 모듈을 `import`할 때 절대경로를 이용해야하고 직관성과 명확성을 위해 이유가 있는 경우를 제외하고는 절대경로를 이용하도록 하자. 


> 참조
> 
>🔗 [패키지](https://wikidocs.net/1418)
>
>🔗 [[Python] Python 3의 상대경로 import 문제 피해가기](https://blog.potados.com/dev/python3-import/)
>
>🔗 [python 공식 홈페이지](https://docs.python.org/3/tutorial/modules.html#intra-package-references)
>
>🔗 [PEP 328 -- Imports](https://www.python.org/dev/peps/pep-0328/)
>
>🔗 [ImportError: Attempted Relative Import With No Known Parent Package (Python)](https://techwithtech.com/importerror-attempted-relative-import-with-no-known-parent-package/)
