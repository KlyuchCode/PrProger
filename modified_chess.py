import chess

def main():
    """Основная функция для запуска шахматной игры с кастомной расстановкой фигур.

    Инициализирует доску с пользовательской расстановкой фигур, управляет ходами игроков
    и отображает состояние доски. Игроки поочередно вводят координаты для выполнения ходов.
    """
    board = chess.Board(custom_setup=[[None for _ in range(8)] for _ in range(8)])
    current_player = 'white'
    move_counter = 0

    board.set_piece((0, 7), chess.DancingKnight('black'))
    board.set_piece((7, 0), chess.DancingKnight('white'))

    board.set_piece((0, 1), chess.Dragon('black'))
    board.set_piece((7, 6), chess.Dragon('white'))

    board.set_piece((0, 5), chess.Tank('black'))
    board.set_piece((7, 2), chess.Tank('white'))

    board.set_piece((0, 4), chess.King('black'))
    board.set_piece((7, 4), chess.King('white'))
    
    board.set_piece((5, 5), chess.Pawn('black'))
    board.set_piece((3, 3), chess.Pawn('white'))
    
    print("Кастомная расстановка:")
    print(board)

    while True:
        def interpretator(coord):
            """Преобразует координаты шахматной доски в индексы массива.

            Аргументы:
                coord (str): Координата на шахматной доске в формате 'a1', 'b2' и т.д.

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
        
        start_pos = interpretator(input('Введите координату фигуры, которой хотите воспользоваться (например, a2): '))
        end_pos = interpretator(input('Введите координату, куда хотите ее передвинуть (например, a4): '))
        
        if start_pos is None or end_pos is None:
            print("Некорректные координаты. Попробуйте снова.")
            continue
        
        piece = board.get_piece(start_pos)
        if piece is None or piece.color != current_player:
            print(f"Вы не можете ходить фигурой противника или пустой клеткой.")
            continue
        
        if not board.move_piece(start_pos, end_pos):
            print("Невозможно выполнить ход.")
            continue

        print("\nДоска после хода:")
        print(board)
        
        opponent = 'black' if current_player == 'white' else 'white'
        if board.is_check(opponent):
            print(f"Король {'черных' if opponent == 'black' else 'белых'} под шахом!")

        current_player = 'black' if current_player == 'white' else 'white'
        
        move_counter += 1
        print(f'Количество ходов: {move_counter}')

if __name__ == '__main__':
    main()
