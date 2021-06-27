스타벅스 메뉴 데이터를 모델링을 하던 중 스타벅스 메뉴와 알러지 유발요인과의 `M:N 관계`를 정의하는 부분이 헷갈렸다. 그래서 블로그 정리를 통해 개념을 확실하게 짚고 넘어가고자 한다. 


## Model 구현
피자와 토핑의 관계를 예를 들어 알아보자.

![](https://images.velog.io/images/anjaekk/post/362d1678-7763-4359-b3ae-abfb9cb13f87/image.png)

위와 같이 포테이토 피자는 토핑의 id `1`, `2`, `3`을 가지고 있고 하와이안 피자는 토핑의 `2`, `3`, `4`를 가지고 있다. 즉, 피자는 여러 토핑을, 토핑은 여러 피자를 구성한다. 이러한 `M:N 관계`에서는 `중간 테이블(Intermediate Table)`을 이용하여 `1:N:1`의 관계를 만들어 준다. 즉, `M:N 관계`에서 `Foreign Key`로만 이루어진 중간테이블을 직접 만들 수도 있지만 `ManyToManyField`를 사용할 경우 자동으로 만들어지기 때문에 더욱 편리하게 모델을 구현할 수 있다. 

![](https://images.velog.io/images/anjaekk/post/a2c43407-2e6d-4ead-be6c-710b08c67839/image.png)

문제는 위와같은 상황에서 장고에서 관계 모델을 어떻게 정의하냐 인데 장고에서는 친절하게도 `중간 테이블(Intermediate Table)`을 자동으로 만들어 준다. 장고의 `models.py` 에서 모델의 속성을 구성해보자.

- <span style="color:olivedrab">**pizza 앱의 models.py**</span>

```python
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=100)
    toppings = models.ManyToManyField(Topping, related_name='pizzas')
    
    
    def __str__(self):
        return self.name

```
`ManyToManyField`는 어느 쪽에 넣는 것은 상관없지만 두 테이블 모두에 넣어서는 안된다. 여기서는 토핑이 들어갈 피자를 선택하는 것이 자연스러우므로 Pizza 클래스에 `ManyToManyField`를 넣어줬다. 이 후 테이블 `migration`을 만들어주고 `migrate`를 한다.

> **related_name**
>만약 Topping에 입장에서 참조할때(역참조) `Topping.pizza_set.all()`과 같이 역참조 매니저의 기본값으로 `pizza_set`을 사용하지만(모델의 소문자 이름_set) `related_name`을 사용하게되면 역참조 매니저의 이름을 `Topping.pizzas.all()`로 좀 더 알아보기 쉬운 참조명을 설정할 수 있다.


## Database 입력
그 후 장고 shell로 이동하여 데이터를 입력해준다.

- <span style="color:olivedrab">**django shell**</span>

```
# 만든 model을 import 해준다.
>>>from pizza.models import *   

# 피자 테이블의 속성을 넣고 변수에 담는다.
>>>p1 = Pizza.objects.create(name="포테이토 피자")
>>>p2 = Pizza.objects.create(name="하와이안 피자")

# 토핑 테이블의 속성을 넣고 변수에 담는다.
>>>t1 = Topping.objects.create(name="포테이토")
>>>t2 = Topping.objects.create(name="치즈")
>>>t3 = Topping.objects.create(name="올리브")
>>>t4 = Topping.objects.create(name="파인애플")

# 포테이토 피자에 포테이토, 치즈, 올리브를 넣어준다.
>>>p1.toppings.add(t1)
>>>p1.toppings.add(t2)
>>>p1.toppings.add(t3)

# 하와이안 피자에 치즈, 올리브, 파인애플을 넣어준다.
>>>p2.toppings.add(t2)
>>>p2.toppings.add(t3)
>>>p2.toppings.add(t4)
```

## QuerySet 확인

위와 같이 입력 후 쿼리 셋을 확인해보자

- <span style="color:olivedrab">**포테이토 피자의 QuerySet**</span>
```
>>>p1.toppings.all()
# 결과
>>><QuerySet [<Topping: 포테이토>, <Topping: 치즈>, <Topping: 올리브>]>
```

- <span style="color:olivedrab">**하와이안 피자의 QuerySet**</span>
```
>>>p2.toppings.all()
# 결과
>>><QuerySet [<Topping: 치즈>, <Topping: 올리브>, <Topping: 파인애플>]>
```

그렇다면 토핑의 입장에서 확인해보자

- <span style="color:olivedrab">**치즈 토핑 QuerySet**</span>

```
>>>t2.pizzas.all()
# 결과
>>><QuerySet [<Pizza: 포테이토 피자>, <Pizza: 하와이안 피자>]>
```
포테이토 피자와 하와이안 피자 두 곳 모두에 치즈토핑이 들어가는 것을 확인 할 수 있다. _model을 작성할 때 `related_name='pizzas'`를 해주었기 때문에 pizzas로 찾을 수 있었다. _


## mySQL 테이블 확인

좀더 보기 편하게 mySQL을 이용하여 테이블들을 시각화해서 확인해보자.

- <span style="color:olivedrab">**mySQL에서 테이블 검색**</span>(use 해당 테이터베이스를 선택했다는 가정)
```
mysql>show tables;
```
![](https://images.velog.io/images/anjaekk/post/e6cca269-ee5c-4bd7-867a-5422badb5686/image.png)

테이블을 검색하면 분명 입력한 테이블은 2개이지만 pizza_toppings라는 `중간테이블`이 자동으로 생성된 것을 확인할 수 있다.

> models.py에 속성 생성시 class Meta를 이용하여 db_table 이름을 설정해주면 pizza_pizza는 pizza로 pizza_pizza_toppings은 pizza_toppings으로 설정해줄 수 있다.(물론 다른 이름으로도 가능!)

각 테이블들의 row값을 확인해보자.

![](https://images.velog.io/images/anjaekk/post/8aca994c-cfb7-4d73-aebc-351ea3281443/image.png)

![](https://images.velog.io/images/anjaekk/post/0c5d6d05-663d-4fc9-b42c-4aa545609296/image.png)

![](https://images.velog.io/images/anjaekk/post/dc1085db-41d3-4e80-97eb-78421c6a3704/image.png)

위와 같이 맨처음 표를 이용하여 작성한 테이블과 같게 작성된 것을 알 수 있다.

## ManyToManyField.through_fields
하지만 만약 위처럼 단순한 다대다관계로 중간테이블이 자동으로 만들어지는 경우가 아닌 중간테이블에 추가적인 값을 넣어줘야 하는 것처럼 **중간테이블을 custom하고 싶은 경우가 생길 것**이다. 이럴경우에는 `models.py`에 `중간테이블 class`를 지정해주고 거기에 `through값`을 넣어주면 된다.

```python
from django.db import models


class Topping(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
 
 
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    toppings = models.ManyToManyField(Topping, related_name='pizzas', through='Service')   
    # Service를 중간테이블로 지정
    
    def __str__(self):
        return self.name


class Servise(models.Model):
    pizza = models.ForignKey(Pizza, on_delete=models.CASCADE)
    topping = models.ForignKey(Topping, on_delete=models.CASCADE)
    servise = models.BooleanField()
```
그렇게 되면 위와같이 중간모델을 직접 지정해줄 수 있게된다. 이외의 중간모델을 만드는데 있어 제약사항이 있으니 이는 [장고 documentation](https://docs.djangoproject.com/en/3.2/topics/db/models/)을 확인해보도록 하자.


> 참조
> 
> 🔗 [django documentation | Models](https://docs.djangoproject.com/en/3.2/topics/db/models/)
>
>🔗 [[Model] 관계](https://nachwon.github.io/django-relationship/)
