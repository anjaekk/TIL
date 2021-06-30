장고를 이용하여 get 요청을 보냈을 때 json response 형식에 대해 공부하여 정리하고자 한다.

http client인 `httpie`를 이용하여 아래의 그림의 `actor` 형식을 목표로 코드를 작성하도록 한다. 우선 해당 내용의 데이터 모델은 `다:다` 혹은 `1:다`에서 "다"의 데이터를 가져올 때 사용할 수 있다. 아래의 json response의 `"actor":["승우", "강호", "태희"]`와 같이 한 `key값`에 리스트형식으로 들어가게 하는 것을 목표로 한다. 

- **결과**

![](https://images.velog.io/images/anjaekk/post/0c17a947-f89b-4c1c-990e-a5f14e78691e/image.png)

**해당 코드**

- **models.py**
```python
# models.py

from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField, IntegerField
from django.db.models.fields.related import ForeignKey

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=45)
    release_date = models.DateField()
    running_time = models.IntegerField()

    class Meta:
        db_table = "movies"


class Actor(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    movies = models.ManyToManyField(Movie, related_name='actors')

    class Meta:
        db_table = "actors"

```
- **views.py**
```python
# views.py


import json
from django.http import JsonResponse
from django.views import View
from movies.models import Movie, Actor


class MoviesView(View):
    def get(self, request):
        results = []
        movies = Movie.objects.all()
        for movie in movies:
            actor_arr = []
            actors = movie.actors.all()
            for i in actors:
                actor_arr.append(i.first_name)
            results.append({
                'title' : movie.title,
                'release_date' : movie.release_date,
                'running_time' : movie.running_time,
                'actor' : actor_arr
            })
        return JsonResponse({'results':results}, status=200)
```

여기서 확인해야할 부분은 movie입장에서 actor를 가져올 때이다. 코드를 하나하나 풀어보자.

1. json response로 보내줄 빈 리스트 형식의 results를 만들어준다.
```python
results = []
```

2. Movie의 모든 쿼리셋을 가져와 movies라는 변수에 담고 그 movies를 이용해 for문을 돌려준다. 
```python
movies = Movie.objects.all()
for movie in movies:
```

3. 한 movie에 해당하는 여려명의 actor를 가져오기 위한 리스트인 actor_arr를 만들어준다. 그리고 아까 for문을 통해 가져왔던 movie에 해당하는 actors를(model에서 related_name='actors'로 속성값을 넣어줌) 모두 가져온다. actors 변수에 넣고 for문을 돌려 아까 만든 actor_arr에 넣는다. 
여기서 append할 때 해당 actor의 first_name 데이터를 가져온다.
```python
actor_arr = []
actors = movie.actors.all()
for i in actors:
   actor_arr.append(i.first_name)

```

4. 그 외의 데이터들과 만든 actor_arr를 아까 만든 results에 넣어주고
```python
results.append({
   'title' : movie.title,
   'release_date' : movie.release_date,
   'running_time' : movie.running_time,
   'actor' : actor_arr
})

```

5. json형식으로 반환한다.
```python
return JsonResponse({'results':results}, status=200)
```

위와 같은 방법으로 for문을 이중으로 돌려 그 값만 가져오고 그 값을 빈 리스트에 넣게되면 json으로 reponse될 때 `"actor":["승우", "강호", "태희"]`와 같이 한 리스트에 값들이 모두 들어가게 된다.

---

만약 위에처럼 한 컬럼의 값들이 합쳐서 나오는게 아닌 모두 따로 딕셔너리형태로 나오길 원한다면 다음과 같이 코드를 작성할 수 있다.

**그 외의 코드**
- **views.py**
```python
# views.py

class MoviesView(View):
    def get(self, request):
        movies = Movie.objects.all()
        results = []
        for movie in movies:
            results.append({
                'title' : movie.title,
                'release_date' : movie.release_date,
                'running_time' : movie.running_time,
                'actor' : list(movie.actors.values('first_name'))
            })
        return JsonResponse({'results':results}, status=200)
```

- **결과**
![](https://images.velog.io/images/anjaekk/post/d9eb2787-1e44-4217-a695-9a3d70971644/image.png)

value값이 하나하나 딕셔너리에 들어가서 `{first_name": "승우"}`로 반환되는 걸 확인할 수 있다. 

- **values_list로 가져오면 안될까?**
아까 for문을 중첩해서 하나의 리스트의 값들로 가져올 때 만약 actors를 all()이 아닌 values_list로 가져올 순 없을까? 딕셔너리의 값들을 리스트로 가져오는 것이니 뭔가 그럴듯 해보인다! 변경된 부분만 보자면 아래와 같다. 애초에 가져올 때 values_list의 'first_name'을 찾아 가져오고 append할 때는 그 값만 넣어주는 것으로 변경했다.

- **views.py**
```python
for movie in movies:
    actors = movie.actors.values_list('first_name')
    actor_arr = []
    for i in actors:
        actor_arr.append(i)
```

- **결과**

![](https://images.velog.io/images/anjaekk/post/c48223b1-83c3-49d1-b967-9bf0f1f2dee4/image.png)

그렇게 하게되면 값들이 하나의 리스트안에 담기는 것이 아닌 값들이 각각의 리스트에 들어있는 것을 확인 할 수 있다. 
그 이유는 values_list는 이렇게 하나의 컬럼에서 여러개의 값을 가져올 때가 아닌 'first_name'과 'last_name'과 같이 2개 이상의 컬럼에서 값을 가져올 때 사용하기 때문이다. 

- **views.py**
```python
actors = movie.actors.values_list('first_name', 'date_of_birth')
```

- **결과**

![](https://images.velog.io/images/anjaekk/post/a11e6c30-59f4-485a-8d66-059fff7a13f7/image.png)

위의 예시에서는 'last_name'을 가져오니 보기 헷갈릴 것 같아 'date_of_birth'로 가져왔다. 여러개의 컬럼에서 데이터를 가져올 때 values_list를 쓰니 보기 편해진 것 같다.
