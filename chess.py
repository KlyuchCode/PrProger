from typing import List, Optional, Tuple

class Piece:
    """Базовый класс для шахматных фигур.

    Атрибуты:
        color (str): Цвет фигуры ('white' или 'black').
    """

    def __init__(self, color: str):
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

    def get_symbol(self) -> str:
        """Возвращает символ фигуры.

        Возвращает:
            str: Символ фигуры.

        Исключения:
            NotImplementedError: Метод должен быть реализован в подклассе.
        """
        raise NotImplementedError("Метод должен быть реализован в подклассе")


class Pawn(Piece):
    """Класс, представляющий пешку."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли пешка переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция пешки (строка, столбец).
            end (Tuple[int, int]): Конечная позиция пешки (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        direction = -1 if self.color == 'white' else 1
        start_row, start_col = start
        end_row, end_col = end

        if start_col == end_col and end_row == start_row + direction:
            return board.get_piece(end) is None
        if start_col == end_col and end_row == start_row + 2 * direction:
            if (self.color == 'white' and start_row == 6) or (self.color == 'black' and start_row == 1):
                return board.get_piece(end) is None and board.get_piece((start_row + direction, start_col)) is None
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            target_piece = board.get_piece(end)
            return target_piece is not None and target_piece.color != self.color
        return False

    def get_symbol(self) -> str:
        """Возвращает символ пешки.

        Возвращает:
            str: Символ пешки ('P').
        """
        return 'P'


class Rook(Piece):
    """Класс, представляющий ладью."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли ладья переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция ладьи (строка, столбец).
            end (Tuple[int, int]): Конечная позиция ладьи (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end

        if start_row != end_row and start_col != end_col:
            return False

        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board.get_piece((start_row, col)) is not None:
                    return False
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board.get_piece((row, start_col)) is not None:
                    return False
        return True

    def get_symbol(self) -> str:
        """Возвращает символ ладьи.

        Возвращает:
            str: Символ ладьи ('R').
        """
        return 'R'


class Knight(Piece):
    """Класс, представляющий коня."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли конь переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция коня (строка, столбец).
            end (Tuple[int, int]): Конечная позиция коня (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) * abs(start_col - end_col) == 2

    def get_symbol(self) -> str:
        """Возвращает символ коня.

        Возвращает:
            str: Символ коня ('N').
        """
        return 'N'


class Bishop(Piece):
    """Класс, представляющий слона."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли слон переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция слона (строка, столбец).
            end (Tuple[int, int]): Конечная позиция слона (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end

        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1
        row, col = start_row + step_row, start_col + step_col
        while row != end_row and col != end_col:
            if board.get_piece((row, col)) is not None:
                return False
            row += step_row
            col += step_col
        return True

    def get_symbol(self) -> str:
        """Возвращает символ слона.

        Возвращает:
            str: Символ слона ('B').
        """
        return 'B'


class Queen(Piece):
    """Класс, представляющий ферзя."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли ферзь переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция ферзя (строка, столбец).
            end (Tuple[int, int]): Конечная позиция ферзя (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        return Rook(self.color).can_move(board, start, end) or Bishop(self.color).can_move(board, start, end)

    def get_symbol(self) -> str:
        """Возвращает символ ферзя.

        Возвращает:
            str: Символ ферзя ('Q').
        """
        return 'Q'


class King(Piece):
    """Класс, представляющий короля."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли король переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция короля (строка, столбец).
            end (Tuple[int, int]): Конечная позиция короля (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    def get_symbol(self) -> str:
        """Возвращает символ короля.

        Возвращает:
            str: Символ короля ('K').
        """
        return 'K'


class Dragon(Piece):
    """Класс, представляющий дракона (нестандартная фигура)."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли дракон переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция дракона (строка, столбец).
            end (Tuple[int, int]): Конечная позиция дракона (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end

        knight_move = abs(start_row - end_row) * abs(start_col - end_col) == 2
        if knight_move:
            return True

        if abs(start_row - end_row) == abs(start_col - end_col):
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
        """Возвращает символ дракона.

        Возвращает:
            str: Символ дракона ('D').
        """
        return 'D'


class Tank(Piece):
    """Класс, представляющий танк (нестандартная фигура)."""

    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """Проверяет, может ли танк переместиться на указанную позицию.

        Аргументы:
            board (Board): Доска, на которой происходит игра.
            start (Tuple[int, int]): Начальная позиция танка (строка, столбец).
            end (Tuple[int, int]): Конечная позиция танка (строка, столбец).

        Возвращает:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end

        if start_col != end_col:
            return False 
        if abs(start_row - end_row) != 1:
            return False

        target_piece = board.get_piece(end)
        if target_piece is not None and target_piece.color != self.color:
            return True

        return board.get_piece(end) is None

    def get_symbol(self) -> str:
        """Возвращает символ танка.

        Возвращает:
            str: Символ танка ('T').
        """
        return 'T'


class DancingKnight(Piece):
    """
    Класс, представляющий фигуру "Танцующий рыцарь".

    Танцующий рыцарь двигается сначала как конь, а затем, если это возможно, делает дополнительный шаг, 
    как король (на одну клетку влево по диагонали).
    """
    
    def can_move(self, board: 'Board', start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """
        Проверяет, может ли фигура переместиться из начальной позиции в конечную.

        Сначала выполняется ход конем (L-образное движение), затем проверяется возможность 
        дополнительного хода на одну клетку в любом направлении.

        Args:
            board (Board): Игровая доска.
            start (Tuple[int, int]): Координаты начальной позиции (строка, колонка).
            end (Tuple[int, int]): Координаты конечной позиции (строка, колонка).

        Returns:
            bool: True, если ход возможен, иначе False.
        """
        start_row, start_col = start
        end_row, end_col = end

        if (abs(start_row - end_row), abs(start_col - end_col)) not in [(2, 1), (1, 2)]:
            return False

        target_piece = board.get_piece(end)
        if target_piece is not None and target_piece.color == self.color:
            return False

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  
                new_row, new_col = end_row + dr, end_col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target_piece = board.get_piece((new_row, new_col))
                    if target_piece is None or target_piece.color != self.color:
                        return True  

        return False 
    
    def get_symbol(self) -> str:
        """
        Возвращает символ, обозначающий фигуру на доске.

        Returns:
            str: Символ 'H'.
        """
        return 'H'

    def get_symbol(self) -> str:
        """Возвращает символ танцующего коня.

        Возвращает:
            str: Символ танцующего коня ('H').
        """
        return 'H'


class Board:
    """Класс, представляющий шахматную доску.

    Атрибуты:
        board (List[List[Optional[Piece]]]): Двумерный список, представляющий доску.
    """

    def __init__(self, custom_setup: Optional[List[List[Optional[Piece]]]] = None):
        """Инициализирует доску.

        Аргументы:
            custom_setup (Optional[List[List[Optional[Piece]]]]): Пользовательская расстановка фигур.
                Если не указана, используется стандартная расстановка.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        if custom_setup:
            self.board = custom_setup
        else:
            self.setup_default_board()

    def setup_default_board(self):
        """Устанавливает стандартную расстановку фигур на доске."""
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')

        self.board[0][0] = Rook('black')
        self.board[0][7] = Rook('black')
        self.board[7][0] = Rook('white')
        self.board[7][7] = Rook('white')

        self.board[0][1] = Knight('black')
        self.board[0][6] = Knight('black')
        self.board[7][1] = Knight('white')
        self.board[7][6] = Knight('white')

        self.board[0][2] = Bishop('black')
        self.board[0][5] = Bishop('black')
        self.board[7][2] = Bishop('white')
        self.board[7][5] = Bishop('white')

        self.board[0][3] = Queen('black')
        self.board[7][3] = Queen('white')

        self.board[0][4] = King('black')
        self.board[7][4] = King('white')

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

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """
        Перемещает фигуру с одной позиции на другую.
        
        Если перемещаемая фигура — Танцующий рыцарь, он сначала двигается как конь,
        а затем, если возможно, делает дополнительный ход как король.
        
        Args:
            start (Tuple[int, int]): Координаты начальной позиции (строка, колонка).
            end (Tuple[int, int]): Координаты конечной позиции (строка, колонка).
        
        Returns:
            bool: True, если ход выполнен успешно, иначе False.
        """
        piece = self.get_piece(start)
        if piece is None or not piece.can_move(self, start, end):
            return False

        if isinstance(piece, DancingKnight):
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None

            second_move_made = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    new_row, new_col = end[0] + dr, end[1] + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        target_piece = self.get_piece((new_row, new_col))
                        if target_piece is None or target_piece.color != piece.color:
                            self.board[new_row][new_col] = piece
                            self.board[end[0]][end[1]] = None
                            second_move_made = True
                            break
                if second_move_made:
                    break

            if not second_move_made:
                self.board[start[0]][start[1]] = piece
                self.board[end[0]][end[1]] = None
                return False

        else:
            self.board[end[0]][end[1]] = piece
            self.board[start[0]][start[1]] = None

        return True

    def is_check(self, color: str) -> bool:
        """Проверяет, находится ли король указанного цвета под шахом.

        Аргументы:
            color (str): Цвет короля ('white' или 'black').

        Возвращает:
            bool: True, если король под шахом, иначе False.
        """
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if isinstance(piece, King) and piece.color == color:
                    king_position = (row, col)
                    break
            if king_position:
                break

        if not king_position:
            return False

        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece and piece.color != color and piece.can_move(self, (row, col), king_position):
                    return True
        return False

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
