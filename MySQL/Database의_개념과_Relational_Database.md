# 1. Database란
`Database`는 컴퓨터 시스템에 저장된 정보나 데이터를 모두 모아 놓은 집합이다. 데이터들은 `Database Management System`을 통해 제어 및 관리하게되는데 `database`라고하면 `data`자체를 의미하기도하고 이를 관리하는 시스템을 통칭하여 부르기도 한다. 
# 2. Database구성 형태
데이터베이스는 `테이블(table)`들로 구성되어있고 테이블은 `행(row)`과 `열(column)`로 구성되어있는 표 형태이다. 

# 3. Database를 사용하는 이유
**1. 데이터를 오랜 기간 저장 및 보존**
**2. 데이터를 체계적으로 보존하고 관리**
데이터를 모아서 구조화함으로써 경제성과 조작성이 향상된다. 

# 4. Relational Database
## 4.1 Relational Database란(관계형 데이터베이스)
관계형 데이터란 데이터가 서로 상호 관련성을 가진 형태로 표현한 데이터를 말한다. `RDBMS(Relational Database Management System)`으로 관계형 데이터모델에 기초를 둔 데이터베이스 시스템이다.
### Relational Database 특징
**1. 모든 데이터들은 2차원 테이블들로 표현할 수 있다.**
**2. 테이블의 각 `행(row)`는 각자의 `고유 키(Primary Key)`가 있다.**
_\* `고유 키(Primary Key)`는 중복될 수 없는 고유한 키이다._
**3. 각각의 테이블들은 상호 관련성을 가지고 있기 때문에 연결될 수 있다.**
각각의 테이블들이 완전하게 독립된 것이 아닌 각각의 테이블들이 서로 연관된 사이이다.

## 4.2 Relational Database cardinality
### <span style="color:DarkOrchid">One to One(1:1)</span>
A라는 하나의 테이블이 오로지 하나의 B 테이블 데이터와 연결되고 B테이블 데이터 또한 하나의 A테이블 데이터와 연결된다.(서로서로 하나의 로우)

![](https://images.velog.io/images/anjaekk/post/bd8091ce-ae52-4c78-b969-86a0616230c3/image.png)

>**예) 주민등록번호-사람 **
하나의 주민등록번호는 한명의 사람과 연결되며 한명의 사람 또한 하나의 주민등록번호를 가진다.

### <span style="color:DarkOrchid">One to Many(1:다)</span>
하나의 A테이블 데이터는 B테이블의 여러 데이터와 연결되고 하나의 B테이블 데이터는 오로지 하나의 A 테이블 데이터와 연결된다.(로우 하나에 다른 테이블 로우 여러개 연결)

![](https://images.velog.io/images/anjaekk/post/cb6f6637-ffd7-4e5b-a5d9-8ae50cf00431/image.png)

>**예) 학생-선생님 **
한명의 학생은 한명의 선생님과 연결되지만 한명의 선생님은 다수의 학생들을 가르치게 된다. 

### <span style="color:DarkOrchid">Many to Many(다:다)</span>
하나의 A테이블 데이터는 B테이블의 여러 데이터와 연결될 수 있고 하나의 B테이블 데이터 또한 여러 A테이블 데이터와 연결된다.

![](https://images.velog.io/images/anjaekk/post/273f4f5f-7aa4-47ce-9669-c8b1226231f7/image.png)

>**예) 학생-수업**
한명의 학생은 여러개의 수업을 들을 수 있고 하나의 수업은 여러 명의 학생들이 듣는다.

`Many to Many`의 데이터베이스 같은 경우 **두 테이블에 속한 데이터의 조합을 입력하기 위한 `중간 테이블`을 생성**하여 데이터들의 상호관계를 쉽게 정리할 수 있다.
