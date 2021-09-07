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
