import checkers

def main():
    """Основная функция для запуска игры в шашки.

    Инициализирует доску для шашек, управляет ходами игроков и отображает состояние доски.
    Игроки поочередно вводят координаты для выполнения ходов. Если есть обязательные взятия,
    игрок должен выполнить их.
    """
    board = checkers.Board()
    move_counter = 0
    current_player = 'white' 
    print("Начальная доска:")
    print(board)
    
    while True:
        def interpretator(coord):
            """Преобразует координаты шашечной доски в индексы массива.

            Аргументы:
                coord (str): Координата на шашечной доске в формате 'a1', 'b2' и т.д.

            Возвращает:
                tuple: Кортеж с индексами (строка, столбец) или None, если координаты некорректны.
            """
            if len(coord) != 2:
                return None
            x = ord(coord[0]) - ord('a') 
            y = 8 - int(coord[1])     
            if 0 <= x < 8 and 0 <= y < 8:
                return (y, x)
            return None
        
        def get_required_captures(player):
            """Возвращает список обязательных взятий для текущего игрока.

            Аргументы:
                player (str): Цвет текущего игрока ('white' или 'black').

            Возвращает:
                list: Список кортежей с начальными и конечными координатами для взятий.
            """
            captures = []
            for row in range(8):
                for col in range(8):
                    piece = board.get_piece((row, col))
                    if piece and piece.color == player:
                        for dx in [-2, 2]:
                            for dy in [-2, 2]:
                                end_row = row + dy
                                end_col = col + dx
                                if 0 <= end_row < 8 and 0 <= end_col < 8:
                                    if piece.can_move(board, (row, col), (end_row, end_col)):
                                        captures.append(((row, col), (end_row, end_col)))
            return captures
        
        def perform_capture(start, end):
            """Выполняет взятие шашки и проверяет возможность дальнейших взятий.

            Аргументы:
                start (tuple): Начальная позиция шашки (строка, столбец).
                end (tuple): Конечная позиция шашки (строка, столбец).

            Возвращает:
                bool: True, если возможно дальнейшее взятие, иначе False.
            """
            if not board.move_piece(start, end):
                return False
            
            piece = board.get_piece(end)
            if piece:
                for dx in [-2, 2]:
                    for dy in [-2, 2]:
                        new_end_row = end[0] + dy
                        new_end_col = end[1] + dx
                        if 0 <= new_end_row < 8 and 0 <= new_end_col < 8:
                            if piece.can_move(board, end, (new_end_row, new_end_col)):
                                return True
            return False
        
        print(f"Сейчас ходят {'черные' if current_player == 'black' else 'белые'}.")
        
        required_captures = get_required_captures(current_player)
        if required_captures:
            print("У вас есть обязательные ходы (взятия):")
            for i, (start, end) in enumerate(required_captures):
                print(f"{i + 1}. {chr(start[1] + ord('a'))}{8 - start[0]} -> {chr(end[1] + ord('a'))}{8 - end[0]}")
            
            while True:
                try:
                    choice = int(input("Выберите номер хода: ")) - 1
                    if 0 <= choice < len(required_captures):
                        start_pos, end_pos = required_captures[choice]
                        break
                    else:
                        print("Некорректный выбор. Попробуйте снова.")
                except ValueError:
                    print("Введите число.")
            
            while True:
                if not perform_capture(start_pos, end_pos):
                    break
                print("Возможно дальнейшее взятие.")
                print(board)
                start_pos = end_pos
                end_pos = interpretator(input('Введите координату для следующего взятия (например, a4): '))
                if end_pos is None:
                    print("Некорректные координаты.")
                    break
        else:
            start_pos = interpretator(input('Введите координату шашки, которой хотите воспользоваться (например, a2): '))
            end_pos = interpretator(input('Введите координату, куда хотите ее передвинуть (например, a3): '))
            
            if start_pos is None or end_pos is None:
                print("Некорректные координаты. Попробуйте снова.")
                continue
            
            piece = board.get_piece(start_pos)
            if piece is None or piece.color != current_player:
                print(f"Вы не можете ходить шашкой противника или пустой клеткой.")
                continue
            
            if not board.move_piece(start_pos, end_pos):
                print("Невозможно выполнить ход. Попробуйте снова.")
                continue

        print("\nДоска после хода:")
        print(board)
        
        current_player = 'black' if current_player == 'white' else 'white'
        
        move_counter += 1
        print(f'Количество ходов: {move_counter}')
    
if __name__ == '__main__':
    main()