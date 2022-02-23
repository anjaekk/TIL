# HTTP(HyperText Transfer Protocol)

처음엔 HTML, TEXT를 전송하기 위한 프로토콜이었으나 현재는 모든 데이터를 전송할 있다.

## HTTP의 버전

### HTTP/1.1

- 1997년 등장
- 지금의 HTTP의 완성본 이후 등장한 버전은 성능개선 정도임
- 1999년에 개정됨
- 현재는 주로 1.1을 사용

### HTTP/2

### HTTP/3

*1.1과 2는 TCP기반이지만 3은 UDP기준임(TCP는 3way handshaking등 절차와 알아야하는 것이 많고 속도가 빠른편은 아님 하지만 UDP를 기반으로 한 3은 속도를 많이 높혔음)*

## HTTP 특징

### 1. Client-Server 구조
    
Client와 Server로 구분함으로서 비즈니스로직과 데이터에 관련된 것들은 Server가 Client는 UI에 집중을 하면서 Client와 Server가 각각 독립적으로 진화할 수 있었다. 
    
### 2. 무상태 프로토콜(stateless)
    
Stateless는 Server가 Client의 상태를 보존하지 않는다는걸 뜻한다.(↔ Stateful)
    
- 장점: Server 확장성이 높음(Scale-out)
	- 상태를 보존하지 않기 때문에 갑자기 많은 Client의 요청에도 Server의 Scale-out으로 대처가 가능하게 된다. 만약 Stateful하다면 해당 정보를 다른 Server에도 전달해야하기 때문에 무한한 Server scale-out이 불가능 할 것이다.(하지만 로그인한 사용자를 판별위해 쿠키나 세션 등 그 상태를 유지해야하는 경우에는 불가피하게 stateful을 사용해야함으로 현 실무에서 아무리 stateless라도 무한한 scale-out은 힘들 것이다. 그래도 **최소한**만 stateful하게 사용!!)
- 단점: Client가 추가 데이터를 전송해야 함
        - 상태를 보존하지 않는 만큼 추가적인 데이터 함께 전송
        
### 3. 비연결성
    
Client의 요청과 Server의 응답 이후 연결을 끊는 것을 의미한다. HTTP의 기본이 연결을 유지하지 않는 모델로 1시간 동안 수천명이 서비스를 사용한다고 해도 실제 서버에서 동시에 처리하는 요청은 수십개에 채 지나지 않는다. 
    
- 장점: Server자원 효율적으로 사용
	- Server는 Client에 연결을 유지하지 않기 때문에 최소한의 자원만 사용하여 효율적으로 사용할 수 있다. Client의 수가 늘어날 수록 만약 연결을 유지해야 한다만 Server의 부담이 커질 것이다.
    
- 단점: 연결시간 소요
	- 매 요청마다 TCP/IP연결을 새로 맺어야 하다보니 그 만큼의 시간이 소요되게 된다.
### 4. HTTP 메세지
- 요청, 응답메세지
- 기본구조
	- start-line  
            요청의 경우 HTTP method, 응답의 경우 상태코드(status-code)가 start-line에 들어가게 된다.     
	- header    
            HTTP 전송에 필요한 모든 meta data들이 모두 들어있다. header에 대한 내용은 아래에서 더 다루도록 한다.    
	- empty line(CRLF; 공백라인 필수)
	- message body    
            byte로 표현할 수 있는 데이터는 모두 들어갈 수 있다.
            
5. 단순하고 확장이 가능하다

## HTTP method

### 1. 종류
- GET
	- 리소스 조회
	- body에 데이터를 전달할순 있지만 지원하지 않는 서버가 많기 때문에 권장하지 않는다.
- POST
	- 요청 데이터 처리
	- body를 통해 서버로 요청 데이터를 전달한다.

- PUT
	- 리소스 완전히 대체(기존 리소스가 존재시 대체, 없다면 생성)
	- **POST와의 차이점은 클라이언트가 리소스를 식별한다.**(POST로 보낼 때는 `users/`로 해서 회원가입 진행했다고 하면 PUT은 `users/100`으로 100번의 user를 식별한다.)
- PATCH
	- 리소스 부분 변경
- DELETE
    
    이 외에도 HEAD, OPTIONS등이 있다.(사용 거의 안함)
    
### 2. 특징
- 멱등성
	- 호출의 횟수와 상관없이 결과가 동일하다.(중간에 외부요인으로 리소스가 변경되어 결과가 변경되는 것은 고려하지 않음)
	- 멱등 method: GET, PUT, DELETE
	- 비멱등 method: POST(여러번 호출시 그 결과가 계속 누적된다.)
        
이러한 멱등성은 서버가 time out등 정상 응답을 하지 못한 경우, 재요청을 해도 되는지에 대한 판단을 할 수 있기 때문에 ‘자동복구 메커니즘’에 활용할 수 있다. 
        
- 캐시(Cacheable)
	- 응답 결과 리소스를 캐시해서 사용해도 되는지 여부
	- 캐시 가능: GET, HEAD, PATCH(실제로는 GET, HEAD만 사용)
	- 캐시 어려움: POST, PATCH는 본문 내용까지 캐시 키로 고려해야 하는데 구현의 어려움이 있어 사용되지 않는다.
