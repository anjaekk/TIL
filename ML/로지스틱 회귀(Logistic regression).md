책 출처: 혼자공부하는 머신러닝 + 딥러닝

[동영상 강의]([https://www.youtube.com/watch?v=pO27UnTsYQU&list=PLJN246lAkhQjoU0C4v8FgtbjOIXxSs_4Q&index=9](https://www.youtube.com/watch?v=pO27UnTsYQU&list=PLJN246lAkhQjoU0C4v8FgtbjOIXxSs_4Q&index=9))

## 로지스틱 회귀

- 이름은 회귀이지만, 분류 알고리즘
- 인공 신경망의 가장 기초가 됨
- 이벤트가 발생할 확률을 결정하는데 사용되는 통계 모델
- 특성 간의 관계를 보여주고 특성 결과의 확률을 계산

### 로지스틱 회귀 종류

1. 이진 로지스틱 회귀
2. 다항 로지스틱 회귀
3. 순서 로지스틱 회귀

# 실습

로지스틱 회귀에 들어가기전에 k-최근접 이웃의 다중 분류로 먼저 분류하고 확률을 알아보도록 한다. 

## k-최근접 이웃의 다중 분류로 분류해보기

### 1.  데이터 가져오기

```java
import pandas as pd

fish = pd.read_csv("https://bit.ly/fish_csv_data")
fish.head()

# 넘파이 배열로 만들기
fish_input = fish[["Weight", "Length", "Diagonal", "Height", "Width"]].to_numpy()

# target 데이터에 필요한 건 "Species"(생선의 종류) 하나 
fish_target = fish["Species"].to_numpy()
```

- 종류를 출력해보면 다음과 같은 종류가 있는걸 확인 할 수 있다.
    
    ```java
    print(pd.unique(fish['Species']))
    ```
    
    ['Bream' 'Roach' 'Whitefish' 'Parkki' 'Perch' 'Pike' 'Smelt']
    

### 2. train_input, test_input, train_target, test_target 생성

```java
from sklearn.model_selection import train_test_split

train_input, test_input, train_target, test_target = train_test_split(fish_input, fish_target, random_state=42)
```

### 3. 표준화

```java
from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(train_input)
train_scaled = ss.transform(train_input)
test_scaled = ss.transform(test_input)
```

### 4. K-최근접 이웃 확률 예측

```java
from sklearn.neighbors import KNeighborsClassifier

kn = KNeighborsClassifier(n_neighbors=3)
kn.fit(train_scaled, train_target)
```

### 5. 테스트 셋의 처음 5개 샘플에 대한 확률 출력

```java
print(kn.predict(test_scaled[:5]))
# ['Perch' 'Smelt' 'Pike' 'Perch' 'Perch']

proba = kn.predict_proba(test_scaled[:5])
print(proba)

print(kn.classes_)
# 알파벳 순서로 정렬된 값
# ['Bream' 'Parkki' 'Perch' 'Pike' 'Roach' 'Smelt' 'Whitefish']
```

- sklearn의 predict_proba() 메서드로 클래스별 확률 값을 알 수 있음
- * 주의: 타깃 값을 그대로 sklearn에 전달하면 자동으로 알파벳 순서가 되기 때문에 pd.unique로 출력한 순서와 다르게 된다. 변경된 값은 `kn**.**classes_` 메서드를 이용해 출력해서 확인 가능하다.
- * _로 끝나는 메서드는 데이터로 부터 학습한 값이 나올 때이다.
- 만약 알파벳 순으로 정렬되면 안되는 경우 각 샘플의 이름을 알파벳이 아닌 숫자로 레이블링하여 사용하면 된다.
- 결과
    - 행 = 샘플, 열 = 해당 생선일 확률
    
    ```java
    [[0.         0.         1.         0.         0.         0.
      0.        ]
     [0.         0.         0.         0.         0.         1.
      0.        ]
     [0.         0.         0.         1.         0.         0.
      0.        ]
     [0.         0.         0.66666667 0.         0.33333333 0.
      0.        ]
     [0.         0.         0.66666667 0.         0.33333333 0.
      0.        ]]
    ```
    

### 6. 소수점 아래 자리수 지정해서 재출력

```java
print(np.round(proba, decimals=4))
```

- numpy의 decimals 매개변수를 이용해 소수점 자리수 지정이 가능함
- 나온 결과는 위에서 출력한 classes_메서드의 결과 순서 값과 동일
- 결과
    - 행 = 샘플, 열 = 해당 생선일 확률
    
    ```java
    #'Bream' 'Parkki' 'Perch' 'Pike' 'Roach' 'Smelt' 'Whitefish'
    [[0.     0.     1.     0.     0.     0.     0.    ]   #perch
     [0.     0.     0.     0.     0.     1.     0.    ]   #smelt 
     [0.     0.     0.     1.     0.     0.     0.    ]   #pike
     [0.     0.     0.6667 0.     0.3333 0.     0.    ]   #perch
     [0.     0.     0.6667 0.     0.3333 0.     0.    ]]  #perch
    ```
    

### 7. 결과

**K-최근접 이웃의 다중 분류는 조합이 너무 단순하게 나오게 됨**

## 로지스틱 회귀

몇 퍼센트의 확률로 생선이 분류되는지 실습 

```python
z = a무게 + b길이 + c대각선 + d높이 + e두께 + f
```

- 여기서 z값을 그대로 사용하면 회귀가 됨
- 분류로 사용하기 위해 확률로 변경해야 하는데 -무한대 ~ +무한대의 값을  0~1의 값으로 변경해야함
    
    *시그모이드 함수(=로지스틱 함수)
    
    - -무한대 ~ +무한대의 값을  0~1의 값으로 변경
    - 0.5를 기준으로 크면 양성, 낮으면 음성
- `sklearn`의 `predict`메소드는 `z`값만 보고 판단하고 `predict_proba`메소드는 파이값을 계산해서 평균값을 출력한다.

### 1. 데이터 준비

- 훈련 셋이서 도미와 빙어의 행만 가져오기

```java
# Bream 도미, Smelt 빙어
bream_smelt_indexes = (train_target == 'Bream') | (train_target == 'Smelt')
train_bream_smelt = train_scaled[bream_smelt_indexes]
target_bream_smelt = train_target[bream_smelt_indexes]
```

- bream_smelt_indexes
    - 도미와 빙어일 경우에만 True 그외는 모두 False
    
    ```java
    [ True False  True False False False False  True False False False  True
    ...
    ]
    ```
    
- train_bream_smelt
    
    ```java
    [[ 0.91965782  0.60943175  0.81041221  1.85194896  1.00075672]
     [-1.0858536  -1.68646987 -1.70848587 -1.70159849 -2.0044758 ]
     [ 0.63818253  0.56257661  0.73223951  1.64473401  0.50705737]
    ...
    ]
    ```
    

### 2. 데이터 훈련

- 로지스틱 회귀도 선형으로 되어있기 때문에 Linear에 있음

```java
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(train_bream_smelt, target_bream_smelt)
```

### 3. 예측 확인

- train_bream_smelt에 있는 처음 5개의 샘플 예측

```java
print(lr.predict(train_bream_smelt[:5]))
# ['Bream' 'Smelt' 'Bream' 'Bream' 'Bream']
```

- predict_proba() 결과의 순서 확인

```java
print(lr.classes_)
```

- 결과
    
    ```java
    ['Bream' 'Smelt']
    ```
    
- predict_proba()메서드로 예측 확률 출력

```java
print(lr.predict_proba(train_bream_smelt[:5]))
```

- 결과
    - 첫번째 열 = 음성 클래스일 확률
    - 두번째 열 = 양성 클래스일 확률
    
    ```java
    # ['Bream' 'Smelt']
    [[0.99759855 0.00240145]
     [0.02735183 0.97264817]
     [0.99486072 0.00513928]
     [0.98584202 0.01415798]
     [0.99767269 0.00232731]]
    ```
    
    - 두번째 생선만 빙어일 확률이 높은것으로 나타남

### 4. 계수 확인

```java
print(lr.coef_, lr.intercept_)
# [[-0.4037798  -0.57620209 -0.66280298 -1.01290277 -0.73168947]] [-2.16155132]
```

- 학습을 통해 나온 기울기와 y절편 확인
    - 기울기(가중치) = lr.coef_
        - [[-0.4037798  -0.57620209 -0.66280298 -1.01290277 -0.73168947]]
    - y절편 = lr.intercept_
        - [-2.16155132]
- 즉 식은 아래와 같다
    
    ```java
    -0.4037798*무게 -0.57620209*길이 -0.66280298*대각선 -1.01290277*높이 -0.73168947*두께 -2.16155132
    ```
    

### 5. z값을 시그노이드 함수에 넣어보기

z값 출력

```java
decisions = lr.decision_function(train_bream_smelt[:5])
print(decisions)
# **[-6.02927744  3.57123907 -5.26568906 -4.24321775 -6.0607117 ]**
```

- decision_function: z값 출력 용도

위에서 나온 z값을 시그노이드 함수에 넣어서 앞에서 나온 확률과 동일한지 확인 

```java
from scipy.special import expit
print(expit(decisions))
# [0.00240145 0.97264817 0.00513928 0.01415798 0.00232731]
```

- expit(): 시그노이드 함수
- 위에서 출력한 양성클래스의 값과 완전히 동일하다는 걸 확인할 수 있음(음성은 1에서 빼기만 하면 되기 때문에 따로 출력 안됨)

## 다중 분류 로지스틱 회귀

다중 분류 로지스틱 회귀를 이용해 위에 처럼 2개의 생선을 뽑지않고 전체 7개의 생선으로 분류해본다.

### 1. 다중 분류 로지스틱 회귀 훈련

```java
lr = LogisticRegression(C=20, max_iter=1000)
lr.fit(train_scaled, train_target)

print(lr.score(train_scaled, train_target)) # 0.9327731092436975
print(lr.score(test_scaled, test_target)) # 0.925
```

- LogisticRegression클래스
    - 기본적으로 반복 알고리즘을 사용한다.
    - max_iter 매개변수에서 반복 횟수를 지정할 수 있으며 기본값은 100이다.
    - max_iter가 모자르면 아래와 같이 오류가 생성된다.
        
        ```java
        lr = LogisticRegression(C=20)
        lr.fit(train_scaled, train_target)
        
        # ConvergenceWarning: lbfgs failed to converge (status=1):
        STOP: TOTAL NO. of ITERATIONS REACHED LIMIT.
        ```
        
    - C값
        - LogisticRegression은 기본적으로 L2 규제(릿지, 가중치의 제곱)를 사용한다.
        - 규제강도 조절을 위해 C값을 사용한다.(C값이 높을수록 규제 낮음)
        - 기본 값 = 1
        - 20으로 늘려서 규제를 풀어주고 복잡한 모델이 될 수 있도록 함
        

### 2. 예측 확인

```java
print(lr.predict(test_scaled[:5]))
# ['Perch' 'Smelt' 'Pike' 'Roach' 'Perch']

proba = lr.predict_proba(test_scaled[:5])
print(lr.classes_)
print(np.round(proba, decimals=3))
```

- 결과
    
    ```java
    ['Bream' 'Parkki' 'Perch' 'Pike' 'Roach' 'Smelt' 'Whitefish']
    [[0.    0.014 0.841 0.    0.136 0.007 0.003]
     [0.    0.003 0.044 0.    0.007 0.946 0.   ]
     [0.    0.    0.034 0.935 0.015 0.016 0.   ]
     [0.011 0.034 0.306 0.007 0.567 0.    0.076]
     [0.    0.    0.904 0.002 0.089 0.002 0.001]]
    ```
    

### 3. 계수 및 y절편 확인

```java
print(lr.coef_.shape, lr.intercept_.shape) 
# (7, 5) (7,)
```

- 7의 행과 5개의 열이 있는 행열이 나오게 된다.
- 다중분류는 클래스마다 z값을 계산하게 되어 가장 큰 z값을 출력하는 클래스가 예측 클래스가 된다. (이진 분류를 여러번 실행해서 다중분류 실행)
    - A, B
- 확률 계산 방법
    - 이진 분류 로지스틱: z값을 0과 1사이의 값으로 반환
    - 다중 분류 로지스틱: 소프트 맥스 함수를 사용하여 7개의 z값 을 이용해 확률을 계산

### 4. 소프트맥스 함수를 이용해 확률로 변경

소프트맥스 함수: 지수함수로 구한부분을 Sum값으로 나누기(일종의 정규화)

```java
decision = lr.decision_function(test_scaled[:5])
print(np.round(decision, decimals=2))
```

- 결과
    
    ```java
    [[ -6.5    1.03   5.16  -2.73   3.34   0.33  -0.63]
     [-10.86   1.93   4.77  -2.4    2.98   7.84  -4.26]
     [ -4.34  -6.23   3.17   6.49   2.36   2.42  -3.87]
     [ -0.68   0.45   2.65  -1.19   3.26  -5.75   1.26]
     [ -6.4   -1.99   5.82  -0.11   3.5   -0.11  -0.71]]
    ```
    

### 5. 소프트맥스 함수 계산

```java
from scipy.special import softmax
proba = softmax(decision, axis=1)
print(np.round(proba, decimals=3))
```

- 결과
    
    ```java
    [[0.    0.014 0.841 0.    0.136 0.007 0.003]
     [0.    0.003 0.044 0.    0.007 0.946 0.   ]
     [0.    0.    0.034 0.935 0.015 0.016 0.   ]
     [0.011 0.034 0.306 0.007 0.567 0.    0.076]
     [0.    0.    0.904 0.002 0.089 0.002 0.001]]
    ```
    
    위에서 구한 proba배열과 일치하는거 확인 가능
