# K-최근접 알고리즘(K-NN, K-Nearest Neighbot Algorithm)

사용한 예제의 출처는 => [혼자 공부하는 머신러닝+딥러닝](https://ebook-product.kyobobook.co.kr/dig/epd/ebook/4801162243665?utm_source=google&utm_medium=cpc&utm_campaign=googleSearch&gclid=CjwKCAiAl9efBhAkEiwA4TorintTGZL5Dc_Fao7A6bnGEgdIq2DGEdbWywLZ9sC_tT7iRZZcx14MThoCJe4QAvD_BwE)


### 장점

- 단순하기 때문에 다른 알고리즘에 비해 구현이 쉽다
- 훈련데이터를 그대로 가지고 있어 특별한 훈련을 하지 않기 때문에 훈련 단계가 빠르게 수행된다.

### 단점

- 훈련 테이터 범위 밖의 새로운 데이터는 예측이 불가능함
- 모델을 생성하지 않기 때문에 클래스간 관례를 이해하는데 제한적
- 미리 변수와 클래스 간의 관계를 파악하여 이를 알고리즘의 적용해야한다.
- 데이터가 많아지면 분류 단계가 느리다.

### K값

- 홀수 지정 권장
- 과적합문제를 최소하기 위해 트레인 데이터 값의 성공률과 테스트 데이터 값의 성공률의 갭이 적게 차이나는 값을 설정해야한다.
- 테스트셋이 달라질 때마다 k값을 다르게 지정해야 한다.

## 과적합

### 과대적합(over fitting)

- 훈련 셋의 점수보다 테스트 셋의 점수가 지나치게 낮은 경우
- 훈련 셋에는 잘 맞지만 일반성이 떨어지는 경우
- 특정 훈련 셋에만 너무 훈련이 되어있게 되면 발생
- High variance(큰 분산)

### 과소적합(under fitting)

- 훈련 셋보다 < 테스트 셋의 점수가 높거나 두 점수가 모두 너무 낮은 경우
- 모델이 너무 단순해서 데이터의 내재된 구조를 학습하지 못하는 경우를 말한다.
- 해결을 위해 모델을 더 복잡하게 만들어야한다.
- High bias(큰 편향)

### K-NN에서의 과적합

- k의 개수를 줄이면 과대 적합이 되고
- k의 개수를 늘리면 과소 적합이 된다.
    - 극단적으로 k를 전체 샘플로 하면 결과값이 1개만 나오기 때문에

## 분류(Classification)과 회귀(Regression) 차이

### 분류

- 예측해야할 대상(class)가 정해져 있음

→ K-NN 분류: 새로운 데이터 x가 주어졌을 때, x에 가장 가까운 k개의 데이터중 가장 많은 값의 class로 판단

예) 이 데이터는 도미일 가능성이 높다.

### 회귀

- 연속성 중 어디에 해당하는가를 예측

→ K-NN 회귀: 새로운 데이터 x가 주어졌을 때, x에 가장 가까운 k개의 데이터 값을 평균내서 값을 예측

예) 이 데이터의 크기가 이정도이니 몸무게는 이정도 일 가능성이 높다.

# 실습1-K-NN 분류

# < 데이터셋과 트레인셋 분리 전 >

## 데이터 정제

### ****Pyplot 라이브러리 설치****

```xml
python -m pip install -U pip
python -m pip install -U matplotlib
```

- matplotlib.pyplot은 MATLAB과 비슷하게 명령어 스타일로 동작하는 함수 모음
- 간편하게 그래프를 만들고 변화를 줄 수 있음

### 도미(bream)와 빙어(smelt) 데이터 추가

```xml
#도미 35마리 데이터(길이, 무게)
bream_length = [25.4, 26.3, 26.5, 29.0, 29.0, 29.7, 29.7, 30.0, 30.0, 30.7, 31.0, 31.0, 31.5, 32.0, 32.0, 32.0, 33.0, 33.0, 33.5, 33.5, 34.0, 34.0, 34.5, 35.0, 35.0, 35.0, 35.0, 36.0, 36.0, 37.0, 38.5, 38.5, 39.5, 41.0, 41.0] 
bream_weight = [242.0, 290.0, 340.0, 363.0, 430.0, 450.0, 500.0, 390.0, 450.0, 500.0, 475.0, 500.0, 500.0, 340.0, 600.0, 600.0, 700.0, 700.0, 610.0, 650.0, 575.0, 685.0, 620.0, 680.0, 700.0, 725.0, 720.0, 714.0, 850.0, 1000.0, 920.0, 955.0, 925.0, 975.0, 950.0]

#빙어 14마리 데이터(길이, 무게)
smelt_length = [9.8, 10.5, 10.6, 11.0, 11.2, 11.3, 11.8, 11.8, 12.0, 12.2, 12.4, 13.0, 14.3, 15.0] 
smelt_weight = [6.7, 7.5, 7.0, 9.7, 9.8, 8.7, 10.0, 9.9, 9.8, 12.2, 13.4, 12.2, 19.7, 19.9]
```

