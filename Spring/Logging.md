## 로깅 라이브러리

스프링에서 기본으로 제공하는 로깅 라이브러리

- 인터페이스: SLF4J
- 구현체: Logback

## 로깅 장점

표준 출력을 사용하지않고 로깅을 통해 로그를 확인하면 다음과 같은 장점을 얻을 수 있다.

1. 로그 레벨 설정이 가능하여 환경마다 구분하여 사용할 수 있다.
2. 스레드 정보, 클래스 이름등 부가 정보를 함께 확인 가능하다.
3. 콘솔에만 출력하는 것이 아닌 파일, 네트워크등으로 로그를 별도 위치에 남길 수 있다. (파일로 남길시 일별, 특정 용량에 따라 로그 분할도 가능)
4. 표준출력보다 성능이 좋다.(내부 버퍼링, 멀티 스레드 등)

## 사용법

Logger를 사용하기 위해서 다음과 같이 두가지 방법이 있다.

### `@Slf4j` 어노테이션 사용

- logging할 클래스에 `@Slf4j` 를 붙여준다.
    
    ```python
    @Slf4j
    @RestController
    public class LogTestController {
    
        @RequestMapping("/log-test")
        public String logTest() {
            String name = "Spring";
    
            log.info("info log = {}", name);
            return "ok";
        }
    }
    ```
    

### LoggerFactory

- LoggerFactory를 통해 클래스를 지정해준다.
    
    ```python
    package hello.springmvc.basic;
    
    import org.slf4j.Logger;
    import org.slf4j.LoggerFactory;
    import org.springframework.web.bind.annotation.RequestMapping;
    import org.springframework.web.bind.annotation.RestController;
    
    @RestController
    public class LogTestController {
    
        // slf4j의 Logger사용, 현재 나 class 지정
        private final Logger log = LoggerFactory.getLogger(getClass());
    
        @RequestMapping("/log-test")
        public String logTest() {
            String name = "Spring";
    
            log.info("info log = {}", name); // 로그 출력
            return "ok";
        }
    }
    ```
    

## 반환

다음과 같이 반환된다. 

![image](https://github.com/anjaekk/TIL/assets/74139727/e863dd4c-30ed-43c0-a788-8493e2aebae1)


- 실행시간, 로깅의 종류, process ID, thread ID, 실행 클래스, 로깅내용

## log level

- 로그 레벨
    
    로그레벨이 나눠져 있기 때문에 운영서버와 개발서버간의 로그레벨을 구분하여 사용할 수 있다. 
    
    trace → debug → info → warn → error
    

- application.properties
    
    spring의 default 로그레벨은 info 이기 때문에 application.properties에서 로그레벨을 설정해주면 trace와 debug도 확인 가능하다. 
    
    hello.springmvc 패키지에 로그 레벨 설정(trace 레벨부터 출력)
    
    ```python
    logging.level.hello.springmvc=trace
    ```
    
    전체 패키지 로그 레벨 설정
    
    ```python
    logging.level.root=trace
    ```
    
- 로그 출력
    
    ```python
    log.trace("trace log = {}", name);
    log.debug("debug log = {}", name);
    log.info("info log = {}", name);
    log.warn("warn log = {}", name);
    log.error("error log = {}", name);
    ```
    

- 출력 결과
    
    아래와 같이 확인할 수 있다. 
    
    ![image](https://github.com/anjaekk/TIL/assets/74139727/77587ab4-3cb4-475e-b31e-1d893f2579e3)

    

## 주의할 점

로그 출력시 다음과 같이 string 조합으로 출력하지 않도록 한다. 

- `log.trace("trace log = ” + name);`  ⇒  X
- `log.trace("trace log = {}", name);`  ⇒  O

만약 로깅 레벨을 info로 설정해놔서 trace를 출력하지 않는 상황이라고 가정했을 때 첫번째 경우 연산이 먼저 이뤄지기 때문에 trace를 출력하지 않지만 불필요한 연산을 하게 되므로서 그만큼 메모리등 리소스를 사용하게 된다.

하지만 두번째 방법은 연산이 없기 때문에 출력하지 않는 trace라면 별도의 다른 작업없이 지나치게 되므로 사소한 습관으로 리소스 낭비를 줄일 수 있다. 

## 추가

- intellij에서 Grep console 플러그인을 사용하면 로깅 레벨에 따라 색을 구분할 수 있어 로그 확인이 더 쉬워진다.
