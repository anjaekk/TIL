// 1. strict 선언
// ES(ECMAScript) 5에 도입
// 선언되어 있지 않은 변수 에러표시
// use this for Vanila Javascript.
'use strict';


// 2. block scope (블럭 스코프)
// 블럭 안에 코드를 작성하게 되면 블럭 밖에서는 안으로 접근할 수 없음
{
  
}


// 3. global scope (글로벌 스코프)
// 블럭 밖에 코드 작성 (블럭 안에서나 밖에서나 모두 접근 가능)
// 글로벌 변수들은 메모리 효율성을 위해 최소한으로 사용
let globalName = 'global name';
{

}


// 4. Variable(변수), rw(읽고 쓰기 가능)
// Mutable 데이터 타입
// let (ES6에 도입)
let globalName = 'global name';
{
  let name = 'ellie';  
  console.log(name);
  name = 'hello';
  console.log(name);
  console.log(globalName);
}
console.log(name);
console.log(globalName);

// var (사용하지 말 것!!)
// var hoisting (어디에 선언했는가와 상관없이 최상단으로 끌어올려 주는 것)
// block scope이 없음 
{
  age = 4;
  var age;
}
console.log(age);


// 5. Constant, r(읽기만 가능, 다른 값으로 쓰기 )
// 한번 할당되면 바뀌지 않음(Immutable)
// 안정적인 프로그램을 위해 변경되어야 할 값이 아니라면 const 사용 권장
const daysInWeek = 7;
const maxNumber = 5;

// Immutable: premitive types, frozen objects (i.e. object.freeze())
// Mutable: JS에서는 대부분 오브젝트는 Mutable

// 6. 변수 타입
// primitive, single item: number, string, boolean, null, undefined, symbol
// object, box container
// function, first-class function


// 연산관련 오류
const infinity = 1 / 0;
const negativeInfinity = -1 / 0;
const nAn = 'not a number' / 2;
console.log(infinity);
console.log(negativeInfinity);
console.log(nAn);


// string
const char = 'c';
const brendan = 'brendan';
const greeting = 'hello ' + brendan;
console.log(`value: ${greeting}, type: ${typeof greeting}`);  //백틱(`) + $ + {} 를 이용하여 변수 할당 가능
const helloBob = `hi ${brendan}!`; 
console.log('value: ' + helloBob + ' type: ' + typeof helloBob); // 이렇게 작성할 필요없이
console.log(`value: ${helloBob}, type: ${typeof helloBob}`); // 이렇게 작성 가능


// boolean
// false: 0, null, undefined, NaN, ''
// true: 그 외의 값
const canRead = true;
const test = 3 < 1; // false


// null
// 아무 것도 없는 값
let nothing = null;


// undefined
// 선언은 되었지만 값이 없는지 있는지 정해져있지 않은 상태
let x; 


// symbol
// 고유식별자가 필요할때 사용
// string은 다른 모듈이나 파일에서 동일한 식별자로 간주되지만 심볼은 다름
const symbol1 = Symbol('id');
const symbol2 = Symbol('id');
console.log(symbol1 === symbol2);  // False, 동일한 스트링을 작성했어도 다른 심볼로 만들어짐(고유함)
const gSymbol1 = Symbol.for('id'); 
const gSymbol2 = Symbol.for('id');
console.log(gSymbol1 === gSymbol2); // true, 동일한 심볼 만들고 싶다면 이렇게 작성
console.log(`value: ${symbol1.description}, type: ${typeof symbol1}`); // 심볼을 바로 출력시 오류, .description을 이용해 string으로 변환후 출력


// object, real-life object, data structure
const apple = { name: 'apple', age: 10 }; // apple이라는 오브젝트 안 변수들은 변경 가능
ellie.age = 11;


// 7. Dynamic typing
// 타입스크립트 탄생 이유
let text = 'hello';  
console.log(text.charAt(0)); // h (이때는 type = string이라서)
console.log(`value: ${text}, type: ${typeof text}`); // type = string
text = 1;
console.log(`value: ${text}, type: ${typeof text}`); // type = number (변경)
text = '7' + 5;
console.log(`value: ${text}, type: ${typeof text}`); // type = string (변경)
text = '8' / '2';
console.log(`value: ${text}, type: ${typeof text}`); // type = number (변경)
console.log(text.charAt(0)); // error 뜸 (type = number라서)

