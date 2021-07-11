## 토큰(Token)
`http`의 대표적인 특징인 `stateless`로 인해 연결이 해제됨과 동시에 서버와 클라이언트는 클라이언트가 이전에 요청한 결과에 대해서 잊어버리게 된다. 즉 각각의 통신기록이 저장되어있지 않기 때문에 로그인을 이전에 했더라도 사용자가 서버에 요청을 할때마다 `인증`을 해야하는데 그 인증을 하기위해 사용되 것이 `토큰(Token)`이다.이러한 토큰은 메타데이터로써 서버와 클라이언트가 `request`와 `response`를 주고 받을 때 `header`에 담아서 주고 받게 된다.
만약 사용자가 로그인에 성공하면 `access token`을 서버가 클라이언트에게 전송하게되고 로그인 성공후 다음부터는 클라이언트가 `access token`을 첨부해서 `request`를 서버에 전송함으로서 매번 로그인 해도 되지 않도록 한다.
여기서 `access token`을 생성하는 방법은 여러가지가 있는데 그 중 가장 널리 사용 되는 기술 중 하나가 바로 `JWT(JSON Web Tokens)`이다.

## JWT(JSON Web Tokens)
JWT는 말 그대로 유저 정보를 담음 JSON 데이터를 암호화 해서 클라이언트와 서버간에 주고 받는 것을 말한다. 
### JWT 구조
JWT는 헤더(Header), 내용(Payload), 서명(Signiture) 이렇게 3가지의 구조로 되어있다. 
#### 헤더(Header)
헤더에는 토큰의 타입(typ)과 해싱 알고리즘(alg)의 정보를 가지고 있다. 헤더의 내용은 BASE64방식으로 인코딩(encoding)해서 JWT의 가장 첫 부분에 기록된다. 아래 예시와 같이 알고리즘 방식은 HS256이며 타입은 JWT라는 토큰의 정보가 들어가게 된다.

- **예시**
```
{"alg":"HS256", "typ":"JWT"}
```

#### 내용(Payload)
내용에는 **토큰에 담을 정보**가 들어있다. 이 담을 정보의 한 부분을 클레임(claim)이라고 부르는데 {"key":"value"}과 같이 이루어져 있다. 클레임은 공개 클레임(public claim)과 비공개 클레임(private claim)으로 구분된다. 공개 클레임은 토큰의 만료시간을 나타내는 `exp`, 토큰이 발급된 시간을 나타내는 `iat`등이 있고 비공개 클래임은 클라이언트와 서버간 협의 하에 사용되는 클레임이다. 이 공개와 비공개 클레임을 조합하여 작성한 뒤 BASE64방식으로 인코딩(encoding)하여 기록된다.

- **예시**
```
{"user-id":1, "exp":"1539517391"}
```

#### 서명(Signiture)
서명은 마치 계약서의 위변조를 막기위해 계약서에 싸인을 하는 것처럼 JWT가 원본 그대로라는 것을 확인할 때 사용한다. 앞서 살펴보았던 헤더와 내용의 값은 간단하게 인코딩하여 값을 넣는 것이었다. 하지만 서명에는 헤더와 내용의 값 뿐만 아니라 별도 생성한 비밀키(Secret key)를 헤더에 지정된 암호 알고리즘으로 암호화하여 전송하게 된다. 물론 이 값은 복호화가 가능하기 때문에 클라이언트 측에서 JWT를 API 서버로 전송하면 서버는 전송받은 JWT의 서명 부분을 복호화하여 서버에서 생성한 JWT가 맞는지 확인하게 된다.
즉, 이 토큰이 우리 사이트에서 발행한 토큰이 맞는지 확인할 수 있는 키가 비밀키(Secret key)가 되는 것이다.

## JWT 사용 예시
- **pyjwt 설치**
```
pip install pyjwt
```

- **JWT생성**
```
>>> import jwt
>>> encoded_jwt = jwt.encode({"user-id": 5}, "secret", algorithm="HS256")
>>> encoded_jwt
'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyLWlkIjo1fQ.tBQu0HfnOYK7lL3tH5ImgsI-y4Jz1RKscJWbV3U2QMI'
```
_\* 패키지명은 pyjwt이지만 임포트할때의 이름은 jwt_

JWT의 첫번째 인자는 JWT에 들어갈 내용(payload)들을 적어주고 두번째 인자로는 시크릿 키를 적어주는데 시크릿 키는 노출되지 않도록 해야한다. 또한 복호화가 가능하기 때문에 내용(payload)에 사용자의 아이디나 패스워드와 같이 사용자 정보가 담기지 않도록 조심해야하고 예제에서 사용한 id의 경우 DB의 접근 권한이 없으면 알게되더라도 의미없는 정보이기 때문에 노출이 가능하다. 
 
- **JWT 복호화**
```
>>> jwt.decode(encoded_jwt, "secret", algorithm="HS256")
{'user-id': 5}
```


> 참조
>
>🔗 [PyJWT | Welcome to PyJWT](https://pyjwt.readthedocs.io/en/latest/)
>
>🔗 [DevTaek 의 개발노트 | HTTP 는 Stateless 한데 로그인은 어떻게 구현할 수 있을까?](https://hyuntaeknote.tistory.com/3)
>
>🔗 [VELOPERT.LOG | JSON Web Token 소개 및 구조](https://velopert.com/2389)
