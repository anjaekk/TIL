사용자가 웹에 회원가입하고 로그인할 때 패스워드의 암호화는 필수적이다. 암호화를 하지 않을 경우 DB가 해킹을 당하면 유저의 패스워드도 그대로 노출 되게 되고 꼭 외부 해킹이 아니더라도 내부 인력이 사용자의 패스워드를 봐서는 안되기 때문이다. 그러므로 필히 암호화를 해서 저장해야한다. 

## 1. 단방향 해쉬 함수(one-way hash function)
패스워드 암호에는 단방향 해쉬 함수(one-way hash function)가 일반적으로 쓰인다. 말 그대로 함수로써 input을 넣으면 암호화된 output이 나오게 된다. 본래 해쉬 함수는 자료구조에서 빠른 자료의 검색이나 데이터의 위변조 체크를 위해 쓰이지만 **복원이 불가능**한 해쉬함수는 암호학적 용도로 사용한다. 

## 2. 다이제스트(digest)
단방향 **해시함수는 원본 메시지를 반환하여 암호화된 메세지인 다이제스트(digest)를 생성**한다. 암호화된 메세지는 원본 메세지를 구할 수 없기 때문에 `단방향성(one-way)`라고 한다.

- **해쉬함수 사용 예**
```
>>> import hashlib
>>> hassed_message = hashlib.sha256()
>>> hassed_message.update(b"password")
>>> hassed_message.hexdigest()
'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
```

## 3. 단방향 해쉬 함수의 한계
단방향 해쉬함수로 암호화를 하는데 있어 한계점이 있다면 동일한 **원본 메세지는 동일한 다이제스트를 얻는 다는 것**이다. 또한 위에도 언급했지만 해쉬함수는 원래 패스워드를 저장하기 위해 설계된 것이 아닌 짧은 시간에 데이터를 검색하기 위해 설계된 것으로 **처리 속도가 매우 빠르게 설계**되었다. 이렇다보니 **공격자(해커)의 입장에서 임의의 문자열 다이제스트와 해킹할 대상의 다이제스트를 비교하여 해싱된 다이제스트의 원문을 알아낼 수 있다.** 이렇다면 패스워드가 충분히 길지 않거나 간단할 때는 그리 긴 시간이 걸리지 않게 될 것이다. 이렇게 다이제스트를 모아놓은 테이블을 `레인보우 테이블(Rainbow Table)` 이라고 한다. 

## 4. 한계 보완
단방향 해쉬 함수의 한계를 보완하기위해 일반적으로 `Salting`, `Key Stretching` 2가지 보완점이 사용된다. 
### 1) Salting
`Salting`은 해쉬함수를 사용하기 전에 원문에 임의의 문자열을 덧붙여 해시값을 계산하는 방법이다. 이렇게 하게되면 공격자가 다이제스트를 알아내더라도 패스워드는 알아내기 어려워진다. 

### 2) Key Stretching
`Key Stretching`은 단방향 해쉬값을 계산하고 그 해쉬값에 또 해싱하는 것처럼 해싱을 반복하는 것을 말한다. 물론 해싱의 반복횟수는 노출되지 않도록 해야하지만 알게되더라도 패스워드 원문을 알아내기까지의 시간이 오래걸리게 될 것이다. 

