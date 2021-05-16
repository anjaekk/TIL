
파이썬으로 알고리즘 문제를 풀다보면 내 답과는 너무 다른 다른 사람의 답을 보고 깜짝 놀란적이 있다.
문제를 풀었다는 기쁨도 잠시, 내 5줄에 걸친 내 코드에 비해 너무나 간단한 한줄코드로 슈류륙~ 풀어져있는 답을보며 아?! 하고 문제를 풀어도 찝찝한 기분을 지울 수 없다ㅠㅠ

`컴프리헨션`을 적절히 사용한다면 나의 코드도 간결하고 가독성이 더 높아 질 수 있다!!

⚠️ **경고** ⚠️
**지나치게 많은 표현식을 사용하게되면 오히려 가독성을 떨어트릴 수 있음!**

## 컴프리헨션(Comprehension)?!
---
우선 들어가기에 앞서 `Comprehension`의 뜻 먼저 알아보자! 
![](https://images.velog.io/images/anjaekk/post/afbda0df-b5ae-4b23-b209-a9c852afb74a/image.png)
Comprehension의 뜻을 구글에 검색한 결과 크게 `포함`과 `이해`이라는 뜻으로 추릴 수 있다. 컴프리헨션은 파이썬 내에서 리스트, 딕셔너리, 집합과 같은 자료구조를 생성, 추출, 검색할때 간결하고 좀 더 이해하기 쉽게 만드는 방법이라고 할 수 있다. 컴프리헨션이라면 조건이 있는 자료구조를 `한줄 코드`로 구현할 수 있다.

## 리스트 컴프리헨션
---
백문불여일견.. 가장 대표적인 리스트를 이용하여 알아보도록 한다.
컴프리헨션을 사용한 경우와 사용하지 않은 경우로 나누어 다음의 조건으로 리스트를 출력한다고 가정해보자.

### ▶️ 1단계: 1부터 10까지의 정수
#### 사용 ❌
>```python
li = []
for i in range(1, 11):
	li.append(i)
```

#### 사용 ⭕️
>```python
[i for i in range(1, 11)]
```

리스트 변수를 따로 선언하지도 않고, `append`함수를 사용하지도 않았다.. 오.. 놀라워라
이를 아래와 같이 응용해보도록 한다. 


### ▶️ 2단계: 1부터 10까지의 정수 * 3
#### 사용 ❌
>```python
li = []
for i in range(1, 11):
	li.append(i * 3)
```

#### 사용 ⭕️
>```python
[i * 3 for i in range(1, 11)]
```

### ▶️ 3단계: 1부터 10까지의 정수 중 홀수에 * 3
#### 사용 ❌
>```python
li = []
for i in range(1, 11):
	if i % 2 == 1:
		li.append(i * 3)
```

#### 사용 ⭕️
>```python
[i * 3 for i in range(1, 11) if i % 2 == 1]
```

### ▶️ 4단계: 1부터 10까지의 정수 중 홀수 * 3, 짝수 + 2
#### 사용 ❌
>```python
li = []
for i in range(1, 11):
    if i % 2 == 1:
        li.append(i * 3)
    else:
        li.append(i + 2)
```

#### 사용 ⭕️
>```python
[i * 3 if i % 2 == 1 else i +2 for i in range(1, 11)]
```

## 딕셔너리, 집합
---
딕셔너리는 key값과 value 값을 콜론(:)으로 나누어 사용하고 집합은 {}로 묶어 사용하면 된다!


---
\* 참고 *
[파이썬 알고리즘 인터뷰](http://www.kyobobook.co.kr/product/detailViewKor.laf?mallGb=KOR&ejkGb=KOR&barcode=9791189909178)
[[Python의 꽃] 리스트 컴프리헨션(List Comprehension)](https://bio-info.tistory.com/28)
[파이썬(python) #23_ 컴프리헨션(Comprehension) 이란?](https://doorbw.tistory.com/174)
