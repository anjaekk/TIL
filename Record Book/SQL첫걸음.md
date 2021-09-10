# DB와 SQL
## 1. 데이터 베이스
### 1) DBMS
- 데이터를 효율적으로 관리하는 System
- 사용목적: 생산성 향상(CRUD의 간편함), 기능성(고속검색, 대용량 저장), 신뢰성
  \* _클러스터구성 = 스케일 아웃_: 하드웨어를 여러대로 구성하여 소프트웨어를 통해 확장성(Scalability), 부하분산(Load balancing) 구현
### 2) DB 종류
- 계층형, 관계형, 객체지향, XML, KVS(Key-value store)
### 3) DB server
- RDBMS는 클라이언트/서버 모델로 구성됨
- 클라이언트는 데이터베이스 서버에 접속해 SQL 명령을 실행하여 데이터베이스 조작 가능
\* 데이터베이스 서버에 접속할 때는 ID와 password를 이용한 사용자 인증이 필요함

## 2. SQL
### 1) SQL이란
 - 관계형 데이터베이스 조작 언어
 - IBM이 개발한 SEQUEL기반으로 만들어짐
### 2) SQL명령의 종류
(1) DML(Data Manipulation Language)
  - SQL의 가장 기본이 되는 명령어 Set
  - 데이터 조작시 사용(데이터 추가, 삭제 등)

(2) DDL(Data Definition Language)
  - 데이터베이스 객체(Object) 생성, 삭제 

(3) DCL(Data Control Language)
 - 트랜잭션을 제어하는 명령과 데이터 접근권한을 제어하는 명령 포함
 - 데이터 제어 명령어
\* mySQL client: mySQL 표준 커맨드

--------

# 테이블에서 데이터 검색
### 1. 자료형
1) CHAR형과 VARCHAR형  
- VARCHAR형은 저장할 문자열의 길이에 맞춰 저장공간을 가변적으로 사용, CHAR형은 항상 고정된 길이로 저장(더 적게 입력시 공백으로 나머지리를 채운 후 저장함)   
2) 문자열 상수 -> '' (싱글쿼트로 감쌈)  
3) 데이터베이스 객체명 -> "" (더블쿼트로 감쌈)  

#### 테이블 구조 참조(DESC)
```
DESC 테이블 명
```
### 2. 패턴 매칭
#### 패턴 매칭 LIKE에서 사용할 수 있는 메타문자
`%` : 임의의 문자 또는 문자열  
`_` : 임의의 문자 하나  

'SQL' 패턴을 찾는 다면
#### 1) 전방 일치
```
SELECT 열명 FROM 테이블명 WHERE 조건식 LIKE 'SQL%';
```
#### 2) 후방 일치
```
SELECT 열명 FROM 테이블명 WHERE 조건식 LIKE '%SQL';
```
#### 3) 중간 일치
```
SELECT 열명 FROM 테이블명 WHERE 조건식 LIKE '%SQL%';
```

### 3.정렬  
#### 1) 오름차순
```
SELECT 열명 FROM 테이블명 WHERE 조건식 ORDER BY 열명;
```
#### 2) 내림차순
```
SELECT 열명 FROM 테이블명 WHERE 조건식 ORDER BY 열명 DESC;
```
#### 3) 복수열 정렬
```
SELECT 열명 FROM 테이블명 WHERE 조건식 ORDER BY 열명1 [ASC|DESC], 열명2 [ASC|DESC] ...;
```
\* 정렬방법 생략시 기본값 ASC

### 4. 결과 행 제한(페이지네이션)

#### 1) LIMIT(MySQL, PostgreSQL)
상위 3건만 확인시
```
SELECT 열명 FROM 테이블명 WHERE 조건식 ORDER BY 열명 LIMIT 3;
```
#### 2) TOP(SQL Server)
```
SELECT TOP 3 열명 FROM 테이블명;
```
#### 3) ROWNUM(Oracle)
```
SELECT 열명 FROM 테이블명 WHERE ROWNUM <= 3;
```
\* ROWNUM은 WHERE구로 지정하기 때문에 정렬하기 전에 처리되어 LIMIT로 행을 제한한 경우와 결과 값이 다름

