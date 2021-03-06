# 쿠키(Cookie)

### 사용처

- 사용자 로그인 세션 관리
- 광고 정보 트래킹

<br/>

### 쿠키 사용 이유

HTTP의 주요 특징: `Stateless`(무상태)

클라이언트와 서버가 `request`와 `response`를 주고 받으면 연결 해지(이전 요청을 기억하지 못함)

요청에 정보가 포함되도록 하기 위해 쿠키 사용

<br/>

### 쿠키의 종류

1. `Set-Cookie`: 서버 → 클라이언트 쿠키 전달(응답)
2. `Cookie`: 클라이언트가 서버에서 받은 쿠키를 저장, HTTP요청시 서버로 전달

<br/>

### 쿠키 사용 프로세스

특정 요청을 클라이언트가 서버에게 보내면 서버는 필요한 정보를 `Set-Cookie`에 담아 응답하게 된다. 웹 브라우저에는 쿠키 저장소가 있는데 그 저장소에 `Set-Cookie`의 데이터를 저장하게 된다. 이 뒤로는 클라이언트가 서버에 요청을 보낼 때마다 쿠키 저장소를 확인해 해당 내용을 `Header`안에 `Cookie:` 으로 표시하여 함께 요청을 보내게 된다. 

<br/>

### 생명주기

- 세션쿠키

만료 날짜를 생략하면 브라우저 종료시까지만 유지된다.

- 영속쿠키

만료 날짜를 입력하면 해당 날짜까지 유지된다.

- `expires`

만료일이 되면 쿠키 삭제

- `max-age`

`max-age=3600` 으로 지정시 3600초가 지나면 쿠키가 삭제되며 0이나 음수로 지정하게 되도 삭제된다.

<br/>

### 단점

쿠키 정보는 항상 서버에 전송되기 때문에 네트워크에 트래픽을 추가로 유발해 부담이 될 수 있다. 이와 더불어 보안적인 문제도 있을 수 있기 때문에 보안에 문제가 되지 않는 내용으로 최소한의 정보만 사용할 것을 권고한다. 

<br/>

### 보안책

**1. 쿠키 내용 보안**

하지만 해당 내용을 모두 담아서 요청하고 응답을 하게되면 보안상 문제가 될 수 있기 때문에 `Session ID`나 인증 토큰을 사용하는 등 보안책들과 함께 사용되게 된다. 

_Session ID활용 예_

유저의 정보를 그대로 드러내서 요청과 응답을 주고 받는 것이 아닌, 애초에 서버에서 클라이언트에게 `Set-Cookie`에 해당 유저에 해당하는 `Session ID`를 만료일등과 함께 전송한다. 그럼 클라이언트는 이 세션아이디를 쿠키 저장소에 저장하고 해당 유저에 대한 `Cookie`를 보낼 때 `Session ID`값을 전송하게 되며 서버에서는 이를 활용하게 된다. 


**1. 쿠키에 지정 보안**
- `Secure`

쿠키는 원래 HTTP와 HTTPS 모두에 전송 가능하지만 Secure를 적용하게 되면 HTTPS인 경우에만 전송하게 된다.  

- `HttpOnly`

XSS 공격을 방지하기 위한 것으로 원래는 Javascript에서 쿠키에 접근이 가능하지만 HttpOnly를 적용하게 되면 접근이 불가하게 된다.

- `SameSite`

XSRF 공격 방지를 위한 것으로 현재 요청하는 도메인과 쿠키에 설정한 도메인이 같은 경우에만 전송되도록 지정하는 것이다.
