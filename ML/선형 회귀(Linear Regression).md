# 선형 회귀(Linear Regression)

## 선형 회귀

선형회귀는 한개 이상의 독립변수 x와 y의 선형관계를 모델링 함.

*독립 변수: 다른 변수의 값을 변하게 하는 변수 x

*종속 변수: 변수 x의 값에 의해 종속적으로 변하는 변수 y

## 단순 선형 회귀(Simple Linear Regression Analysis)

- 독립 변수 x가 한 개인 선형 회귀
    
    ```python
    y = wx + b
    ```
    

## 다중 회귀 ****분석(Multiple Linear Regression Analysis)****

- 결과 값에 영향을 미치는 독립변수가 여러 개 일때
    
    ```python
    y = w1x1 + w2x2 + ... + b
    ```
    
    - 다항 = ploy, 다중 = multiple

# 선형 회귀 실습

농어 길이에 따른 무게를 찾기 위한 선형회귀모델

### 1. 농어 데이터

```python
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

### 2. 데이터 훈련 셋과 테스트셋 준비

```python
from sklearn.model_selection import train_test_split

train_input, test_input, train_target, test_target = train_test_split(perch_length, perch_weight, random_state = 42)
```

- 임의의 값 42

### 3. sklearn의 LinearRegression을 이용한 선형 회귀 모델 훈련

- 농어무게 = w*농어길이 + b

```python
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(train_input, train_target)

# 50cm 농어에 대한 예측 -> 1.2kg정도 나옴
print(lr.predict([[50]])) # [1241.83860323]

#
print(lr.coef_, lr.intercept_) # [39.01714496] -709.0186449535477
```

- `lr.coef_`, `lr.intercept_`: 내가 설정한 값이 아닌 모델이 학습한 값 뒤에는 언더바(_)를 붙여서 표시함
- 학습을 통해 나온 기울기와 y절편
    - 기울기 = `lr.coef_` = [39.01714496]
    - y 절편 = `lr.intercept_` = -709.0186449535477
- 기울기값이 numby array로 되어있는 이유: 여러 개의 특성을 사용할 경우 기울기의 계수가 많아짐

### 4.  학습한 선형 회귀모델 확인

```python
import matplotlib.pyplot as plt 

# 훈련 셋의 산점도
plt.scatter(train_input, train_target)

# 15~50까지의 1차 방정식 그래프
plt.plot([15, 50], [15*lr.coef_ + lr.intercept_, 50*lr.coef_ + lr.intercept_])

# 50cm 농어 데이터는 삼각형으로 표시
plt.scatter(50, 1241.8, marker='^')
plt.show()

print(lr.score(train_input, train_target)) # 0.939846333997604
print(lr.score(test_input, test_target)) # 0.8247503123313558
```

![image](https://user-images.githubusercontent.com/74139727/221748117-3038d1fa-af55-42f4-b27d-edecd5b4fb84.png)


- 훈련 셋과 테스트 셋의 점수가 둘다 낮은 축에 속하여(테스트셋의 score가 최근접 회귀보다 낮음⇒0.97) “과소 적합”이 되었을 가능성이 높음
- 과소적합과 과대적합을 판단할 때는 상대적으로 판단하는 것이 좋음
- 문제파악
    - 왼쪽에 무게가 음수로 나온 것을 확인할 수 있음
    - 선점도를 확인하면 직선이기 보다는 약간의 곡선인 것을 확인 할 수 있음 ⇒ 2차 방정식 이용

### 5. 다항 회귀로 학습을 위한 데이터 셋 준비

- 무게 = a*길이^2 + b*길이 + c
- x^2 부분의 값을 기존에 진행했던 LinearRegression 클래스에 넣어주면 자동으로 구현됨

```python
train_poly = np.column_stack((train_input**2, train_input))
test_poly = np.column_stack((test_input**2, test_input))

print(train_poly)
[[ 384.16   19.6 ]
 [ 484.     22.  ]
 [ 349.69   18.7 ]
...
]
```

### 6. 다항 회귀 모델 훈련

```python
lr = LinearRegression()
lr.fit(train_poly, train_target)

# 50cm 농어 확인 1.5kg 예측
print(lr.predict([[50**2, 50]])) # [1573.98423528]

print(lr.coef_, lr.intercept_) # [  1.01433211 -21.55792498] 116.0502107827827
```

- lr.coef_: [  1.01433211 -21.55792498]
    - 제곱항을 추가 했기 때문에 계수가 2개가 된 것을 확인할 수 있음
- y = 1.01x^2 - 21.6x +116.05

### 7. 다항 회귀 훈련 결과 확인

```python
# 15~50까지의 배열을 만들어서 그래프 그리기
point = np.arange(15, 50)

# 훈련세트의 선점도 그리기
plt.scatter(train_input, train_target)

# 15~49까지 2차 방적식 그래프 그리기
plt.plot(point, 1.01*point**2 - 21.6*point + 116.05)

# 50cm 농어 데이터
plt.scatter([50], [1574], marker='^')
plt.show()

print(lr.score(train_poly, train_target)) # 0.9706807451768623
print(lr.score(test_poly, test_target)) # 0.9775935108325122
```

- 앞선 선형 회귀 모델보다 점수가 높아진 걸 확인할 수 있지만 test 셋의 점수가 살짝 높은걸 봐서는 조금 더 모델을 복잡하게 훈련을 시킬 필요가 있음