#### 4) 오프셋 지정
6 ~ 10까지의 결과값 보기(5개) => offset = 시작할 행-1
\* OFFSET의 기본값은 0
```
SELECT 열명 FROM 테이블명 LIMIT 3 OFFSET 5;
```

### 5. 계산
#### 1) SELECT 구로 계산
price와 quantity열을 이용해 곱한 값 나타내기(곱한 값에 amount라는 별명 붙임)
\* AS는 생략가능(SELECT price * quantity amount)
\* 한글로 설정시에는 ""로 감싸서 넣기
```
SELECT *, price * quantity AS amount FROM sample;
```
#### 2) WHERE 구로 계산
price * quantity >= 2000 으로 필터링
\* 주의할 점: WHERE구 -> SELECT구의 순서로 데이터베이스 서버내에서 처리 `(SELECT *, price * quantity AS amount FROM sample WHERE amount >= 2000) 안됨!!`
SELECT구에서 지정한 별명은 WHERE 구 안에서 사용할 수 없음

#### 3) ORDER BY 구로 계산
ORDER BY구는 서버에서 내부적으로 가장 나중에 처리 됨 = SELECT구에서 지정한 별명을 사용할 수 있음
```
SELECT *, price * quantity AS amount FROM sample ORDERBY amount DESC;
```

#### 4) ROUND(반올림)
amount를 소숫점 셋 째자리에서 반올림
```
SELECT ROUND(amount, 2) FROM sample;
```

### 6. 문자열 연산
**문자열 결합**

|연산자/함수|데이터베이스|
|:-:|:-:|
|+|SQL Server|
|`ㅣㅣ`|Oracle, DB2, PostgreSQL|
|CONCAT|MySQL|

#### 1) `10개`와 같이 표시하기
```
SELECT CONCAT(quantity, unit) FROM sample;
```
#### 2) SUBSTRING(SUBSTR) 함수
문자열의 일부분 계산해서 반환
**앞 4자리(년) 추출**
```
SUBSTRING('20140125001', 1, 4)
```
결과: '2014'

**5째 자리부터 2자리(월) 추출**
```
SUBSTRING('20140125', 5, 2)
```
결과: '01'

#### 3) TRIM 함수
스페이스(인수 지정시 지정 인수) 제거 함수
```
TRIM('ABC   ')  ->   'ABC'
```

#### 4) CHARACTER_LENGTH(CHAR_LENGTH) 함수
문자열 길이 계산 함수
\* OCTET_LENGTH 함수는 문자 수가 아닌 바이트 단위로 길이 계산


### 7. 날짜 연산
#### 1) 시스템 날짜 확인하기
```
SELECT CURRENT_TIMESTAMP;
```
#### 2) 날짜의 덧셈과 뺄셈
**1일 후**
```
SELECT CURRENT_DATE + INTERVAL 1 DAY;
```
**날짜형 간의 뺄셈(MySQL)**
```
DATEDIFF('2014-02-28', '2014-01-01')
```

### 8. CASE 문
"a(null=0)" 라는 이름의 열에서 NULL값을 0으로 변환하기
```
SELECT a, CASE WHEN a IS NULL THEN 0 ELSE a END "a(null=0)" FROM sample;
```
\* 사실 null값 변경은 COALESCE 함수 쓰는게 편리함(null이 아니면 앞의 값으로 null이면 뒤의값으로)
```
SELECT a, COALESCE(a, 0) FROM sample;
```
#### ELSE문 생략
ELSE를 생략하면 ELSE NULL이 됨, 상정한 것 외의 데이터가 들어오는 경우도 많으니 ELSE문을 생략하지 않는 편이 나음
