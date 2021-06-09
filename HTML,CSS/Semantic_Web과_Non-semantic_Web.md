`HTMl`과 `CSS`의 `Semantic`과 `non-semantic`를 사례를 통해 비교하여 알아보도록 한다. 

# 1. Semantic Web과 Semantic Tag
---
## 1) Semantic Web
`Semantic Web`은 '의미론적인 웹'이라는 뜻으로, `정보`와 `자원` 사이의 `관계`, `의미 정보`를 컴퓨터가 처리할 수 있는 [온톨로지](https://ko.wikipedia.org/wiki/%EC%98%A8%ED%86%A8%EB%A1%9C%EC%A7%80) 형태로 표현하여 처리하도록 하는 기술이다. 
> 📁 [위키백과: 시맨틱 웹](https://ko.wikipedia.org/wiki/%EC%8B%9C%EB%A7%A8%ED%8B%B1_%EC%9B%B9)

이렇게만 듣기에는 그 뜻이 모호할 수 있으니 쉽게 설명하자면 컴퓨터(브라우저)와 사람 모두 쉽게 이해하고 찾아볼 수 있도록 `HTML` 안에있는 요소에 이름표(태그)를 붙여주는 것이다. 이러한 `Semantic Web`은 1998년, `W3C`에서 제안 되었다.

**즉, `Semantic Web`을 통해 웹에 `접근성(accessibility)`이 좋아진다.**

## 2) Semantic Tag
`Semantic Web`이 위와같다면 `Semantic Tag`는 당연하게도 그 이름표를 말한다.
## 3) Semantic Tag 요소
사람과 컴퓨터가 이름표의 의미를 같게 이해하기 위해서는 마음대로 작성한 이름이여서는 안될 것이다. 그 의미가 정해진 `Semantic Tag`의 요소들은 다음과 같다.
![](https://images.velog.io/images/anjaekk/post/a5dc7261-57c8-4820-b498-86f7dd6293a6/image.png)

**`<div>`와 `<span>`은 `Non-semantic` 즉, 의미가 없는 태그이다.**

이 외, 요소에 대한 자세한 설명은 아래 링크를 참조하면 된다.
> 📁 [Semantic Tag 요소](https://www.w3schools.com/html/html5_semantic_elements.asp)

# 2. Semantic Web과 Non-semantic Web
---
## 1) 이미지 삽입시 Semantic과 Non-semantic
웹사이트에 이미지를 넣는 방법을 통해 Semantic과 non-semantic를 비교해보고자 한다. 우선 웹 사이트에 이미지를 넣는 방법은 크게 다음과 같이 두가지로 나뉜다.

**(1) `HTML`에서 `<img>` 태그를 사용하는 것**
```HTML
<img src="hamster.png"
     alt="Golden striped fluffy hamster">
```
**(2) `CSS`의 `<div>` 태그 안 `background-image`속성을 추가하는 것**
**- HTML**
```HTML
<div class="hamster-img">햄스터 🐹 </div>
```
**- CSS**
```css
.hamster-img {
  background-image: url("hamster.png");
}
```

위와 같을 때 **(1)**번은 `Semantic`한 방법이며 **(2)**번은 `Non-semantic`한 방법이다. 

## 2) Semantic과 Non-semantic 비교
### (1) 접근성

(1)번과 같이 `HTML`에서 `<img>` 태그를 사용하게 되면 `Semantic Tag`를 이용하게 되어 브라우저도 이를 이해함으로 `SEO`(검색엔진 최적화)에 유리하게 된다. 또한 시각장애가 있을 경우 스크린 리더를 통해 웹페이지를 읽게 되는데 여기서 **이미지 대체 텍스트**인 `alt` 속성 안 텍스트를 읽게된다. 위와 같은 상황이라면 _"여기엔 금색 줄무늬가 있는 햄스터 이미지가 있어"_ 하고 알려주는 것이다. 

하지만 (2)번과 같이 `background-image`속성으로 이미지를 넣게 될 경우 `alt` 속성을 넣을 수 없음으로 스크린리더를 사용하는 **사용자의 접근성을 떨어트리게 된다.**

아래 링크는 alt 속성의 들어가야 할 요소들이 정리되어있다.
> 📁 [alt 속성 요소](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Images_in_HTML)

### (2) 이해도
만약 이미지에 에러가 나게된다면 어떻게 될까?
(1)번과 같이 `Semantic Web`일 경우 `broken image` 와 `alt` 텍스트가 보일 것이다. 그럼 웹페이지 사용자는 이미지가 나타나지 않아도 _"아! 여기 금색 줄무늬 햄스터가 있구나!"_ 하고 웹페이지를 이해할 수 있다.
하지만 (2)번과 같이 `Non-semantic Web`일 경우 이미지 에러 발생시 어떠한 정보도 노출되지 않고 지나치게 된다.(마치 없는듯!) 만약 그 정보가 웹페이지를 이해하는데 있어 필요한 내용이라면 사용자의 이해도를 떨어트릴 수 있다.

_하지만 이미지 에러시 텍스트 노출을 안하는 것이 더 자연스럽고 그 이미지가 웹페이지의 내용을 이해하는데 영향을 미치지 않는다면 `Non-semantic`한 방법을 이용하여 사용할수도 있다._

### (3) 그 외
이 외에도 `Semantic Tag`로 정리되어있는 `HTML`은 개발자 입장에서도 오로지 `<div>`와 `<span>`태그로만 이루어진 `HTML`보다 유지, 보수관리에 있어 편하게 된다.

# 3. 결론
---
`Semantic Web`이라면
**1. `SEO`(검색엔진 최적화)에 유리하게 되어 사용자의 접근성을 높힐 수 있다.
2. 시각장애인과 같이 스크린리더로 웹페이지를 읽을 때 이해도와 접근성을 높힐 수 있다.(이미지가 에러로 인해 나오지 않을 경우 `broken image` 와 `alt` 텍스트로 대체되어 일반 사용자의 웹페이지 이해도 또한 높힐 수 있음)
3. 개발자의 입장에서도 유지관리가 편하다.

하지만 이미지 삽입의 경우 웹페이지를 이해하는데 영향을 미치지 않는다면 `Non-semantic`한 방법을 이용할 수도 있다.

> 참조
🔗 [시맨틱 웹](https://ko.wikipedia.org/wiki/%EC%8B%9C%EB%A7%A8%ED%8B%B1_%EC%9B%B9)
🔗 [HTML: A good basis for accessibility](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML)
🔗 [HTML Semantic Elements](https://www.w3schools.com/html/html5_semantic_elements.asp)
🔗 [Images in HTML](https://developer.mozilla.org/en-US/docs/Learn/HTML/Multimedia_and_embedding/Images_in_HTML)
