# Function Parameters, arguments
파이썬에서 함수를 사용할 때 `input`으로 `매개변수(Parameters)`를 받아서 함수 실행후 값을 `output`으로 반환하게 된다. 여기서 **다양한 형태의 인수를 파라미터로 받을 때에는 각 형식에 따라 받아오는 순서가 존재**하게 된다.
## 1. 디폴트 값이 있는 파라미터
- **위치파라미터 - 디폴트 값 파라미터 순**

우선 아래의 `info` 함수의 코드를 보자. `info` 함수는 이름, 나이, 사는 곳을 파라미터로 받게 된다.

- **기본 함수**
```python
def info(name, age, city):
	print(f"{name}, {age}, {city}")
    
info("둘리", 10, "Seoul") 

# 둘리, 10, Seoul
```

- **city에 디폴트 값을 넣은 함수**
```python
def info(name, age, city="Seoul"):
	print(f"{name}, {age}, {city}")
    
info("둘리", 10)

# 둘리, 10, Seoul
```
`city`는 디폴트 값이 될테니 `name`, `age`값만 넣어주면 된다. 함수를 사용해보자.

함수의 결과를 보면 `city`에 `Seoul`이 들어가 둘리, 10, `Seoul`가 잘 출력됨을 알 수 있다. 
하지만 맨 뒤에있는 `city`가 아닌 `name`이나 `age`에 디폴트 값을 주면 어떻게 될까?

- **name에 디폴트 값을 넣은 함수**
```python
def info(name="둘리", age, city):
	print(f"{name}, {age}, {city}")
    
info(10, "Seoul")

# SyntaxError: non-default argument follows default argument
```
name에 디폴트 값을 넣었더니 결과는 출력되지 않고 SyntaxError가 뜨게된다. 이는 **디폴드 값이 있는 파라미터를 사용하는 경우 사용하지 않는 경우보다 적은 인수(arguments)를 넣기 때문이다.** name이나 age에 디폴트 값을 주면 어느 파라미터의 인수인지 알 수 없으므로 디폴트 값이 있는 파라미터는 없는 파라미터보다 뒤로 가야한다.

## 2. 가변 인수
- **위치 파라미터 - 가변인수를 받는 파라미터 순**

`가변 인수(variable length arguments)`는 말 그대로 값의 갯수가 가변적인 인수이다. 이런 가변 인수는 관례적으로 `*args`로 표현한다.(`*star`, `*hamster` 처럼 앞에 '`*`'만 붙어도 가변 인수를 나타내지만 `*args`로만 쓰자) 함수에서는 이런 가변 인수를 쓰면 튜플로 인식하여 실행한다.

다음의 `func_param_with_var_args` 함수를 봐보자.
```python
def func_param_with_var_args(name, *args, age):
    print("name=",end=""), print(name)
    print("args=",end=""), print(args)
    print("age=",end=""), print(age)

func_param_with_var_args("정우성", "01012341234", "seoul", 20)

# TypeError: func_param_with_var_args() missing 1 required keyword-only argument: 'age'
```
결과를 보니 `TypeError`가 뜬다. 그 이유를 살펴보니 '`age`'의 인수가 누락됐다고 한다. 우리가 확인하기에는 분명 마지막에 20이라는 숫자가 '`age`'인 것 같아보이지만 컴퓨터는 이를 알 수 없다. **`*args`는 몇개의 인수를 받는지 알 수 없다. 그러므로 일반 위치인수(위치로 인수를 받는 `name`과 `age`같은 인수)보다 가변인수는 뒤로 가야 한다.**

**- 가변인수를 위치인수 뒤로 보낸 함수**

```python
def func_param_with_var_args(name, age, *args):
    print("name=",end=""), print(name)
    print("age=",end=""), print(age)
    print("args=",end=""), print(args)

func_param_with_var_args("정우성", "01012341234", "seoul", 20)

# name=정우성
# age=01012341234
# args=('seoul', 20)
```

## 3. 키워드 가변 인수
- **위치 파라미터 - 파라미터가 키워드로 되어있는 인수 - 키워드 가변 인수를 받는 파라미터**

`키워드 가변 인수(variable length keyword arguments)`도 관례상 `**kwargs` 로 사용한다. 앞에 `**`만 붙으면 상관없지만 관례는 중요하다. `**kwargs`로 쓰도록 하자. 키워드 가변인수는 **딕셔너리 형태**로 정해지지 않은 가변의 인수이다. 

