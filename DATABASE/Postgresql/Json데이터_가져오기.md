Json 연산자
`->` : key형태로 json객체 반환
`->>` : text형태로 json객체 반환

### key형태
product 테이블, info 컬럼에 {"name": "milk"}라는 데이터들이 있을 때
```
SELECT info -> 'name'
FROM product;
```
#### 반환값
```
"milk"
```

### text형태
```
SELECT info ->> 'name'
FROM product;
```
#### 반환값
```
milk
```
