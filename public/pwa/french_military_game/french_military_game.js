// размер клетки на доске
var step;

// диаметр поля
var d1;

// диаметр фишки
var d2;

// количество клеток на поле
const N = 11;

// расположение фигур на поле
var b = [];

const EMPTY = 0;
const WHITE = 1;
const BLACK = 2;

// начальное расположение фигур на поле
var b0 = [
     0,    // 0
  0, 0, 0, // 1 2 3
  0, 2, 0, // 4 5 6
  1, 0, 1, // 7 8 9
     1     // 10
];

// Возможные ходы для белых (только вперед).
const m = [
  [],
  [0,2],   [0,1,3],      [0,2],
  [1,5],   [1,2,3, 4,6], [3,5],
  [4,5,8], [7,5,9],      [6,5,8],
  [7,8,9]
];

// Возможные ходы для черных (также назад)
const mb = [
  [1,2,3],
  [4,5], [5],     [5,6],
  [7],   [7,8,9], [9],
  [10],  [10],    [10],
  []
];

const xp = [
  2,
  1,2,3,
  1,2,3,
  1,2,3,
  2
];

const yp = [
  1,
  2,2,2,
  3,3,3,
  4,4,4,
  5
];

// чей ход? 
// true: white, false: black
var whiteMove;

// какая фишка сейчас выбрана?
// (-1 если никакая)
var nsel = -1;

// цвет выбранной фишки
var bsel;

// координаты фишки, которую тянут
var xdrag, ydrag;

function setup() {
  createCanvas(533, 800);
  step = height/6;
  d1 = step*0.75;
  d2 = d1*0.75;
  resetButtonSize = step/5;
  resetBoard();
  
  var button = createButton('reset');
  button.position(width, height);
  button.mousePressed(resetBoard);
}

function resetBoard() {
  for (let i=0; i<N; i++) {
    b[i] = b0[i];
  }
  whiteMove = true;
}

function draw() {

  background(255); //color('#f8f4d0'));
  // нарисовать сетку
  for (let i=0; i<N; i++) {
    var p = m[i];
    for (let j=0; j<p.length; j++) {
      var x1 = step*xp[i];
      var y1 = step*yp[i];
      var x2 = step*xp[p[j]];
      var y2 = step*yp[p[j]];
      line(x1,y1,x2,y2);
    }
  }
  
  // нарисовать поля
  for (let i=0; i<N; i++) {
    var xc = step*xp[i];
    var yc = step*yp[i];
    fill(255);
    ellipse(xc,yc, d1,d1);
    if (b[i] != EMPTY) {
      drawPiece(xc,yc, b[i]);
    } 
  }
  
  // фишка которую тянут
  if (nsel != -1) {
    drawPiece(xdrag,ydrag, bsel);
  }
}

function drawPiece(xc,yc, cell) {
  fill(cell === WHITE? 220 : 0);
  ellipse(xc,yc, d2,d2);
  if ((cell === WHITE) ^ whiteMove) {
    return;
  }
  stroke(cell === WHITE? 0 : 200);
  var d = d2;
  for (let i=0; i<2; i++) {
    d *= 0.8;
    ellipse(xc,yc, d,d);
  }
  stroke(0);
}

// номер поля, на которое сейчас указывает мышь
function mouseCell() {
  var x = round(map(mouseX, 0,width,  0,4));
  var y = round(map(mouseY, 0,height, 0,6));
  if (x === 0 || x === 4 || y === 0 || y === 6) {
    return -1;
  }
  var k = y*3 + x;
  //console.log("x="+x+", y="+y+",k="+k);
  return (k >= 7 && k <=15)? k - 6 : (k === 5)? 0 : (k === 17)? 10 : -1;
}

function mousePressed() {
  nsel = mouseCell();
  if (nsel === -1) {
    return;
  }
  // проверить что взята фишка соотв. цвета
  if (!(whiteMove && b[nsel] === WHITE || !whiteMove && b[nsel] === BLACK)) {
    nsel = -1;
    return;
  }
  xdrag = mouseX;
  ydrag = mouseY;
  bsel = b[nsel];
  b[nsel] = EMPTY;
}

function mouseDragged() {
  if (nsel != -1) {
    xdrag = mouseX;
    ydrag = mouseY;
  }
}

function mouseReleased() {
  if (nsel === -1) {
    return;
  }
  // определить координаты нажатой клетки
  var n = mouseCell();
  if (n != -1 && canMove(nsel,n)) {
    b[n] = bsel;
    whiteMove = !whiteMove;
  } else {
    b[nsel] = bsel;
  }
  nsel = -1;
}

function canMove(n1,n2) {
  if (b[n2] != EMPTY) {
    return false;
  }  
  if (arrayContains(m[n1], n2)) {
    return true;
  }
  if (!whiteMove && arrayContains(mb[n1], n2)) {
    return true;
  }
  return false;
}

function arrayContains(arr, n) {
  for (let i=0; i<arr.length; i++) {
    if (arr[i] === n) {
      return true;
    }
  }
  return false;
}