### 도미와 빙어 데이터 기반 그래프

```xml
from K_NN_data import * 
import matplotlib.pyplot as plt 

plt.scatter(bream_length, bream_weight) 
plt.scatter(smelt_length, smelt_weight) 
plt.xlabel('length') 
plt.ylabel('weight') 
plt.show()
```

- scatter: 산점도 그리는 함수

→ 물고기 길이에 따라 무게가 많이 나가서 선형적 그래프가 그려지게 된다.

### 도미와 빙어 데이터 합치기

```xml
length = bream_length + smelt_length 
weight = bream_weight + smelt_weight

# 2차원 리스트 생성
fish_data = [[l, w] for l, w in zip(length, weight)]

fish_target = [1] * 35 + [0] * 14
```

- 빙어는 0, 도미는 1로 하여 정답 데이터를 만든다.
- 길이와 무게 두가지의 feature를 이용한다.
    
    fish_data
    
    ```xml
    **[[25.4, 242.0], [26.3, 290.0], [26.5, 340.0], [29.0, 363.0], [29.0, 430.0], [29.7, 450.0], [29.7, 500.0], [30.0, 390.0], [30.0, 450.0], [30.7, 500.0], [31.0, 475.0], [31.0, 500.0], [31.5, 500.0], [32.0, 340.0], [32.0, 600.0], [32.0, 600.0], [33.0, 700.0], [33.0, 700.0], [33.5, 610.0], [33.5, 650.0], [34.0, 575.0], [34.0, 685.0], [34.5, 620.0], [35.0, 680.0], [35.0, 700.0], [35.0, 725.0], [35.0, 720.0], [36.0, 714.0], [36.0, 850.0], [37.0, 1000.0], [38.5, 920.0], [38.5, 955.0], [39.5, 925.0], [41.0, 975.0], [41.0, 950.0], [9.8, 6.7], [10.5, 7.5], [10.6, 7.0], [11.0, 9.7], [11.2, 9.8], [11.3, 8.7], [11.8, 10.0], [11.8, 9.9], [12.0, 9.8], [12.2, 12.2], [12.4, 13.4], [13.0, 12.2], [14.3, 19.7], [15.0, 19.9]]**
    ```
    
    fish_target
    
    ```xml
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ```
    

## 훈련

### 사이킷런(Scikit-learn) 설치

```xml
pip install scikit-learn
```

- 파이썬을 대표하는 머신러닝 오픈소스 라이브러리
- 무료(개인, 비지니스 모두)
- 사이킷런 페이지에 가면 무료로 이용할 수 있는 데이터도 있음

### 사이킷런(Scikit-learn)의 K-NN 분류 클래스 이용

```xml
from sklearn.neighbors import KNeighborsClassifier 
kn = KNeighborsClassifier()
```

- KNeighborsClassifier(): K-NN 분류 클래스
- K 기본값: 5
    - n_neighbors 매개변수로 변경 가능

### 도미 찾기 기준 학습

```xml
kn.fit(fish_data, fish_target) 
print(kn.score(fish_data, fish_target)) # 1.0
```

- fit 메서드를 통해 도미 fish_data를 이용해 target생선이 맞는지 학습한다.
- score 메소드를 이용하여 훈련 평가
    - 0~1 사이의 값 반환
    - 1은 모든 데이터를 정확히 맞춘 것

### K값 변경

```xml
kn = KNeighborsClassifier(n_neighbors=49) 
kn.fit(fish_data, fish_target) 
print(kn.score(fish_data, fish_target)) # 0.7142857142857143
```

- K를 49로 줬을 때(근처 49개의 데이터를 이용해 어떤 생선인지 확인) → 정확도: 35/49 = 0.7142857142857143
- 전체 데이터가 49개이니, k값이 중요하다는 걸 알 수 있다.

# < 트레인 셋과 테스트 셋 분리>

