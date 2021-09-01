# <span style="color:MediumSeaGreen">Django ORM</span>
**Django는 데이터베이스를 코드를 이용해 관리할 수 있도록 Mapping해주는 `ORM(Objects Relational Mapping)`을 이용해 데이터를 관리**한다. 즉 ORM은 Object와 데이터베이스를 연결해주는 역할을 한다고 할 수 있다. 

# <span style="color:MediumSeaGreen">ORM의 장단점</span>
## 장점
#### 1. SQL 쿼리문을 몰라도 쉽게 사용 가능하다.
`ORM`을 사용하게되면 `SQL`문을 사용하지 않고 Django의 경우 python을 이용하여 데이터베이스를 조작할 수 있기 때문에 코드가 직관적이고 이해하기 쉽다. 또한 `SQL`의 절차적, 순차적 접근이 아닌 객체 지향적 접근으로 생산성이 증가하게 된다.
#### 2. RDBMS의 종속성이 하락하게 된다.
ORM은 Object간 관계를 바탕으로 SQL문을 자동으로 생성하고 그 Object의 자료형 타입까지 사용할 수 있다. 그렇다보니 데이터베이스의 종류를 아에 다른 데이터베이스로 바꾼다고 하더라도 적은 리스크와 시간으로 변경할 수 있다.
#### 3. 유지보수 및 재사용이 편리하다.
Object와 테이블의 Mapping관계가 명확하여 언제든지 목적에 따라 유지보수와 재사용이 편리하다.
## 단점
#### 1. 반드시 효율적인 SQL로 변환해 주는 것은 아니다.
잘못된 설계를 하게되면 심각한 성능저하와 더불어 일관성이 무너지는 문제가 생길 수 있다.
#### 2. ORM 의존문제가 발생할 수 있다.
ORM은 프로젝트의 규모와 복잡성이 커질 수록 raw SQL문을 사용한 것보다 구현 난도가 올라가게되고 문제 발생시 대처에 어려움이 생길 수 있다.

# <span style="color:MediumSeaGreen">Lazy-loading</span>
Django의 ORM은 다른 `ORM`과 마찬가지로 `Lazy-loading`방식을 사용한다. `Lazy-loading`이란 `ORM`에서 명령을 실행할 때마다 데이터베이스에 접근하여 데이터를 가져오는 것이 아닌 모든 명령처리가 끝나고 **실제 데이터를 불러와야할 때** 데이터베이스 `Query`문을 실행하는 방식을 말한다. 

### Query문을 실행하는 시점
다음은 Django에서 `Query`문을 실행하는 시점(`QuerySet`을 불러올 때)이다.
**1. 슬라이싱(Slicing)**
**2. Pickling/Caching**
**3. `__repr()__`**
**4. len()**
**5. list()**
**6. bool()**
- if문을 사용해 `boolean`값을 확인하게 될 때 포함한다. 그러므로 찾는 값의 존재여부만 파악할 때는 if문을 사용하는 것보다 `.exists()`를 이용하여 확인하는 것이 성능면에서는 효율적이다._(하지만 그 값으로 `evaluation`을 해야할 경우에는 if문을 사용)_


> 📁 [When QuerySets are evaluated](https://docs.djangoproject.com/en/3.2/ref/models/querysets/#when-querysets-are-evaluated)

### Eager-loading
`Eager-loading`(즉시 로딩)은 `Lazy-loading`의 반대 개념이다. `Lazy-loading`은 `Query`문을 하나, 하나 실행하여 데이터를 가져온다면 Eager-loading은 **지금 당장 사용하지 않을 데이터도 포함하여 `Query`문을 실행하기 때문에 밑에 설명할 `Lazy-loading`의 `N+1`문제의 해결책으로 많이 사용하게 된다.** 
Django에서 `Eager-loading`을 실행하는 방법은 `select_related`  메소드와 `prefetch_related` 메소드를 사용한다. 이 두가지 메소드를 이용해 `Lazy-loading`의 성능이슈를 해결할 수 있는데 자세한 내용은 다음 블로그에서 설명하도록 하겠다.


# <span style="color:MediumSeaGreen">N+1 Query 문제</span>
`Lazy-loading`의 성능이슈인 `N+1 Query` 문제는 외래키(`Foreign Key`)를 참조해서 데이터를 가져올 때 발생한다. 

아래와 같이 `restaurant`와 `owner`가 1:1 관계인 모델이 있다고 가정하자

```

mysql> select * from restaurants;
+----+--------------+--------------+----------+
| id | name         | place        | owner_id |
+----+--------------+--------------+----------+
|  1 | 얌얌피자     | 서울         |        1 |
|  2 | 굿굿피자     | 인천         |        2 |
|  3 | 좋아좋아     | 부산         |        3 |
|  4 | 배고파아     | 제주         |        4 |
|  5 | 정통스       | 이탈리아     |        5 |
+----+--------------+--------------+----------+


mysql> select * from owners;
+----+------+-----+
| id | name | age |
+----+------+-----+
|  1 | 김   |  21 |
|  2 | 이   |  22 |
|  3 | 박   |  30 |
|  4 | 안   |  40 |
|  5 | 전   |  50 |
+----+------+-----+
```

다음과 같이 5개의 `restaurant`에서 `owner`의 이름을 가져오도록 하겠다.
```

>>> restaurants = Restaurant.objects.all()
>>>
>>> for restaurant in restaurants:
...     restaurant.owner.name

```

이때 발생한 쿼리를 확인해 보면 5개가 아닌 5+1인 6개의 쿼리가 날라간 것을 확인 할 수 있다. 
```
{'sql': 'SELECT `restaurants`.`id`, `restaurants`.`name`, `restaurants`.`owner_id`, `restaurants`.`place` FROM `restaurants`', 'time': '0.003'},
 {'sql': 'SELECT `owners`.`id`, `owners`.`name`, `owners`.`age` FROM `owners` WHERE `owners`.`id` = 1 LIMIT 21', 'time': '0.004'},
 {'sql': 'SELECT `owners`.`id`, `owners`.`name`, `owners`.`age` FROM `owners` WHERE `owners`.`id` = 2 LIMIT 21', 'time': '0.001'},
 {'sql': 'SELECT `owners`.`id`, `owners`.`name`, `owners`.`age` FROM `owners` WHERE `owners`.`id` = 3 LIMIT 21', 'time': '0.001'}, 
{'sql': 'SELECT `owners`.`id`, `owners`.`name`, `owners`.`age` FROM `owners` WHERE `owners`.`id` = 4 LIMIT 21', 'time': '0.001'}, 
{'sql': 'SELECT `owners`.`id`, `owners`.`name`, `owners`.`age` FROM `owners` WHERE `owners`.`id` = 5 LIMIT 21', 'time': '0.001'}]
```
맨 첫번 째 `Query`문은 전체 `restaurant`를 가져오고 그뒤 `owner`에서 5번 따로 가져오게 된다. 이는 가져오는 데이터가 많으면 많을수록 비효율적인 코드가 되기 때문에 위에서 언급한 `Eager-loading`을 통해 해결해야 한다. 



> 참조
> 
>🔗 [Django documantation](https://docs.djangoproject.com/en/2.2/topics/db/queries/)
>
>🔗 [queryset 파헤치기](https://cocook.tistory.com/52)
>
>🔗 [Django ORM 성능 튜닝](https://show-me-the-money.tistory.com/entry/Django-ORM-%EC%84%B1%EB%8A%A5-%ED%8A%9C%EB%8B%9D)
