class Piece:
    """Базовый класс для шахматных фигур"""

    def __init__(self, color):
        self.color = color  # 'white' или 'black'
        self.has_moved = False

    def symbol(self):
        """Возвращает символ фигуры"""
        raise NotImplementedError

    def can_move(self, board, start_pos, end_pos):
        """Проверяет возможность хода"""
        raise NotImplementedError

    def update_position(self):
        """Обновляет статус фигуры после хода"""
        self.has_moved = True


class Pawn(Piece):
    """Пешка с расширенными правилами"""

    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = -1 if self.color == 'white' else 1

        # Обычный ход вперед
        if start_col == end_col and board.get_piece(end_pos) is None:
            # На одну клетку
            if end_row == start_row + direction:
                return True
            # На две клетки из начальной позиции
            if (not self.has_moved and end_row == start_row + 2 * direction and
                    board.get_piece((start_row + direction, start_col)) is None):
                return True

        # Взятие (по диагонали)
        if (abs(end_col - start_col) == 1 and end_row == start_row + direction and
                board.get_piece(end_pos) is not None and board.get_piece(end_pos).color != self.color):
            return True

        # Взятие на проходе
        if self.en_passant_possible(board, start_pos, end_pos):
            return True

        return False

    def en_passant_possible(self, board, start_pos, end_pos):
        """Проверяет возможность взятия на проходе"""
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = -1 if self.color == 'white' else 1

        # Условия для взятия на проходе
        if (abs(end_col - start_col) == 1 and end_row == start_row + direction and
                board.get_piece(end_pos) is None):

            # Проверяем, есть ли пешка противника рядом
            adjacent_pos = (start_row, end_col)
            adjacent_piece = board.get_piece(adjacent_pos)

            if (isinstance(adjacent_piece, Pawn) and adjacent_piece.color != self.color and
                    board.last_move and board.last_move.piece == adjacent_piece and
                    abs(board.last_move.start_pos[0] - board.last_move.end_pos[0]) == 2):
                return True

        return False

    def promote(self, piece_type):
        """Превращение пешки в другую фигуру"""
        if piece_type.lower() in ['q', 'r', 'b', 'n']:
            return {
                'q': Queen(self.color),
                'r': Rook(self.color),
                'b': Bishop(self.color),
                'n': Knight(self.color)
            }[piece_type.lower()]
        return None


class Rook(Piece):
    """Ладья"""

    def symbol(self):
        return 'R' if self.color == 'white' else 'r'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row != end_row and start_col != end_col:
            return False

        if start_row == end_row:  # Горизонтальное движение
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board.get_piece((start_row, col)) is not None:
                    return False
        else:  # Вертикальное движение
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board.get_piece((row, start_col)) is not None:
                    return False

        target = board.get_piece(end_pos)
        return target is None or target.color != self.color


class Knight(Piece):
    """Конь"""

    def symbol(self):
        return 'N' if self.color == 'white' else 'n'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)


class Bishop(Piece):
    """Слон"""

    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if abs(end_row - start_row) != abs(end_col - start_col):
            return False

        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step

        while row != end_row and col != end_col:
            if board.get_piece((row, col)) is not None:
                return False
            row += row_step
            col += col_step

        target = board.get_piece(end_pos)
        return target is None or target.color != self.color


class Queen(Piece):
    """Ферзь"""

    def symbol(self):
        return 'Q' if self.color == 'white' else 'q'

    def can_move(self, board, start_pos, end_pos):
        rook = Rook(self.color)
        bishop = Bishop(self.color)
        return rook.can_move(board, start_pos, end_pos) or bishop.can_move(board, start_pos, end_pos)


class King(Piece):
    """Король"""

    def symbol(self):
        return 'K' if self.color == 'white' else 'k'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        return abs(end_row - start_row) <= 1 and abs(end_col - start_col) <= 1