## 훈련셋(Train set)과 테스트 셋 분리

- 각 데이터 셋은 샘플이 고루 섞여 있어야 한다.
    - 샘플링 편향: 샘플링이 한쪽으로 치우쳐져 있는 경우
    

### 넘파이 설치

```xml
pip install numpy
```

- 데이터 섞기, 골고루 샘플 데이터 뽑아서 훈련셋과 테스트셋 만들기

### 리스트를 넘파이 array로 변경

```xml
import numpy as np 

input_arr = np.array(fish_data) 
target_arr = np.array(fish_target)
```

### 무작위 샘플 선택

```xml
np.random.seed(42) 
index = np.arange(49) # [0, 1, 2, ... , 48] 
np.random.shuffle(index) 

# 배열 인덱싱
train_input = input_arr[index[:35]] 
train_target = target_arr[index[:35]]
```

- 섞은 후 35개의 샘플 선택
- 일정한 결과를 얻기위한 random seed 설정

### 표준점수(z점수)

(특성-평균)/표준편차

# K-최근접 회귀(K-NN Regression)

## 회귀

우선 회귀란 여러 개의 독립변수와 한 개의 종속변수 간의 상관관계를 모델링하는 기법을 말한다. 머신러닝 에서 독립변수는 = feature에 해당하고 종속변수는 = 결정 값에 해당하게 된다. 여기서 파악해야하는 건 주어진 feature와 결정 값 데이터에서 학습을 통해 **최적의 회귀 계수를 찾아내는 것**이다.

## K-최근접 회귀

주변의 가장 가까운 K개의 샘플을 통해 값을 예측하는 방식

# 실습1-K-NN 회귀

### 사이킷런(Scikit-learn)의 K-NN 회귀 클래스 이용

KNeighborsRegressor

[sklearn.neighbors.KNeighborsRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html)

```python
class sklearn.neighbors.KNeighborsRegressor(
	n_neighbors=5, 
	*, 
	weights='uniform', 
	algorithm='auto', 
	leaf_size=30, 
	p=2, 
	metric='minkowski', 
	metric_params=None, 
	n_jobs=None
)
```

- n_neighbors: 근접한 K의 값
- weights: 가중치
    - uniform: 균일한 가중치(기본값, 각 이웃의 포인트가 동일한 가중치를 가짐)
    - distance: 거리의 역수로 가중치 부여(가까울 수록 가중치 높아짐)
    - callable: 사용자가 직접 정의한 함수(파라미터로 거리가 저장된 배열을 받고 가중치가 저장된 배열을 리턴해야함)
- algorithm: 가까운 이웃 계산시 사용되는 알고리즘 선택
    - auto: 입력된 훈련 데이터에 기반하여 적잘한 알고리즘 사용(기본 값)
    - ball_tree: Ball-Tree 구조 사용
    - kd_tree: KD_Tree 구조
    - brute: Brute-Force
- leaf_size: 알고리즘을 ball_tree나 kd_tree와 같이 tree 구조를 사용했을 때 leaf의 사이즈를 선택
    - 트리저장을 위한 메모리, 트리 구성과 쿼리 처리 속도에 영향을 미침
- p: 민코프스키 미터법(Minkowski)의 차수를 결정
    - 1: 맨해튼 거리(Manhatten distance)
    - 2: 유클리드 거리(Euclidean distance)
