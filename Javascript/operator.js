// 1. 문자역 합치기
console.log('my' + ' cat');
console.log('1' + 2); // 숫자가 문자로 변환
console.log(`string literals: 1 + 2 = ${1 + 2}`); 


// 2. 숫자 연산
console.log(1 + 1); // add
console.log(1 - 1); // substract
console.log(1 / 1); // divide
console.log(1 * 1); // multiply
console.log(5 % 2); // remainder
console.log(2 ** 3); // exponentiation


// 3. ++, -- 오퍼레이터
// 앞에 ++ 붙여준 것을 preincrement라고 하고 아래 코드와 같은 뜻이됨
let counter = 2;
const preIncrement = ++counter; // counter에 1을 더하고 preIncrement에 값을 할당 = 3
// counter = counter + 1; 
// preIncrement = counter; 
console.log(`preIncrement: ${preIncrement}, counter: ${counter}`);
// 뒤에 ++ 붙여준 것을 postincrement라고 함
const postIncrement = counter++; // 먼저 변수의 값을 postIncrement에 할당하고 counter의 값 1 증가 = 4(위에 이어서)
// postIncrement = counter;
// counter = counter + 1;
console.log(`postIncrement: ${postIncrement}, counter: ${counter}`);
const preDecrement = --counter;
console.log(`preDecrement: ${preDecrement}, counter: ${counter}`);
const postDecrement = counter--;
console.log(`postDecrement: ${postDecrement}, counter: ${counter}`);


// 4. 할당
let x = 3;
let y = 6;
x += y; // x = x + y;
x -= y;
x *= y;
x /= y;


// 5. 비교
console.log(10 < 6); // less than
console.log(10 <= 6); // less than or equal
console.log(10 > 6); // greater than
console.log(10 >= 6); // greater than or equal


// 6. 논리연산자: || (or), && (and), ! (not)
const value1 = true; 
const value2 = 4 < 2;  // false

// || (or)
// or 연산자 주의할점!! 순서대로 확인해서 true가 나오면 거기서 멈추게 됨(하나라도 true면 true라서)
// 코드 작성할때 복잡한 연산의 함수를 앞에 두게되면 비효율적이게 됨으로 단순한 값들을 앞쪽에 넣기
console.log(`or: ${value1 || value2 || check()}`);  // check()가 true여서 true리턴

// && (and)
// && (and)연산자도 마찬가지로 단순한 값들을 앞에두기
console.log(`and: ${value1 && value2 && check()}`);

// ! (not) // true -> false, false -> true 
console.log(!value1);


// 7. Equality
const stringFive = '5';
const numberFive = 5;

// == loose equality, 두개(==)는 타입이 달라도 값이 같으면 같은거!
console.log(stringFive == numberFive); // true
console.log(stringFive != numberFive); // false

// === strict equality, 세개(===)는 타입 다르면 다른거!
console.log(stringFive === numberFive); // false
console.log(stringFive !== numberFive); // true

// 오브젝트는 메모리에 탑재될 때 레퍼런스 형태로 저장 됨
const ellie1 = { name: 'ellie' };
const ellie2 = { name: 'ellie' };
const ellie3 = ellie1;
console.log(ellie1 == ellie2); // false
console.log(ellie1 === ellie2); // false
console.log(ellie1 === ellie3); // true


// 8. 조건문: if
// if, else if, else
const name = 'df';
if (name === 'ellie') {
  console.log('Welcome, Ellie!');
} else if (name === 'coder') {
  console.log('You are amazing coder');
} else {
  console.log('unkwnon');
}


// 9. 삼항연산자: ?
// "?" 앞에 있는 내용이 참이면 콜론(:)의 왼쪽 실행, 거짓이면 오른쪽 실행
// condition ? value1 : value2;
console.log(name === 'ellie' ? 'yes' : 'no');


// 10. Switch문
// if 문을 다수로 많이 사용할 때 사용
const browser = 'IE';
switch (browser) {
  case 'IE':
    console.log('go away!');
    break;
  case 'Chrome':
  case 'Firefox':
    console.log('love you!');
    break;
  default:
    console.log('same all!');
    break;
}

// 11. Loops
let i = 3;
while (i > 0) {
  console.log(`while: ${i}`);
  i--;
}

// do while loop
// 블럭안에 내용을 먼저 실행하고 while 실행
do {
  console.log(`do while: ${i}`);
  i--;
} while (i > 0);

// for loop
// for(시작하는 문장; condition; 어떤 것을 할건지)
for (i = 3; i > 0; i--) {
  console.log(`for: ${i}`);
}

for (let i = 3; i > 0; i = i - 2) {  // 블럭안에 지역변수 선언해서 사용도 가능
  // inline variable declaration
  console.log(`inline variable for: ${i}`);
}

// nested loops
for (let i = 0; i < 10; i++) {
  for (let j = 0; j < 10; j++) {
    console.log(`i: ${i}, j:${j}`);
  }
}

// continue
for (let i = 0; i < 11; i++) {
  if (i % 2 === 0) {
    continue;
  }
  console.log(`q1. ${i}`);
}

// break
for (let i = 0; i < 11; i++) {
  if (i > 8) {
    break;
  }
  console.log(`q2. ${i}`);
}
