Шашки
=====

::

  import streamlit as st
  from dataclasses import dataclass
  from typing import List, Tuple, Optional
  import math
  import functools
  import sys

Print banner

::

  st.set_page_config(
      page_title="Checkers"
  )

Board

::

  Board = List[List[str]]  # 8x8

  @dataclass
  class Move:
      # Для взятий seq содержит последовательность позиций (r,c) приземлений
      # start хранит начальную клетку (для удобства печати/применения)
      start: Tuple[int, int]
      seq: List[Tuple[int, int]]
      captured: List[Tuple[int, int]]  # клетки сбитых фигур по порядку
      is_capture: bool

  DIRECTIONS_MAN_WHITE = [(1, -1), (1, 1)]   # обычные ходы белой простой
  DIRECTIONS_MAN_BLACK = [(-1, -1), (-1, 1)]
  DIAGONALS = [(-1,-1),(-1,1),(1,-1),(1,1)]  # для взятий и дамки

  def clone(board: Board) -> Board:
      return [row[:] for row in board]

  def inside(r, c): return 0 <= r < 8 and 0 <= c < 8

  def is_white(p): return p in ('w','W')
  def is_black(p): return p in ('b','B')
  def is_king(p):  return p in ('W','B')

  def side_matches(p: str, side: str) -> bool:
      return (side == 'w' and is_white(p)) or (side == 'b' and is_black(p))

  def enemy_of(side: str) -> str:
      return 'b' if side == 'w' else 'w'

  def parse_board(s: str) -> Board:
      # 8 строк, разделённых \n
      rows = [list(line.strip()) for line in s.strip().splitlines()]
      assert len(rows) == 8 and all(len(r)==8 for r in rows)
      rows.reverse()
      return rows

  def board_to_str(board: Board) -> str:
      return "\n".join("".join(r) for r in board)

  def promote_if_needed(piece: str, r: int, side: str) -> str:
      if piece == 'w' and r == 7:
          return 'W'
      if piece == 'b' and r == 0:
          return 'B'
      return piece

Применить ход

::

  def apply_move(board: Board, move: Move, side: str) -> Board:
      b = clone(board)
      sr, sc = move.start
      piece = b[sr][sc]
      b[sr][sc] = '.'

      r, c = sr, sc
      if move.is_capture:
          for idx, (nr, nc) in enumerate(move.seq):
              # убираем сбитую фигуру
              cr, cc = move.captured[idx]
              b[cr][cc] = '.'
              r, c = nr, nc
              # промежуточная промоция: простая может стать дамкой посреди удара
              if not is_king(piece):
                  piece = promote_if_needed(piece, r, side)
          b[r][c] = piece
      else:
          (r, c) = move.seq[-1]
          # финальная промоция
          piece = promote_if_needed(piece, r, side)
          b[r][c] = piece
      return b\
    
Сгенерировать возможные ходы

::

  def generate_moves(board: Board, side: str) -> List[Move]:
      captures = []
      quiets = []
      for r in range(8):
          for c in range(8):
              p = board[r][c]
              if p == '.' or not side_matches(p, side):
                  continue
              captures.extend(gen_captures_from(board, r, c, side))
      if captures:
          # правило большинства: оставить только с макс количеством взятий
          max_cap = max(len(m.captured) for m in captures)
          return [m for m in captures if len(m.captured) == max_cap]
      # иначе — простые ходы
      for r in range(8):
          for c in range(8):
              p = board[r][c]
              if p == '.' or not side_matches(p, side):
                  continue
              quiets.extend(gen_quiets_from(board, r, c, side))
      return quiets

Сгенерировать простые ходы

