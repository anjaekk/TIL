HTML에서 스크립트를 직접 장성하지 않고 외부 스크립트 파일을 로드할 때 로드 방법에 대해 알아보도록 한다.

## 스크립트 삽입
HTML페이지에서 외부 스크립트 파일은 보통 아래와 같은 코드를 삽입하여 가져오게 된다.

```HTML
<script src="script.js"></script>
```
HTML 페이지를 파싱(Parsing) 하는 중 위와 같은 코드를 만나게 되면 **DOM 생성을 멈추고 스크립트파일 다운로드를 진행**하게 된다. 그리고 스크립트 파일 다운로드가 완료되고 나서야 다시 파싱을 재개하게 되는데 여기서 중요한 건 스크립트 삽입 위치에 따라 렌더링 시간이 달라진다는 사실이다. 그러므로 어디에 스크립트를 삽입해야 효율적이고 효과적일지에 대해 알아보도록 한다.

---

## `<head>` 에 포함시킬 경우
맨 처음으로 살펴볼 내용은 HTML `<head>`에 삽입했을 경우이다. 

![](https://images.velog.io/images/anjaekk/post/69046b35-bcaf-4950-92ab-f14c90ee5a3b/image.png)

위와 같이 `<head>`에 삽입할 경우 아래의 그림과 같이 HTML 페이지를 파싱하던 중 js파일을 받아오고(Fetching), 실행(Executing)한 뒤 다시 페이지를 파싱하게 된다. 

![](https://images.velog.io/images/anjaekk/post/de713449-0b39-4aff-abfa-b8873bccd118/image.png)

이럴경우 JS파일 크기가 엄청나게 클 경우 렌더링이 너무 오래걸리게 되어 사용자가 페이질르 보기까지 너무 오래걸리게 될 것이다. 그러므로 `<head>`에 스크립트 파일을 포함하는 것은 좋은방법이라고 할 수 없다.

---

## `<body>` 에 포함시킬 경우
다음으로는 DOM을 먼저 생성할 수 있도록 `<body>`의 하단에 스크립트태그를 넣어주는 경우이다.

![](https://images.velog.io/images/anjaekk/post/82bce27c-fd99-4707-a18f-3bfe32efafec/image.png)

위와 같이 HTML 페이지를 파싱을 먼저 진행하고 JS파일을 받아오고 실행하게 된다.

![](https://images.velog.io/images/anjaekk/post/2844c7f2-c966-457a-8365-c3e254815fb4/image.png)

`<body>`에 삽입하게 될 경우 화면 렌더링에서는 좀 더 효과적일 수 있으나 HTML파일 크기가 큰 경우에는 JS가 포함된 `의미있는 콘텐츠`를 보기 위해서는 너무 오래 걸릴 것이다. 그러므로 이 방법도 좋은 방법이라고 할 수 없겠다.

---

`async`와 `defer`은 HTML5에 새로 추가된 `<script>` 속성이다. 이 두가지 속성은 HTML파싱과 스크립트 다운로드를 **병렬**로 진행한다.

## async 속성 사용
`async` 속성은 아래와 같이 `<head>`에 `<script>`를 `async` 속성과 함께 사용하게 된다.

![](https://images.velog.io/images/anjaekk/post/5b5b708a-baef-4512-9f80-f64b86f979b9/image.png)

`async` 속성은 파싱과 JS 불러오기를 병렬적으로 진행한다.

![](https://images.velog.io/images/anjaekk/post/18748d4a-a7d9-485b-8949-2797fbce8104/image.png)

병렬적으로 진행하기 때문에 기존 방법들보다는 다운로드 받는 시간이 절약되어 효율적이라고 볼 수 있다. 하지만 JS를 실행하는 단계에서는 파싱을 중지하게 되고 JS실행이 끝나면 다시 파싱을 재시작 하게 되기 때문에 HTML이 모두 실행되기 전에 JS가 실행되게 된다. 
다수의 스크립트 파일을 다운로드 받게되면 **다운로드가 완료되는 순으로 JS파일을 실행**하기 때문에 순서에 상관없이 실행하게 된다. 만약 순서에 의존적인 페이지라면 문제가 될 수 있기 때문에 유의해야한다.

## defer 속성 사용
`defer` 속성은 `async` 속성과 마찬가지로 `<head>`에 `<script>`를 `defer` 속성과 함께 사용하게 된다.

![](https://images.velog.io/images/anjaekk/post/709898a0-95fd-4d37-95e1-118c7471e666/image.png)

병렬적으로 파싱과 JS 불러오기를 진행하게 되고 파싱이 모두 끝나면 JS를 실행한다.

![](https://images.velog.io/images/anjaekk/post/d48d1483-2ac5-4141-a9de-cfa5e5048c4e/image.png)

병렬적으로 진행되기 때문에 다운로드 시간이 절약되고 `async` 속성과는 다르게 파싱하는 중에 JS파일을 모두 다운로드 받아놓고 파싱이 끝난 후 순서대로 JS파일을 실행하기 때문에 원하는 방향대로 스크립트를 실행할 수 있다.

## 결론
**외부 스크립트를 불러올 때에는 `defer` 속성을 사용하는 것이 최선이다.** 만약 스크립트 순서가 상관 없고 빨리 실행하는게 중요할 경우에는 `async` 속성을 사용할 수 있겠다.

물론 인터넷이 아주아주 빠른 곳에서는 눈에 띄지 않는 문제일 수도 있다. 하지만 아직은 네트워크환경이 좋지 않은 곳도 존재하기도 하거니와 작은 차이가 큰 결과를 낳기에 이런 차이를 지각하고 적용하는 것이 중요하다고 생각한다.



\* 참조 *
[드림코딩 by 엘리](https://www.youtube.com/watch?v=tJieVCgGzhs&list=PLv2d7VI9OotTVOL4QmPfvJWPJvkmv6h-2&index=2)

[Efficiently load JavaScript with defer and async](https://flaviocopes.com/javascript-async-defer/)

[스크립트 요소](https://developer.mozilla.org/ko/docs/Web/HTML/Element/script)