- metric: 거리 계산에 사용될 메트릭
    - minkowski: p=2일 때, 표준 유클리드 거리가 됨(기본값)
    - 유효한 메트릭 참조
        
        [sklearn.metrics.pairwise.distance_metrics](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.distance_metrics.html#sklearn.metrics.pairwise.distance_metrics)
        
- metric_params: 메트릭 함수에 대한 키워드 인수(기본 값=None)
- n_jobs: 이웃 검색을 위해 실행할 병렬 작업 수(기본 값=None)

### 훈련 데이터 셋

```python
import numpy as np

# K-NN 회귀를 위한 데이터 셋
# 농어의 길이
perch_length = np.array([8.4, 13.7, 15.0, 16.2, 17.4, 18.0, 18.7, 19.0, 19.6, 20.0, 21.0,
       21.0, 21.0, 21.3, 22.0, 22.0, 22.0, 22.0, 22.0, 22.5, 22.5, 22.7,
       23.0, 23.5, 24.0, 24.0, 24.6, 25.0, 25.6, 26.5, 27.3, 27.5, 27.5,
       27.5, 28.0, 28.7, 30.0, 32.8, 34.5, 35.0, 36.5, 36.0, 37.0, 37.0,
       39.0, 39.0, 39.0, 40.0, 40.0, 40.0, 40.0, 42.0, 43.0, 43.0, 43.5,
       44.0])
# 농어의 무게
perch_weight = np.array([5.9, 32.0, 40.0, 51.5, 70.0, 100.0, 78.0, 80.0, 85.0, 85.0, 110.0,
       115.0, 125.0, 130.0, 120.0, 120.0, 130.0, 135.0, 110.0, 130.0,
       150.0, 145.0, 150.0, 170.0, 225.0, 145.0, 188.0, 180.0, 197.0,
       218.0, 300.0, 260.0, 265.0, 250.0, 250.0, 300.0, 320.0, 514.0,
       556.0, 840.0, 685.0, 700.0, 700.0, 690.0, 900.0, 650.0, 820.0,
       850.0, 900.0, 1015.0, 820.0, 1100.0, 1000.0, 1100.0, 1000.0,
       1000.0])
```

### 산점도 그래프 확인

```python
plt.scatter(perch_length, perch_weight) 
plt.xlabel('length') 
plt.ylabel('weight') 
plt.show()
```

![image](https://user-images.githubusercontent.com/74139727/220824130-2a0cabda-da2d-432a-bdeb-7eda220542ae.png)


### 훈련 세트 준비

```python
from sklearn.model_selection import train_test_split

train_input, test_input, train_target, test_target = train_test_split(
    perch_length, perch_weight, random_state=42
)

train_input = train_input.reshape(-1, 1)
test_input = test_input.reshape(-1 ,1)
```

- 사이킷 런에서 기본적으로 2차원 배열을 사용하기 때문에(행=샘플, 열방향=특성) numpy의 reshape을 이용해 1차원 배열을 2차원 배열로 바꿔줌
- train_input을 출력해보면 아래와 같은 2차원이 됨
    - reshape는 헷갈릴 수 있는데
    reshape(인자 갯수): 괄호의 개수
        
        인자의 뒤에서 부터 가장 안쪽 괄호의 개수를 지정한다고 생각하면 된다.
        
        가장 안쪽 괄호의 개수라면 1은 안쪽괄호의 개수
        
        그리고 -1은 정해진 값을 제외한 나머지 값들을 의미한다. 여기서는 (42, 1)
        
        = 총 개수가 인자들의 곱과 같으면 어떤 차원이든 생성가능!
        
    
    ```python
    [[19.6]
     [22. ]
     [18.7]
     [17.4]
    #....
    ]
    ```
    

### 회귀모델 훈련

```python
from sklearn.neighbors import KNeighborsRegressor

knr = KNeighborsRegressor()
knr.fit(train_input, train_target)

knr.score(test_input, test_target) #0.992809406101064
```

- 1에 가까운 0.99..로 타겟을 잘 맞준다고 할 수있음

### 회귀 결과 값

1. **결정 계수(R-Squared)**
    - 분류에서 나온 값 = 정확도(몇 개 중에 몇 개 맞았는지)
    - 회귀에서 나온 값 = 결정 개수(Coefficient of determination)
    - SST = SSE + SSR
    - 총 변동 = 설명된 변동 + 설명안된 변동
    - 평균이로부터의 거리 = 평균부터 우리가 만든 모델의 거리 + 우리 모델에서 관측된 값의 거리(오차)
    - 0(예측이 평균 값과 비슷 → 좋지 않은 회귀 모델)
    - 1(예측이 타겟에 정확히 맞춘다면 분자가 0이됨 → 좋은 회귀 모델)



1. 평균 절대값 오차(MAE, Mean Absolute Error)
    
    ```python
    from sklearn.metrics import mean_absolute_error
    
    test_prediction = knr.predict(test_input)
    mae = mean_absolute_error(test_target, test_prediction)
    print(mae) # 19.157142857142862
    ```
    
    - test_target과 test_prediction 차이의 절대값의 평균을 리턴한다.
    - 19g정도 오차가 난다는 걸 확인 할 수 있음(더 많은지 적은지는 알 수 없음)

### 과적합 확인

```python
print(knr.score(train_input, train_target)) # 0.9698823289099254
print(knr.score(test_input, test_target)) # 0.992809406101064
```

- 훈련 셋 < 테스트 셋 이므로 과소적합(under fitting)된 것을 확인할 수 있음
