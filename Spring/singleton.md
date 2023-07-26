## Singleton

- 기존에 만들었던 순수한 DI컨테이너인 AppConfig는 요청을 할때마다 객체를 새로 생성하게 된다.
- 매번 새로운 객체를 생성하는 것은 그만큼 메모리의 낭비가 심하게 되므로 객체를 단 1개만 생성하여 공유하도록 설계할 수 있다. → Singleton

### 싱글톤 패턴

- 클래스의 인스턴스가 1개만 생성되는 것을 보장하는 디자인 패턴
- = 객체 인스턴스가 2개 이상 생성되지 못하도록 막는다.

```java
public class SingletonService {

    // static 영역에 객체를 1개만 생성해둔다.
    private static final SingletonService instance = new SingletonService();

    public static SingletonService getInstance() {
        return instance; // 이 static 메서드를 통해서만 조회가 가능함
    }

    //생성자를 private으로 선언해서 외부에서 new 키워드를 사용한 객체 생성을 못하게 막는다.
    private SingletonService() {
    }
    
    public void logic() {
        System.out.println("싱글톤 객체 로직 호출");
    }
}
```

- 위에 싱글톤 패턴 생성코드의 문제점
    - 싱글톤 패턴을 생성하는데 코드가 많이 들어간다.
    - 의존관계상 클라이언트가 구체 클레스에 의존한다. → DIP 위반’
        - 사용할때 구체클래스 .getInstance로 가져와야 한다.
    - 테스트가 어렵다.
    - private 생성자로 자식 클래스 생성하기 어려움
    - 안티패턴으로 불리기도 함

### 싱글톤 컨테이너

- 스프링 컨테이너는 싱글톤 패턴의 문제점을 해결하면서 객체 인스턴스를 싱글톤으로 관리한다.
- 스프링의 기본 빈 등록 방식이 싱글톤이지만 싱글톤 방식만 지원하는 것은 아니다.
- = 스프링 DI 컨테이너를 사용하는 장점(자동 싱글톤!)