![](https://images.velog.io/images/anjaekk/post/7dee0b0d-ab3a-4ea3-9380-5348545cc5ad/image.png)

> 📁 [이미지 출처: egovframework:rte:fdl:encryption_decryption](https://www.egovframe.go.kr/wiki/lib/exe/detail.php?id=egovframework%3Arte%3Afdl%3Aencryption_decryption&media=egovframework:rte:fdl:password.jpg)

## 5. bcrypt
`bcrypt`는 해시함수 오픈소스 라이브러리로 `Salting`과 `Key Stretching`을 구현한 해쉬 함수중 가장 널리 사용된다. `bcrypt`는 암호화를 위해 다양한 언어가 지원되고 사용이 간편하기 때문에 많이 사용된다. 만약 `Salting`과 `Key Stretching`을 `bcrypt`없이 구현한다고 하면 어떤 `Salting`을 넣어줬는지, `Key Stretching`을 몇번했는지 어떤 알고리즘을 썼는지 모두 DB에 저장해야할 것이다. 하지만 `bcrypt`는 해쉬 결과값에 소금값과 해시값 및 반복횟수를 같이 보관하기 때문에 우리는 암호화된 값만 DB에 저장하면 되기 때문에 비밀번호 해싱을 적용하는데 있어 DB설계를 복잡하게 할 필요가 없다는 장점이 있다. 

- **bcrypt를 통해 해싱된 다이제스트**

![](https://images.velog.io/images/anjaekk/post/d6090924-6a11-4425-a97b-3a369d7ae2ff/image.png)

> 📁 [이미지 출처: Using PHP Native Password API with Magento](https://www.classyllama.com/blog/using-php-native-password-api-magento)

_\* salt값을 알게되더라도 원문 패스워드를 모르면 해킹할 수 없다. _

## 6. bcrypt 사용 예시

- **bcrypt를 사용하기전 설치를 해준다.**
```
pip install bcrypt
```

- **파이썬을 이용하여 패스워드를 암호화 해보자.**
```
>>> import bcrypt
>>> password = '1234'

>>> bcrypt.hashpw(password, bcrypt.gensalt())
TypeError("Unicode-objects must be encoded before hashing")
```
위와 같이 임의의 패스워드를 `bcrypt`를 이용해 해싱해줬더니 `TypeError`가 발생했다. 에러로그를 확인하니 **"유니코드 객체는 해싱전에 인코딩 되어야 한다"**라고 되어있다. 

> _**파이썬의 인코딩**: 문자열을 바이트 코드인 utf-8, ascii, euc-kr형식으로 변환(문자 -> 숫자)_
> _**파이썬의 디코딩**: utf-8, ascii, euc-kr형식의 바이트 코드를 문자열로 변환(숫자 -> 문자)_

- **인코딩(encoding) 결과**
```
>>> encoded_password=password.encode('utf-8')
>>> encoded_password
b'1234'

>>> type(encoded_password)
<class 'bytes'>
```
b'1234'라고 바이트화 된 것을 확인할 수 있다.

- **디코딩(decoding) 결과**
```
>>> decoded_password = encoded_password.decode('utf-8')
'1234'
```
다시 문자열이 되어 출력됐다.

- **인코딩하여 해싱**
```
>>> hassed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
>>> hassed_password
b'$2b$12$Bqf0lzJqKpyBm8FphjoHyOrSzxoqerlta0Mqxvc6mDqQFJpq.1jVK'
```
`encode('utf-8')`를 이용하여 인코딩을 해줬더니 다이제스트(digest)가 잘 생성된 것을 확인할 수 있다.

- **솔트값 생성**
```
>>> bcrypt.gensalt()
b'$2b$12$./hCD6Q.YUY5T0TX6f46gO'
>>> bcrypt.gensalt()
b'$2b$12$jp3HSJdyG2WROFiMh4w7BO'
```
솔트 값은 실행할 때마다 랜덤한 값들이 생성되어 나온다.

```
>>> salt = bcrypt.gensalt()
>>> salt
b'$2b$12$WBuLNTOVb2/mB7pYY4mmou'
```
솔트값을 변수에 담아 저장해주도록 한다.(사용할 때는 변수에 담지 않아도 된다.)

- **정해진 솔트값으로 해싱**
```
>>> hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
>>> hashed_password
b'$2b$12$WBuLNTOVb2/mB7pYY4mmoubar.55Id3WVqdVax9Lj.n9tpVqTKqXO'
>>> type(hashed_password)
<class 'bytes'>
```
이렇게 해쉬된 패스워드 값을 디코드하여 DB에 저장하도록 한다. 

- **로그인시 패스워드 확인**

```
>>> bcrypt.checkpw('1234'.encode('utf-8'), hashed_password)
True
>>> bcrypt.checkpw('123'.encode('utf-8'), hashed_password)
False
```
`checkpw`는 말 그대로 사용자가 로그인을 할 때 계정과 패스워드가 일치하는지 확인하는 것이다. 공식문서에 나와있듯이 첫번째 인자로 사용자가 입력한 패스워드를, 두번째 인자로 해쉬된 값을 넣어주면 된다.
```
>>> if bcrypt.checkpw(password, hashed):
...     print("It Matches!")
... else:
...     print("It Does not Match :(")
```
주의할 점은 DB에 해쉬된 패스워드를 디코드하여 넣어줬기 때문에 패스워드 확인시 다시 인코딩하여 확인해야한다.

> 참조
>
>🔗 [stranger's LAB 블로그 | 패스워드의 암호화와 저장 - Hash(해시)와 Salt(솔트)](https://st-lab.tistory.com/100)
>
>🔗 [Project description | bcrypt](https://pypi.org/project/bcrypt/)