::

  def gen_quiets_from(board: Board, r: int, c: int, side: str) -> List[Move]:
      p = board[r][c]
      res = []
      if is_king(p):
          # дамка: любое расстояние по диагонали до первой преграды
          for dr, dc in DIAGONALS:
              nr, nc = r + dr, c + dc
              while inside(nr, nc) and board[nr][nc] == '.':
                  res.append(Move((r,c), [(nr,nc)], [], False))
                  nr += dr; nc += dc
      else:
          dirs = DIRECTIONS_MAN_WHITE if side == 'w' else DIRECTIONS_MAN_BLACK
          for dr, dc in dirs:
              nr, nc = r + dr, c + dc
              if inside(nr, nc) and board[nr][nc] == '.':
                  res.append(Move((r,c), [(nr,nc)], [], False))
      return res

Сгенерировать возможные взятия

::

  def gen_captures_from(board: Board, r: int, c: int, side: str) -> List[Move]:
      p = board[r][c]
      results: List[Move] = []
      visited = set()

      def rec(bd: Board, cr: int, cc: int, piece: str,
              path: List[Tuple[int,int]], caps: List[Tuple[int,int]]):
          key = (cr,cc, tuple(path), tuple(caps), piece)
          if key in visited:
              return
          visited.add(key)

          found = False
          if is_king(piece):
              # дамка: можем "перепрыгнуть" ровно через одну вражескую и встать дальше на любую пустую
              for dr, dc in DIAGONALS:
                  nr, nc = cr + dr, cc + dc
                  # идём, пока пусто
                  while inside(nr, nc) and bd[nr][nc] == '.':
                      nr += dr; nc += dc
                  if inside(nr, nc) and bd[nr][nc] != '.' and side_matches(bd[nr][nc], enemy_of(side)):
                      # нашли вражескую; за ней должны быть пустые клетки приземления
                      j_r, j_c = nr + dr, nc + dc
                      while inside(j_r, j_c) and bd[j_r][j_c] == '.':
                          # выполнить прыжок
                          nb = clone(bd)
                          nb[cr][cc] = '.'
                          nb[nr][nc] = '.'
                          nb[j_r][j_c] = piece
                          # продолжить
                          rec(nb, j_r, j_c, piece, path + [(j_r,j_c)], caps + [(nr,nc)])
                          found = True
                          j_r += dr; j_c += dc
          else:
              # простая: прыгаем на 2 клетки (в любом из 4 диагональных направлений), если там враг и за ним пусто
              for dr, dc in DIAGONALS:
                  mr, mc = cr + dr, cc + dc
                  jr, jc = cr + 2*dr, cc + 2*dc
                  if inside(jr, jc) and inside(mr, mc) and side_matches(bd[mr][mc], enemy_of(side)) and bd[jr][jc] == '.':
                      nb = clone(bd)
                      nb[cr][cc] = '.'
                      nb[mr][mc] = '.'
                      # приземляемся
                      new_piece = promote_if_needed(piece, jr, side)
                      nb[jr][jc] = new_piece
                      # если стали дамкой — продолжим как дамка
                      rec(nb, jr, jc, new_piece, path + [(jr,jc)], caps + [(mr,mc)])
                      found = True

          if not found and caps:
              # конец цепочки взятий
              results.append(Move((r,c), path, caps, True))

      rec(board, r, c, p, [], [])
      if not results:
          return results

      # Фильтрация: убираем те последовательности, множество взятых фигур которых
      # является строгим подмножеством множества взятых фигур другой последовательности.
      filtered: List[Move] = []
      captured_sets = [set(m.captured) for m in results]
      for i, m in enumerate(results):
          mset = captured_sets[i]
          # строгий поднабор?
          if any(mset < otherset for j, otherset in enumerate(captured_sets) if i != j):
              continue
          filtered.append(m)

      # Дополнительно устраним возможные дубликаты одинаковых путей (seq) после фильтра.
      unique = {}
      for mv in filtered:
          key = tuple(mv.seq), tuple(mv.captured)
          unique[key] = mv  # последний побеждает, безразлично
      return list(unique.values())
    
Оценка позиции

