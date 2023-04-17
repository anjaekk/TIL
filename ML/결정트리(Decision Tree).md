# 결정트리(Decision Tree)

<br/>

## 정의

- 분류와 회귀에 사용되는 지도학습 방법
- 결정 트리는 불순도를 최소화(순도를 최대화)하고 정보 이득을 최대화하는 방향으로 학습을 진행

<br/>

## 특징

- 시각화가 가능하다
- 수치형과 범주형 데이터 모두를 다룰 수 있다
- 스케일을 조정할 필요가 없음(스케일에 구애 받지 않음)
    - 해당 특성 값에 대한 비교만 수행하여 분기
- 불순도를 기준으로 브랜치를 나누게 됨
- 항상 축에 평행하게 데이터를 나눌 수 있음
- 특성 중요도(feature importance)를 출력 가능
- 앙상블 모델을 만들 수 있음

<br/>

## 결정트리의 분류와 회귀

- 분류: 리프노드의 값이 예측 값이 됨
- 회귀: 리프노드들의 평균 값이 예측 값이 됨

<br/>

## 결정트리의 구조
<img src="https://user-images.githubusercontent.com/74139727/232351654-537fff9f-8dba-4cef-a178-c9b84e1fc8b3.png" width="600"/>

<br/>

## 결정트리 분석 절차

1. 데이터를 두 개의 집단으로 잘 분할하는 특성과 분할점을 선택
    - 두 집단의 순도(purity)가 최대화 되는 특성과 분할점으로 선정
2. 선정된 특성과 분할점을 이용하여 데이터를 두개의 집단으로 분할
3. 분할작업은 순도가 일정 기준 이상으로 증가하지 않을 때까지 반복

<br/>

## 특성 중요도(Feature importance)

선형모델에서 특성과 타겟과의 관계를 확인하기 위해 회귀계수를 확인하는 것처럼 결정 트리에서는 특성중요도를 사용한다. 특성 중요도는 0과 1 사이의 양수 값을 가지며 특성 중요도가 높을 수록 가장 먼저 분기에 사용된다. 

- 0: 해당 특성이 전혀 사용되지 않음
- 1: 해당 특성으로 완벽하게 타깃 클래스를 예측

<br/>

## 불순도(Impurity)

- 해당 범주 안에 서로 다른 데이터가 얼마나 섞여 있는가
    
    <img src="https://user-images.githubusercontent.com/74139727/232351678-01ff154c-6431-4218-bc49-a9daa2109037.png" width="500"/>
    
    - A의 불순도가 더 높다.

<br/>

## 불순도 측정 지표

불순도를 수치적으로 나타내는 대표적은 불순도 함수는 지니지수와 엔트로피 지수가 있다. 

결정트리에서 분기를 할 때 불순도 함수의 값이 줄어드는 방향으로 트리를 형성한다.

<br/>

### 지니 지수(Gini)

- CART(Classification and Regression Trees) 에서 쓰는 지수
- 지니 불순도 = 1-(음성클래스 비율 제곱 + 양성클래스 비율 제곱)
- 부모의 불순도 - (왼쪽 노드의 샘플수 / 부모의 샘플 수)*왼쪽 노드의 불순도 - (오른쪽 노드의 샘플수 / 부모의 샘플 수) * 오른쪽 노드의 불순도
- 부모의 지니 불순도에서 자식의 지니 불순도를 뺐을 때 그 차이가 크게 나오는 방향으로 노드를 분할함
- 양성클래스와 음성클래스가 정확히 50:50 나뉘어져 있을 경우 지니 불순도는 0.5가 된다
- 한쪽 클래스로 이루어져 있을 경우에는 지니 불순도는 0으로 순수노드 혹은 퓨어 노드라고 부른다.(= 불순도가 낮음)

- 10명의 사람을 성별과 결혼 여부로 분류하면

<img src="https://user-images.githubusercontent.com/74139727/232351690-a3c3acfd-9a1e-4441-bba4-760703aee3de.png" width="700"/>

- *출처(유튜브 - 강서대학교 빅데이터경영학과 이상철 교수)*

<img src="https://user-images.githubusercontent.com/74139727/232351705-2f046555-6050-4ea4-9223-ac63d2993728.png" width="700"/>

- *출처(유튜브 - 강서대학교 빅데이터경영학과 이상철 교수)*
- 성별은 지니지수 0.167, 결혼여부는 지니지수 0.48로 성별에 따른 분류가 더 불순도가 낮기 때문에 성별로 분류하게 된다.

