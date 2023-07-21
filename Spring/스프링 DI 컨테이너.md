## 스프링 DI 컨테이너

### 스프링 컨테이너

- ApplicationContext 를 스프링 컨테이너라고 한다.
- AnnotationConfigApplicationContext를 이용해 생성한다.
- 기존에는 AppConfig를 사용해서 직접 객체를 생성하고 DI를 했지만 스프링의 ApplicationContext를 이용해 사용할 수 있다.
- @Configuration이 붙은 AppConfig를 설정(구성) 정보로 사용하고 여기서 @Bean이라고 적힌 메서드를 모두 호출하여 반환된 객체를 스프링 컨테이너에 등록한다.

### 스프링 빈

- @Bean이 붙은 메서드의 명을 스프링빈의 이름으로 사용한다.
- 스프링 빈은 applicationContext.getBean()메서드를 통해 찾을 수 있다.

## 빈 조회

- ac.getBean(빈이름, 타입)
- ac.getBean(타입)
- 컨테이너에 등록된 모든 빈 조회

```java
void findAllBean() {
            String[] beanDefinitionNames = ac.getBeanDefinitionNames();
            for (String beanDefinitionName : beanDefinitionNames) {
                Object bean = ac.getBean(beanDefinitionName);
                System.out.println("name = " + beanDefinitionName + " object = " + bean);

        }
```

- 내가 등록한 빈 조회(ROLE_APPLICATION)

```java
void findApplicationBean() {
            String[] beanDefinitionNames = ac.getBeanDefinitionNames();
            for (String beanDefinitionName : beanDefinitionNames) {
                BeanDefinition beanDefinition = ac.getBeanDefinition(beanDefinitionName);

                if (beanDefinition.getRole() == BeanDefinition.ROLE_APPLICATION) {
                    Object bean = ac.getBean(beanDefinitionName);
                    System.out.println("name = " + beanDefinitionName + " object = " + bean);
                }
        }
```

### 동일한 타입이 둘 이상일 때

- 빈 이름을 지정해 주면됨

### 상속관계

- 부모타입을 조회하면 자식타입도 함께 조회한다

## BeanFactory와 ApplicationContext

- BeanFactory와 ApplicationContext 모두 스프링 컨테이너라고 부르며 BeanFactory를 직접 사용할 일은 거의 없으므로 보통 ApplicationContext를 사용한다.

### BeanFactory

- 스프링 컨테이너의 최상위 인터페이스
- 스프링 빈을 관리하고 조회하는 역할을 한다

### ApplicationContext

- BeanFactory를 모두 상속받아 제공한다.
- BeanFactory와 달리 ApplicationContext에서 제공하는 부가기능
    - 메세지소스를 활용한 국제화 기능
    - 환경변수
    - 어플리케이션 이벤트
    - 편리한 리소스 조회

## BeanDefinition

- 스프링 빈 메타장보
- 스프링 컨테이너는 이 메타정보를 기반으로 스프링 빈을 생성한다.
    - 그래서 xml을 이용하던 자바코드를 이용해 빈을 생성하던 BeanDefinition을 이용해 스프링 빈을 생성하면 된다.