class Move:
    """Класс для хранения информации о ходе"""

    def __init__(self, piece, start_pos, end_pos, captured_piece=None, promotion=None, en_passant=False):
        self.piece = piece
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.captured_piece = captured_piece
        self.promotion = promotion  # Тип фигуры при превращении
        self.en_passant = en_passant  # Флаг взятия на проходе
        self.promoted_to = None  # Ссылка на новую фигуру после превращения


class Board:
    """Шахматная доска с историей ходов"""

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.move_history = []
        self.last_move = None  # Последний ход для взятия на проходе
        self.setup_board()

    def setup_board(self):
        """Начальная расстановка фигур"""
        # Ладьи
        self.grid[0][0] = Rook('black')
        self.grid[0][7] = Rook('black')
        self.grid[7][0] = Rook('white')
        self.grid[7][7] = Rook('white')

        # Кони
        self.grid[0][1] = Knight('black')
        self.grid[0][6] = Knight('black')
        self.grid[7][1] = Knight('white')
        self.grid[7][6] = Knight('white')

        # Слоны
        self.grid[0][2] = Bishop('black')
        self.grid[0][5] = Bishop('black')
        self.grid[7][2] = Bishop('white')
        self.grid[7][5] = Bishop('white')

        # Ферзи
        self.grid[0][3] = Queen('black')
        self.grid[7][3] = Queen('white')

        # Короли
        self.grid[0][4] = King('black')
        self.grid[7][4] = King('white')

        # Пешки
        for i in range(8):
            self.grid[1][i] = Pawn('black')
            self.grid[6][i] = Pawn('white')

    def get_piece(self, pos):
        """Возвращает фигуру по позиции"""
        row, col = pos
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        return None

    def move_piece(self, start_pos, end_pos, promotion_choice=None):
        """Выполняет ход с сохранением в истории"""
        piece = self.get_piece(start_pos)
        if not piece:
            return False

        # Проверяем превращение пешки
        promotion = None
        if isinstance(piece, Pawn) and (end_pos[0] == 0 or end_pos[0] == 7):
            if promotion_choice and promotion_choice.lower() in ['q', 'r', 'b', 'n']:
                promotion = promotion_choice.lower()
            else:
                promotion = 'q'  # По умолчанию в ферзя

        # Проверяем взятие на проходе
        en_passant = False
        if isinstance(piece, Pawn) and piece.en_passant_possible(self, start_pos, end_pos):
            en_passant = True

        # Сохраняем информацию о ходе
        captured_piece = self.get_piece(end_pos)
        if en_passant:
            # При взятии на проходе съедаем пешку с другой позиции
            captured_pos = (start_pos[0], end_pos[1])
            captured_piece = self.get_piece(captured_pos)

        move = Move(piece, start_pos, end_pos, captured_piece, promotion, en_passant)

        # Выполняем ход
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Удаляем съеденную фигуру (для взятия на проходе)
        if en_passant:
            self.grid[start_row][end_col] = None

        # Перемещаем фигуру
        self.grid[end_row][end_col] = piece
        self.grid[start_row][start_col] = None

        # Превращение пешки
        if promotion:
            promoted_piece = piece.promote(promotion)
            self.grid[end_row][end_col] = promoted_piece
            move.promoted_to = promoted_piece

        piece.update_position()
        self.move_history.append(move)
        self.last_move = move

        return True

    def undo_move(self, num_moves=1):
        """Откатывает указанное количество ходов"""
        for _ in range(num_moves):
            if not self.move_history:
                return False

            last_move = self.move_history.pop()

            # Возвращаем фигуру на место
            start_row, start_col = last_move.start_pos
            end_row, end_col = last_move.end_pos

            # Если было превращение, возвращаем пешку
            if last_move.promoted_to:
                self.grid[start_row][start_col] = last_move.piece
            else:
                self.grid[start_row][start_col] = last_move.piece

            # Восстанавливаем съеденную фигуру
            if last_move.en_passant:
                # Для взятия на проходе
                self.grid[start_row][end_col] = last_move.captured_piece
                self.grid[end_row][end_col] = None
            else:
                self.grid[end_row][end_col] = last_move.captured_piece

            # Восстанавливаем статус фигуры
            last_move.piece.has_moved = any(
                m.piece == last_move.piece and m.end_pos != last_move.start_pos
                for m in self.move_history
            )

        # Обновляем последний ход
        self.last_move = self.move_history[-1] if self.move_history else None

        return True

    def parse_position(self, pos_str):
        """Преобразует строку в координаты (ряд, колонка)"""
        if len(pos_str) != 2:
            return None
        col = ord(pos_str[0].lower()) - ord('a')
        row = 8 - int(pos_str[1])
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None

    def display(self):
        """Отображает доску"""
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                piece = self.grid[row][col]
                print(piece.symbol() if piece else '.', end=" ")
            print(f"{8 - row}")
        print("  a b c d e f g h")


