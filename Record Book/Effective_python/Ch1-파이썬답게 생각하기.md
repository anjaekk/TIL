## 유니코드 샌드위치

- 파이썬 프로그램을 작성할 때 유니코드 데이터를 인코딩하거나 디코딩하는 부분을 인터페이스 가장 먼 경계지점에 위치시키기

- Bytes 에는 8비트 값의 시퀀스가 들어있고 str에는 유니코드 코드 포인트의 시퀀스가 들어있다.

## 문자열 포메팅

1. 형식 문자열(%)
    
    ```python
    a = "테스트1"
    b = "테스트2"
    print("테스트1: %s, 테스트2: %s" % (a, b))  
    ```
    
    - %s 와 같이 형식 지정자의 문법은 C의 printf 함수에서 비롯되어 파이썬에 이식됐다.
    - 형식문자열의 문제점
        - 형식화 식에서 오른쪽에 있는 Tuple 내 데이터 값의 순서를 바꾸거나 값의 타입을 바꾸면 타입 변환이 불가능 하므로 오류가 발생할 수 있다.
        - 형식화를 하기 전에 값을 살짝 변경해야한다면 식을 읽기가 어려워진다. (값을 넣어야하는 튜플의 길이가 길어지면 가독성이 떨어짐)
        - 형식화 문자열에서 같은 값을 여러 번 사용하고 싶다면 튜플에서 같은 값을 여러번 반복해야 한다.
            - 이를 해결 하기 위해 Tuple대신 Dictionary타입을 사용할 수 있지만 가독성이 떨어지고 번잡스러워진다.
            
    1. format과 str.format 내장함수
        
        ```python
        a = 1234.5678
        formatted = format(a, ',.2f')
        print(formatted) # 1,234.57
        
        b = "바나나"
        c = "맛있어"
        formatted = '{}는 {}'.format(b, c) 
        print(formatted) # 바나나는 맛있어
        ```
        
        - format메서드도 형식문자열과 동일한 문제 발생
        
    2. 인터폴레이션을 통한 문자열(= f-문자열, 3.6 이상)
        
        ```python
        a = "테스트1"
        print(f"{a} 입니다.") # 테스트1 입니다.
        ```
        
        - 형식 문자열의 표현력을 극대화
        - 키와 값을 불필요하게 중복지정해야하는 경우가 없어짐
        - 간결하지만 위치 지정자 안에 임의의 파이썬 식을 직접 포함할 수 있어서 매우 강력함
    
    ### zip 내장함수
    
    - 둘이상의 이터레이터를 지연계산 제너레이터를 사용해 묶어주는 함수
    - 만약 이터레이터의 길이가 상이하다면 짧은 입력의 길와 같게 반환하여 긴쪽은 짤리게 된다.
    - 길이가 긴 이터레이터의 값을 버리면 안된다면 itertools.zip_longest 함수를 사용하면 된다.(긴쪽 None으로 맵핑)
