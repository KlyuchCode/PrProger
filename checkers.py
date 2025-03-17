from typing import List, Optional, Tuple

class Piece:
    """Базовый класс для шахматных фигур.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
    """

    def __init__(self, color):
        """Инициализирует фигуру с указанным цветом.

        Аргументы:
            color (str): Цвет фигуры ('white' или 'black').
        """
        self.color = color

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли фигура переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция фигуры (строка, столбец).
            end (Tuple[int, int]): Конечная позиция фигуры (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.

        Исключения:
            NotImplementedError: Метод должен быть реализован в подклассе.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")

    def __str__(self):
        """Возвращает строковое представление фигуры.

        Возвращает:
            str: Символ фигуры в верхнем регистре для белых и в нижнем для черных.
        """
        symbol = self.get_symbol()
        return symbol.upper() if self.color == 'white' else symbol.lower()

    def get_symbol(self):
        """Возвращает символ фигуры.

        Возвращает:
            str: Символ фигуры.

        Исключения:
            NotImplementedError: Метод должен быть реализован в подклассе.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")


class Checker(Piece):
    """Класс, представляющий шашку.

    Атрибуты:
        color (str): Цвет шашки ('white' или 'black').
        is_queen (bool): Флаг, указывающий, является ли шашка дамкой.
    """

    def __init__(self, color: str, is_queen: bool = False):
        """Инициализирует шашку с указанным цветом и статусом дамки.

        Аргументы:
            color (str): Цвет шашки ('white' или 'black').
            is_queen (bool): Флаг, указывающий, является ли шашка дамкой.
        """
        super().__init__(color)
        self.is_queen = is_queen

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли шашка переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция шашки (строка, столбец).
            end (Tuple[int, int]): Конечная позиция шашки (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end

        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        if board.get_piece(end) is not None:
            return False

        direction = -1 if self.color == 'white' else 1

        if not self.is_queen:
            if abs(start_col - end_col) == 1 and end_row == start_row + direction:
                return True

            if abs(start_col - end_col) == 2 and end_row == start_row + 2 * direction:
                middle_row = (start_row + end_row) // 2
                middle_col = (start_col + end_col) // 2
                middle_piece = board.get_piece((middle_row, middle_col))
                return middle_piece is not None and middle_piece.color != self.color
        else:
            if abs(start_col - end_col) == abs(start_row - end_row):
                step_row = 1 if end_row > start_row else -1
                step_col = 1 if end_col > start_col else -1
                row, col = start_row + step_row, start_col + step_col
                while row != end_row and col != end_col:
                    if board.get_piece((row, col)) is not None:
                        return False
                    row += step_row
                    col += step_col
                return True

        return False

    def get_symbol(self) -> str:
        """Возвращает символ шашки.

        Возвращает:
            str: Символ шашки ('O' для обычной шашки, 'K' для дамки).
        """
        return 'O' if not self.is_queen else 'K'


class Board:
    """Класс, представляющий доску для игры в шашки.

    Атрибуты:
        board (List[List[Optional[Piece]]]): Двумерный список, представляющий доску.
    """

    def __init__(self):
        """Инициализирует доску и расставляет шашки в начальные позиции."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_checkers()

    def setup_checkers(self):
        """Расставляет шашки на доске в начальные позиции."""
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Checker('black')
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.board[row][col] = Checker('white')

    def get_piece(self, position) -> Optional[Piece]:
        """Возвращает фигуру на указанной позиции.

        Аргументы:
            position (Tuple[int, int]): Позиция на доске (строка, столбец).

        Возвращает:
            Optional[Piece]: Фигура на указанной позиции или None, если позиция пуста.
        """
        row, col = position
        return self.board[row][col]

    def set_piece(self, position: Tuple[int, int], piece: Optional[Piece]):
        """Устанавливает фигуру на указанную позицию.

        Аргументы:
            position (Tuple[int, int]): Позиция на доске (строка, столбец).
            piece (Optional[Piece]): Фигура, которую нужно установить.
        """
        row, col = position
        self.board[row][col] = piece

    def move_piece(self, start, end) -> bool:
        """Перемещает фигуру с начальной позиции на конечную.

        Аргументы:
            start (Tuple[int, int]): Начальная позиция фигуры (строка, столбец).
            end (Tuple[int, int]): Конечная позиция фигуры (строка, столбец).

        Возвращает:
            bool: True, если перемещение успешно, иначе False.
        """
        if start is None or end is None:
            return False
        
        piece = self.get_piece(start)
        if piece is None or not piece.can_move(self, start, end):
            return False

        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

        if isinstance(piece, Checker) and not piece.is_queen:
            if (piece.color == 'white' and end[0] == 0) or (piece.color == 'black' and end[0] == 7):
                piece.is_queen = True

        if abs(start[0] - end[0]) == 2:
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            self.board[middle_row][middle_col] = None

        return True

    def __str__(self):
        """Возвращает строковое представление доски.

        Возвращает:
            str: Строковое представление доски с координатами.
        """
        result = []
        result.append("  a b c d e f g h")
        for i, row in enumerate(self.board):
            row_str = ' '.join([str(piece) if piece else '.' for piece in row])
            result.append(f"{8 - i} {row_str} {8 - i}")
        result.append("  a b c d e f g h")
        return '\n'.join(result)