class ChessGame:
    """Управление игровым процессом"""

    def __init__(self):
        self.board = Board()
        self.current_player = 'white'

    def play(self):
        """Основной игровой цикл"""
        print("Шахматы с откатом ходов и расширенными правилами для пешки")
        print("Команды: 'e2 e4' - ход, 'undo 2' - откат 2 ходов")
        print("При превращении пешки введите: 'e8 q' (ферзь), 'e8 r' (ладья) и т.д.")

        while True:
            self.board.display()
            print(f"\nХод {'белых' if self.current_player == 'white' else 'черных'}")
            print(f"Сделано ходов: {len(self.board.move_history)}")

            command = input("Введите ход или команду: ").strip().lower()

            if command.startswith('undo'):
                try:
                    num = int(command.split()[1]) if len(command.split()) > 1 else 1
                    if self.board.undo_move(num):
                        self.current_player = 'white' if len(self.board.move_history) % 2 == 0 else 'black'
                        print(f"Откатили {num} ход(ов)")
                    else:
                        print("Нельзя откатить - история пуста")
                except ValueError:
                    print("Некорректное число ходов для отката")
                continue

            move = command.split()
            if len(move) not in {2, 3}:
                print("Некорректный ввод. Используйте формат 'e2 e4' или 'e8 q' для превращения")
                continue

            start_pos = self.board.parse_position(move[0])
            end_pos = self.board.parse_position(move[1]) if len(move) > 1 else None

            if not start_pos:
                print("Некорректные координаты")
                continue

            piece = self.board.get_piece(start_pos)
            if not piece or piece.color != self.current_player:
                print("Не ваша фигура или пустая клетка")
                continue

            # Обработка превращения пешки
            if (isinstance(piece, Pawn) and
                    ((piece.color == 'white' and start_pos[0] == 1) or
                     (piece.color == 'black' and start_pos[0] == 6)) and
                    len(move) == 3):
                promotion_choice = move[2]
                if promotion_choice.lower() not in ['q', 'r', 'b', 'n']:
                    print("Некорректный выбор фигуры. Используйте: q, r, b, n")
                    continue

                if self.board.move_piece(start_pos, start_pos, promotion_choice):
                    self.current_player = 'black' if self.current_player == 'white' else 'white'
                continue

            if not end_pos:
                print("Некорректные координаты конечной позиции")
                continue

            if not piece.can_move(self.board, start_pos, end_pos):
                print("Невозможно выполнить такой ход")
                continue

            # Проверяем, нужно ли превращение пешки
            promotion_choice = None
            if (isinstance(piece, Pawn) and
                    (end_pos[0] == 0 or end_pos[0] == 7)):
                print("Выберите фигуру для превращения (Q, R, B, N):")
                promotion_choice = input("> ").strip().lower()
                while promotion_choice not in ['q', 'r', 'b', 'n']:
                    print("Некорректный выбор. Введите Q, R, B или N:")
                    promotion_choice = input("> ").strip().lower()

            if self.board.move_piece(start_pos, end_pos, promotion_choice):
                self.current_player = 'black' if self.current_player == 'white' else 'white'


if __name__ == "__main__":
    game = ChessGame()
    game.play()