::

  def evaluate(board: Board, side_to_move: str) -> int:
      # простая и понятная эвристика
      score = 0
      for r in range(8):
          for c in range(8):
              p = board[r][c]
              if p == '.': 
                  continue
              val = 0
              if p in ('w','b'):
                  val = 100
              elif p in ('W','B'):
                  val = 300
              # небольшие бонусы за продвижение простых и мобильность
              if p == 'w': val += r*3
              if p == 'b': val += (7-r)*3
              score += val if is_white(p) else -val
      # лёгкий бонус стороне хода
      if side_to_move == 'w':
          score += 5
      else:
          score -= 5
      return score

Альфа-бета

::

  @functools.lru_cache(maxsize=100000)
  def _hashable_position(board_str: str, side: str, depth: int, alpha: int, beta: int):
      # Заглушка для lru_cache-совместимости
      return board_str, side, depth, alpha, beta

  def alphabeta(board: Board, side: str, depth: int, alpha: int, beta: int) -> Tuple[int, Optional[Move]]:
      moves = generate_moves(board, side)
      if depth == 0 or not moves:
          return evaluate(board, side), None

      best_move = None
      if side == 'w':
          value = -math.inf
          # упорядочивание: сначала длинные взятия
          moves.sort(key=lambda m: (m.is_capture, len(m.captured)), reverse=True)
          for m in moves:
              nb = apply_move(board, m, side)
              score, _ = alphabeta(nb, 'b', depth-1, alpha, beta)
              if score > value:
                  value = score
                  best_move = m
              alpha = max(alpha, value)
              if alpha >= beta:
                  break
          return int(value), best_move
      else:
          value = math.inf
          moves.sort(key=lambda m: (m.is_capture, len(m.captured)), reverse=True)
          for m in moves:
              nb = apply_move(board, m, side)
              score, _ = alphabeta(nb, 'w', depth-1, alpha, beta)
              if score < value:
                  value = score
                  best_move = m
              beta = min(beta, value)
              if alpha >= beta:
                  break
          return int(value), best_move

Утилита решения задачи (найти лучший ход за указанную сторону)

::

  def solve_position(board_text: str, side: str, depth: int = 8):
      board = parse_board(board_text)
      score, move = alphabeta(board, side, depth, -10**9, 10**9)
      return score, move

Read example position from file

::

  BOARD_EMPTY = """
  _._._._.
  ._._._._
  _._._._.
  ._._._._
  _._._._.
  ._._._._
  _._._._.
  ._._._._
  """.strip()

..
    BOARD_INITIAL = """
    b b b b
    b b b b
    b b b b
    . . . .
    . . . .
    w w w w
    w w w w
    w w w w
    """.strip() 

::

  BOARD_INITIAL = """
  _._._b_.
  ._w_b_._
  _._._._w
  ._._._w_
  _b_._w_.
  ._b_w_._
  _b_._._.
  ._._._._
  """.strip()

  if len(sys.argv) > 1:
      filename = sys.argv[1]
      with open(filename, "r") as f:
          example = f.read().strip()
  else:
      example = BOARD_INITIAL

  col1, col2, col3 = st.columns([7,1,7])

  with col1:
      if st.button("New", width="stretch"):
          example = BOARD_EMPTY
    
      if st.button("Start", width="stretch"):
          example = BOARD_INITIAL
  with col2:  
      row_nums = ""
      for i in range(7, -1, -1):
          row_nums += str(i) + "  \n"
      st.text_area(f".", value=row_nums, height=300)
  with col3:
      example = st.text_area(f"Position", value=example + "\n01234567", height=300)

  if st.button("Solve", type="primary", width="stretch"):
      sc, mv = solve_position(example.replace("\n01234567", ""), 'w', depth=8)
      st.write("Score:", sc)
      if mv:
          st.write("From:", mv.start)
          st.write("Seq:", mv.seq)
          st.write("Captured:", mv.captured) 
          st.write("Capture?" , mv.is_capture)
