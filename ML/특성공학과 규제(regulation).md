# 특성공학과 규제(regulation)

## 다중 회귀 ****분석(Multiple Linear Regression Analysis)****

- 결과 값에 영향을 미치는 독립변수가 여러 개 일때
    
    ```python
    y = w1x1 + w2x2 + ... + b
    ```
    
    - 다항 = ploy, 다중 = multiple

## 특성공학
새로운 특성을 추가하거나 조합하는 행위
ML은 특성공학의 영향을 많이 받지만 딥러닝은 특성공학의 종류가 조금 달라지고 영향을 비교적 많이 받지 않는다. 


## 규제(regulation)

MSE(잔차 제곱합)을 이용해 구하는 선형회귀에서 알파항을 붙여 최적의 가중치와 편향을 찾기(가중치(기울기)를 작게 만들기)

### 1. 릿지(Ridge)

- L2라고도 불림
- 가중치의 제곱
- 규제의 강도가 있음(alpha 값)
    - 이 alpha값을 변경하면서 좋은 모델을 찾기 때문에 하이퍼 파라미터임
- 변수선택 불가능

### 2. 라쏘(Lasso)

- L1이라고도 불림
- 변수 선택 가능

# 실습

### 1. 판다스 설치

```python
pip install pandas
```

### 2. 데이터 준비

- 혼자 공부하는 머신러닝 + 딥러닝의 자료

```python
import pandas as pd

df = pd.read_csv("https://bit.ly/perch_csv")
perch_full = df.to_numpy()

print(perch_full)
```

### 3.  훈련 셋과 테스트 셋 준비

```python
from sklearn.model_selection import train_test_split
import numpy as np

perch_weight = np.array([5.9, 32.0, 40.0, 51.5, 70.0, 100.0, 78.0, 80.0, 85.0, 85.0, 110.0,
       115.0, 125.0, 130.0, 120.0, 120.0, 130.0, 135.0, 110.0, 130.0,
       150.0, 145.0, 150.0, 170.0, 225.0, 145.0, 188.0, 180.0, 197.0,
       218.0, 300.0, 260.0, 265.0, 250.0, 250.0, 300.0, 320.0, 514.0,
       556.0, 840.0, 685.0, 700.0, 700.0, 690.0, 900.0, 650.0, 820.0,
       850.0, 900.0, 1015.0, 820.0, 1100.0, 1000.0, 1100.0, 1000.0,
       1000.0]
       )

train_input, test_input, train_target, test_target = train_test_split(perch_full, perch_weight, random_state=42)
```

### 4. 다항 특성 생성

길이, 높이, 두께 이 3개가지의 특성만 이용하는 것이 아닌 이 특성들의 조합을 이용해 또 다른 특성들을 이용

```python
from sklearn.preprocessing import PolynomialFeatures

# degree=2 -> 제곱만을 이용해 특성을 만들기(기본값 2)
poly = PolynomialFeatures()
poly.fit(
    [[2, 3]]
)

print(poly.transform(
        [[2, 3]]
    )
) 
# [[1. 2. 3. 4. 6. 9.]]
```

- sklearn의 PolynomialFeatures 변환기 클래스를 이용해 특성의 경우의 수를 얻을 수 있음
- fit + transform을 합쳐서 fit_transform() 메서드가 존재하기도 함

위와 같이 특성을 만들 수 있는 PolynomialFeatures클래스를 이용해 특성 생성

```python
# 변환된 배열에서 1 빼기
poly = PolynomialFeatures(include_bias=False)

# 선형 회귀에서 사용한 train_input
poly.fit(train_input)

# train_poly numpy 배열
train_poly = poly.transform(train_input)

print(train_poly.shape) # (42, 9)

poly.get_feature_names_out()
# array(['x0', 'x1', 'x2', 'x0^2', 'x0 x1', 'x0 x2', 'x1^2', 'x1 x2', 'x2^2'], dtype=object)
```

- Include_bias: 회귀에서는 1을 사용하지 않기 때문에 제외
- *get_feature_names()메소드는 sklearn 1.0버전 이후 get_feature_names_out()으로 대체*

### 5. 태스트 셋으로 변환

```python
test_poly = poly.transform(test_input)

from sklearn.linear_model import LinearRegression

lr = LinearRegression()
lr.fit(train_poly, train_target)

print(lr.score(train_poly, train_target)) # 0.9903183436982124
print(lr.score(test_poly, test_target)) # 0.9714559911594132
```

### 6. 더 많은 특성으로 테스트

```python
poly = PolynomialFeatures(degree=5, include_bias=False)

poly.fit(train_input)
train_poly = poly.transform(train_input)
test_poly = poly.transform(test_input)

print(train_poly.shape) # (42, 55) -> 샘플이 42개인데 특성이 55개

lr.fit(train_poly, train_target)
print(lr.score(train_poly, train_target)) # 0.9999999999991109
print(lr.score(test_poly, test_target)) # -144.40579241220442
```

- PolynomialFeatures의 degree를 늘려서 더 많은 특성을 가지고 테스트
- 훈련 셋에서는 0.999…으로 굉장히 높게 나왔지만 테스트셋은 음수로 매우 안좋은 결과가 나옴(과대 적합)
- ⇒ 규제를 통해 적합한 가중치와 편향 찾아내야 함

### 7. 규제를 위한 표준화

```python
from sklearn.preprocessing import StandardScaler

ss = StandardScaler()
ss.fit(train_poly) # 평균과 표준편차를 구함

train_scaled = ss.transform(train_poly)
test_scaled = ss.transform(test_poly)
```

- 특성의 스케일이 비슷해야 특성에 곱해지는 기울기가 비슷해지기 때문에 표준화를 선행작업 해준다.

### 8. 릿지 회귀를 이용한 규제

```python
from sklearn.linear_model import Ridge

ridge = Ridge()
ridge.fit(train_scaled, train_target)

print(ridge.score(train_scaled, train_target)) # 0.9896101671037343

print(ridge.score(test_scaled, test_target)) # 0.9790693977615389
```

- 이전 그대로 특성은 여전히 55개이지만 릿지를 이용해 가중치가 편향되는 것을 막아 0.98이라는 높은 점수를 받을 수 있음
- Ridge()에서 매개변수로 alpha값(규제 강도)를 입력가능(기본값 1)
