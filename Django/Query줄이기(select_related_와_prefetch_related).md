# <span style="color:MediumSeaGreen">Django의 Eager Loading</span>

이전 글에서 [Django-ORM의 Lazy-loading과 N+1 Query 문제](https://velog.io/@anjaekk/Django-Django-ORM%EC%9D%98-Lazy-loading%EA%B3%BC-N1-Query-%EB%AC%B8%EC%A0%9C)를 다뤘었다. 거기서 `Lazy-loading`으로 인한 `N+1 Query`문제가 발생한다고 했었고 이를 해결할 수 있는 방법으로 지금 당장 사용하지 않을 데잍도 포함하여 Query문을 실행하는 `Eager-loading`(즉시로딩)을 언급했었다. **`Djnago`의 `Eager-loading` 방법은 `select_related` 와 `prefetch_related` 메소드를 이용**하는 것이다. 이는 `SQL Query`문은 복잡하게 만들지만 다시 데이터베이스에 접근하지 않아 최종적으로는 Query의 갯수를 줄일 수 있고 이는 성능향상으로 이어질 수 있다.

# <span style="color:MediumSeaGreen">select_related 와 prefetch_related</span>

## 공통점
- 하나의 쿼리셋을 가져올 때 연관 Objects들을 미리 불러오는 메소드
DB에 connection하는 횟수를 줄여줘서 성능을 향상시킬 수 있다. 
- `result_cache`에 `cache`되기 때문에 중복호출을 방지할 수 있다.(`result_cache`: `SQL`의 수행결과 저장)


## 차이점
### select_related(정방향 참조)
`SQL`에서 `JOIN`을 사용해 데이터를 가져오기 때문에 Query문이 한 번만 실행된다. 
- 1:1 관계
- 1:N 관계에서 N이 사용

아래와 같은 모델이 있을 때를 가정해본다.

```python
class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'cities'


class Owner(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'owners'


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'restaurants'


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    restaurant = ManyToManyField(Restaurant, related_name="pizzas")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'pizzas'
```

여기서 1:1 관계의 `Restaurant`모델에서 정참조인 `Owner`의 `city`를 가져온다고 가정하겠다.

#### select_related()를 사용하지 않은 경우

```
restaurant = Restaurant.objects.get(id=1)
owner = restaurant.owner
city = owner.city
```
`select_related` 메소드를 사용하지 않은 경우 다음과 같이 총 3번의 쿼리를 날리는 것을 확인 할 수 있다.

```
{'sql': 'SELECT `restaurants`.`id`, `restaurants`.`name`, `restaurants`.`owner_id` FROM `restaurants` WHERE `restaurants`.`id` = 1 LIMIT 21', 'time': '0.002'},
{'sql': 'SELECT `owners`.`id`, `owners`.`name`, `owners`.`city_id` FROM `owners` WHERE `owners`.`id` = 1 LIMIT 21', 'time': '0.005'}, 
{'sql': 'SELECT `cities`.`id`, `cities`.`name` FROM `cities` WHERE `cities`.`id` = 1 LIMIT 21', 'time': '0.001'}]
```
1. `Restaurant`모델에서 `id=1`인 `restaurant`를 가져오기 위한 query
2. 1번에서 가져온 `restaurant`의 `owner`를 가져오기 위한 query
3. 그 `owner`의 `city`를 가져오기 위한 query

#### select_related()를 사용한 경우
```python
restaurant = Restaurant.objects.select_related('owner__city').get(id=1)
owner = restaurant.owner
city = owner.city
```

`select_related` 메소드를 사용한 경우 아래와 같이 `INNER JOIN`을 사용하여 단 1개의 query만 날린 것을 확인할 수 있다.

```
 {'sql': 'SELECT `restaurants`.`id`, `restaurants`.`name`, `restaurants`.`owner_id`, `owners`.`id`, `owners`.`name`, `owners`.`city_id`, `cities`.`id`, `cities`.`name` FROM `restaurants` INNER JOIN `owners` ON (`restaurants`.`owner_id` = `owners`.`id`) INNER JOIN `cities` ON (`owners`.`city_id` = `cities`.`id`) WHERE `restaurants`.`id` = 1 LIMIT 21', 'time': '0.002'}]
```
이처럼 `select_related` 메소드를 사용한 경우 관련된 객체(`related objects`) 데이터들을 가져와 `cache`에 저장하게 되고 `cache`에 저장된 데이터를 사용하기 때문에 query를 다시 날릴 필요가 없게 된다.

### prefetch_related(역방향 참조)
관련된 테이블 2개를 각각 불러드려서 파이썬 단계에서 JOIN한다. 1:1, M:N등 모든 관계에서 사용가능 하지만 보통 `select_related`를 사용할 수 없는 M:N 관계에서 주로 사용한다. 
- M:N 관계
- 1:N 관계에서 1이 사용

`select_related` 예시에서 사용한 모델이라고 할때 M:N 관계인 `Restaurant`에서 Pizza를 가져오는 코드를 작성하여 호출되는 query문을 확인하도록 하겠다.

#### prefetch_related를 사용하지 않은 경우
```python
restaurants = Restaurant.objects.all()
for restaurant in restaurants:
    for pizza in restaurant.pizzas.all():
        print(restaurant.name+": "+pizza.name)
    print("")
    
# 결과
피자좋아: 포테이토
피자좋아: 페페로니
피자좋아: 고구마

맛있다요: 포테이토
맛있다요: 페페로니
맛있다요: 고구마

배고파아: 포테이토
배고파아: 페페로니
배고파아: 고구마
```
(`related_name="pizzas"`를 설정해줬기 때문에 `pizza_set`이 아닌 `pizzas`로 입력)

query문 확인
```
{'sql': 'SELECT `restaurants`.`id`, `restaurants`.`name`, `restaurants`.`owner_id` FROM `restaurants`', 'time': '0.002'},
{'sql': 'SELECT `pizzas`.`id`, `pizzas`.`name` FROM `pizzas` INNER JOIN `pizzas_restaurant` ON (`pizzas`.`id` = `pizzas_restaurant`.`pizza_id`) WHERE `pizzas_restaurant`.`restaurant_id` = 1', 'time': '0.006'}, 
{'sql': 'SELECT `pizzas`.`id`, `pizzas`.`name` FROM `pizzas` INNER JOIN `pizzas_restaurant` ON (`pizzas`.`id` = `pizzas_restaurant`.`pizza_id`) WHERE `pizzas_restaurant`.`restaurant_id` = 2', 'time': '0.001'}, 
{'sql': 'SELECT `pizzas`.`id`, `pizzas`.`name` FROM `pizzas` INNER JOIN `pizzas_restaurant` ON (`pizzas`.`id` = `pizzas_restaurant`.`pizza_id`) WHERE `pizzas_restaurant`.`restaurant_id` = 3', 'time': '0.001'}, 
{'sql': 'SELECT `pizzas`.`id`, `pizzas`.`name` FROM `pizzas` INNER JOIN `pizzas_restaurant` ON (`pizzas`.`id` = `pizzas_restaurant`.`pizza_id`) WHERE `pizzas_restaurant`.`restaurant_id` = 4', 'time': '0.001'}, 
{'sql': 'SELECT `pizzas`.`id`, `pizzas`.`name` FROM `pizzas` INNER JOIN `pizzas_restaurant` ON (`pizzas`.`id` = `pizzas_restaurant`.`pizza_id`) WHERE `pizzas_restaurant`.`restaurant_id` = 5', 'time': '0.001'}]
```
`prefetch_related` 메소드를 사용하지 않은 경우 
1. `restaurants`의 모든 데이터를 가져오는 query문
2. 그 `restaurants`의 각각마다 `pizza`를 가져오는 query문(저는 `restaurant` 테이블에 5개의 데이터를 넣어놔서 5번 실행)

이렇게 `N+1`의 query가 발생하는 것을 확인할 수 있다.(위 데이터로는 6개)



#### prefetch_related를 사용한 경우

`prefetch_related` 메소드를 사용한 경우를 확인해 보자. 위의 코드와 동일하나 `prefetch_related`메소드만 넣어줬다. 

```python
restaurants = Restaurant.objects.all().prefetch_related('pizzas')
for restaurant in restaurants:
    for pizza in restaurant.pizzas.all():
        print(restaurant.name+": "+pizza.name)
    print("")
```

해당의 쿼리를 확인해보면 아래와 같다.

```
{'sql': 'SELECT `restaurants`.`id`, `restaurants`.`name`, `restaurants`.`owner_id` FROM `restaurants`', 'time': '0.001'}, 
{'sql': 'SELECT (`pizzas_restaurant`.`restaurant_id`) AS `_prefetch_related_val_restaurant_id`, `pizzas`.`id`, `pizzas`.`name` FROM `pizzas` INNER JOIN `pizzas_restaurant` ON (`pizzas`.`id` = `pizzas_restaurant`.`pizza_id`) WHERE `pizzas_restaurant`.`restaurant_id` IN (1, 2, 3, 4, 5)', 'time': '0.002'}]
```

물론 두번째 query문이 복잡하고 길어지긴 했지만 단 2개의 query로 같은 결과를 낸 것을 확인할 수 있다. **`restaurant`를 모두 가져오는 query는 같지만 그 뒤 `pizza`데이터를 가져와 `result_cache`에 `caching`하게 되고 데이터베이스에 접근하지 않고도 `cache`에서 찾아 사용하게 된다.** 여기서 알 수 있는 것은 `prefetch_related` 메소드는 `main query`를 실행한 후 별도의 query를 따로 실행한다는 것이다._(추가 `query` 발생) _

그렇다면 1:1 관계에서 무조건 `Inner Join`으로 한번만 가져오는 `select_related`를 사용하는 것이 좋냐고 한다면 그건 아니다. `ORM` 조건이 복잡하거나 데이터 양이 방대한 경우에는 한 번에 Query를 전부 조회해서 가져오는 것보다 `prefetch_related` 메소드를 이용하여 두 번으로 나눠 각각 가져오는 것이 속도면에서 더 빠를 수도 있다. 이는 직접 대조해보며 어느 쪽이 성능면으로 나은지 확인 후 사용하는 것이 좋겠다.  


> 참조
> 
>🔗 [PyCon Korea2020-김성렬 | Django ORM (QuerySet)구조와 원리 그리고 최적화전략](https://www.youtube.com/watch?v=EZgLfDrUlrk&t=460s)
>
>🔗 [chrisjune | 당신이 몰랐던 Django Prefetch](https://medium.com/chrisjune-13837/%EB%8B%B9%EC%8B%A0%EC%9D%B4-%EB%AA%B0%EB%9E%90%EB%8D%98-django-prefetch-5d7dd0bd7e15)
>
>🔗 [jupiny | select_related와 prefetch_related](https://jupiny.com/2016/10/06/select_related-prefetch_related/)
