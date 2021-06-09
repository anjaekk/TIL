`HTML`과 `CSS`를 복습겸 공부하는 중 자주 헷갈리는 개념인 `Position` 속성에 대해 정리하고 넘어가고자 한다.

# 1. Position 속성
포지션 속성은 문서상의 요소를 배치하는 방법으로 `top`, `right`, `bottom`, `left` 속성이 요소를 배치할 최종 위치를 결정하게 된다.

# 2. 속성 값
## Static(정적)
`Static`은 `Position` 속성에서 아무런 값을 지정하지 않았을 때 적용되는 기본값으로 요소를 일반적인 문서의 흐름대로 배치한다. 정적인 값으로 `top`, `right`, `bottom`, `left`속성을 사용하지 않는다. Static은 잘 사용되어지지 않는다.

## Relative(상대적)
`Relative`는 **자기 자신을 기준**으로 원하는 위치로 이동하고자 할때 사용하고 별도의 `top`, `right`, `bottom`, `left`의 값을 주지 않는다면 `Static`과 동일하게 동작한다. 

- HTML
```HTML
<div class="relative1">
  relative-box1
</div>
<div class="relative2">
  relative-box2
</div>
```

- CSS
```css
.relative1 {
  position: relative;
  background-color: yellow;
  width: 200px;
  height: 150px;
}

.relative2 {
  position: relative;
  top: -20px;
  left: 20px;
  background-color: red;
  width: 200px;
  height: 150px;
}
```

- 결과

![image](https://user-images.githubusercontent.com/74139727/121281848-8d78d500-c913-11eb-9836-4b44ac151b14.png)


위의 코드를 보면 `position: relative;`를 적용하고 `top: -20px;`, `left: 20px;`를 적용했을 때를 알 수 있다. 기존의 **본인 위치**에서 지정해준 만큼 움직였다.

## Absolute(절대적)
`Absolute`는 **가장 가까운 부모 요소를 기준**으로 배치한다. `top`, `right`, `bottom`, `left`로 위치를 지정할 수 있으며 `Absolute`를 자식요소에 지정해주기 위해서 부모요소에는 `Relative` 속성값을 넣어줘야 한다. 만약 따로 지정해놓은 **부모 요소가 없다면 본문(document body)를 기준**으로 삼는다.


- HTML
```HTML
<div class="relative">
  relative-box
</div>
<div class="absolute">
  absolute-box
</div>
```

- CSS
```css
.relative {
  position: relative;
  background-color: yellow;
  width: 200px;
  height: 150px;
}

.absolute {
  position: absolute;
  top: 40px;
  left: 20px;
  background-color: red;
  width: 200px;
  height: 150px;
}
```

- 결과

![image](https://user-images.githubusercontent.com/74139727/121281991-ce70e980-c913-11eb-9a28-3d776f647c67.png)


부모요소에는 `position: relative;`를 자식요소인 빨간색의 `absolute-box`에는 `position: absolute;`값을 주었다. 그리고 `top: 40px;`과 `left: 20px;`를 주게되면 **부모요소의 위치를 기준으로 이동**하게 된는걸 확인할 수 있다.

## fixed(고정)
`fixed`는 페이지를 스크롤로 움직이더라도 계속 같은 곳에 고정되어있는 속성 값이다. `top`, `right`, `bottom`, `left`로 위치를 지정할 수 있다.


- HTML
```HTML
<body>
  <p>여기가 처음!<p/>
  <div class="fixed">
    fixed-box
  </div>
</body>
```

- CSS
```css
body {
  height: 200vh;
}

.fixed {
  position: fixed;
  top: 40px;
  left: 20px;
  background-color: yellow;
  width: 100px;
  height: 50px;
}
```

- 결과

![image](https://user-images.githubusercontent.com/74139727/121282125-f95b3d80-c913-11eb-8d9e-6ebafcc741b1.png)

![image](https://user-images.githubusercontent.com/74139727/121282169-0415d280-c914-11eb-8be0-ff216ca43b79.png)


위 코드를 보면 스크롤을 내려도 노란색의 `position: fixed;`를 적용한 박스는 계속 그 자리인 것을 확인할 수 있다.


> 참조
> 
>🔗 [position](https://developer.mozilla.org/ko/docs/Web/CSS/position)
>
>🔗 [Learn CSS Layout](https://learnlayout.com/position.html)