```python
def func_param_with_kwargs(name, age, **kwargs, address=0):
    print("name=",end=""), print(name)
    print("age=",end=""), print(age)
    print("kwargs=",end=""), print(kwargs)
    print("address=",end=""), print(address)


func_param_with_kwargs("정우성", "20", mobile="01012341234", address="seoul")

#  File "main.py", line 1
#    def func_param_with_kwargs(name, age, **kwargs, address=0):
                                                    ^
# SyntaxError: invalid syntax
```
결과는 `SyntaxError`가 발생한다. 보면 **이건 디폴트 값이 있는 파라미터가 아니라 키워드로 되어있어서 인수로 키워드를 받는 파라미터이다.** 위 함수에서 파라미터와 인수의`**kwargs`와 `address=0`의 순서를 바꿔주게 되면 잘 실행되는걸 확인 할 수 있다. 

```python
def func_param_with_kwargs(name, age, address=0, **kwargs):
    print("name=",end=""), print(name)
    print("age=",end=""), print(age)
    print("kwargs=",end=""), print(kwargs)
    print("address=",end=""), print(address)


func_param_with_kwargs("정우성", "20", address="seoul", mobile="01012341234")

# name=정우성
# age=20
# kwargs={'mobile': '01012341234'}
# address=seoul
```

## 4. 가변 인수(*args)와 키워드 가변 인수(**kwargs)
- **위치 파라미터 - 디폴트 값 파라미터 - 가변인수를 받는 파라미터 - 키워드 '인수'를 받는 파라미터 - 키워드 가변 인수를 받는 파라미터**

```python
def mixed_params(name="아이유", *args, age, **kwargs, address):
    print("name=",end=""), print(name)
    print("args=",end=""), print(args)
    print("age=",end=""), print(age)
    print("kwargs=",end=""), print(kwargs)
    print("address=",end=""), print(address)


mixed_params(20, "정우성", "01012341234", "male" ,mobile="01012341234", address="seoul")

#  File "main.py", line 1
#    def mixed_params(name="아이유", *args, age, **kwargs, address):
#                                                       ^
# SyntaxError: invalid syntax
```
`SyntaxError`에러가 발생하는 코드이다 어떻게 변경해줘야 할까? 
이제까지 봐왔던 다양한 인수와 파라미터의 조합으로 굉장히 복잡하다. 일단 정답 순서를 보면서 이유를 찾아보자.

```python
def mixed_params(age, name="아이유", *args, address, **kwargs):
    print("age=",end=""), print(age)
    print("name=",end=""), print(name)
    print("args=",end=""), print(args)
    print("address=",end=""), print(address)
    print("kwargs=",end=""), print(kwargs)


mixed_params(20, "정우성", "01012341234", "male", address="seoul", mobile="01012341234")

#  age=20
#  name=정우성
#  args=('01012341234', 'male')
#  address=seoul
#  kwargs={'mobile': '01012341234'}
```

>1. 위치 파라미터
>
>2. 디폴트 값 파라미터
>
>3. 가변인수를 받는 파라미터
>
>4. 키워드 인수를 받는 파라미터(Non-default keyword-only arguments)
>
>5. 파라미터가 키워드로 되어있는 인수(keyword-only arguments) 
>
>6. 키워드 가변인수를 받는 파라미터

<u>\* 5번은 파라미터가 키워드로 되어있기 때문에 키워드로 밖에 인수를 받지 못한다.</u>

내가 이해한 내용은 아래와 같다. 

1. 가장 기본인 위치파라미터가 맨 앞으로 오는 것에는 이견이 없길 바란다.
2. 디폴트 값 파라미터는 인수를 따로 받지 않기 때문에 위치 파라미터의 뒤로만 오면 된다. 
3. 가변인수를 받는 파라미터는 키워드 형태와 구분되기 때문에 키워드의 앞으로 위치한다.
4. 키워드를 인수를 받는 파라미터는 파라미터가 키워드로 되어있는 인수보다 앞으로 간다.
5. 파라미터 자체에 디폴드값이 있는 키워드 인수는 그 뒤로
6. 맨 마지막이 키워드 가변인수를 받는 파라미터 이다.

> 참조
🔗 [Python keyword only arguments](https://getkt.com/blog/python-keyword-only-arguments/#non-default-kw-syntax)