<br/>

### 엔트로피 지수(Entropy)

- ID3(Iterative Dichotomiser 3) 에서 사용하는 지수
- 불순도가 낮을 수록 엔트로피가 낮음
- entropy = 1 → 불순도 최대, entropy = 0 → 순도 최대

<br/>

### 정보 이득(IG; Information gain)

- 분기 이전의 엔트로피와 분기 이후의 엔트로피를 뺀 수치
    
    ```java
    information gain = entropy(parent) - [weighted average] entropy(childeren)
    ```
    
    - entropy(parent): 분기 이전 엔트로피
    - entropy(childeren): 분기 이후 엔트로피
    - [weighted average] entropy(childeren): 분기 이후 엔트로피의 가중 평균
- 정보이득이 높은 노드 선택

<br/>

## 가지치기(Pruning)

- 리프 노드가 퓨어노드가 될 수 있도록 트리를 성장시키지만 너무 많은 트리가 생기가 되면 이렇게되면 과대적합 문제가 생길 수 있다.
    - 순수노드로 이루어진 트리는 훈련세트에 100% fitting
        
        <img src="https://user-images.githubusercontent.com/74139727/232351796-117e014a-ea90-46e6-9608-d9c37d1ba516.png" width="600"/>

        
        <img src="https://user-images.githubusercontent.com/74139727/232351833-6bb14afa-4467-4621-a918-99090c23ee0f.png" width="600"/>

        
        <img src="https://user-images.githubusercontent.com/74139727/232351883-db76c547-9776-48b3-8b33-e8309e7d7b4a.png" width="600"/>
        
        <img src="https://user-images.githubusercontent.com/74139727/232351894-5a110755-6058-4789-910c-ab67d20397df.png" width="600"/>

        
- 과대적합을 회피하기 위해 대표적으로 사용하는게 가지치기
    - 결정트리에는 선형함수를 가정하는 L2 규제와 L1규제를 사용할 수 없음
- 가지치기는 훈련세트의 정확도가 떨어지지만 테스트 세트의 성능을 개선 시킨다.

<br/>

### 가지치기 하이퍼 파라미터

1. `max_depth`
    - 트리 깊이 제한
    - max_depth=4
2. `max_leaf_nodes`
    - 노드 개수 제한
3. `min_samples_split`
    - 샘플 개수 제한
4. `min_samples_leaf`
    - 노드가 되려면 가지고 있어야할 최소 샘플 수 제한

<br/>

## 결정트리의 한계

1. 과적합 발생 확률이 높아 가지치기를 통해 최적화를 해야한다. 하지만 최적화를 하더라도 성능이 좋지 않아 앙상블기법을 단일 결정트리의 대안으로 많이 사용한다.
2. 회귀를 통해 예측시 가지고 있는 데이터의 마지막 데이터를 이용해 예측하다보니 모델이 가진 데이터 범위 밖으로 나가게되면 새로운 데이터를 예측할 수 없음


<br/>

출처

*[https://bkshin.tistory.com/entry/머신러닝-4-결정-트리Decision-Tree](https://bkshin.tistory.com/entry/%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D-4-%EA%B2%B0%EC%A0%95-%ED%8A%B8%EB%A6%ACDecision-Tree)*

지니 지수 계산 방법 - *[https://lucy-the-marketer.kr/ko/growth/decision-tree-and-impurity/](https://lucy-the-marketer.kr/ko/growth/decision-tree-and-impurity/)*

*[https://tensorflow.blog/파이썬-머신러닝/2-3-5-결정-트리/](https://tensorflow.blog/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D/2-3-5-%EA%B2%B0%EC%A0%95-%ED%8A%B8%EB%A6%AC/)*

엔트로피 계산 방법 - *[https://needjarvis.tistory.com/718#:~:text=정보 이득(Information Gain)은,때 사용하는 기댓값이다](https://needjarvis.tistory.com/718#:~:text=%EC%A0%95%EB%B3%B4%20%EC%9D%B4%EB%93%9D(Information%20Gain)%EC%9D%80,%EB%95%8C%20%EC%82%AC%EC%9A%A9%ED%95%98%EB%8A%94%20%EA%B8%B0%EB%8C%93%EA%B0%92%EC%9D%B4%EB%8B%A4).*
