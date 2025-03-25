class Piece:
    """Базовый класс для шахматных фигур"""

    def __init__(self, color):
        self.color = color  # 'white' или 'black'

    def symbol(self):
        """Возвращает символ фигуры для отображения на доске"""
        raise NotImplementedError

    def can_move(self, board, start_pos, end_pos):
        """Проверяет, может ли фигура переместиться с start_pos на end_pos"""
        raise NotImplementedError


class Pawn(Piece):
    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def can_move(self, board, start_pos, end_pos):
        # Реализация правил движения пешки
        direction = -1 if self.color == 'white' else 1
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Пешка движется вперед
        if start_col == end_col:
            # Обычный ход на 1 клетку
            if end_row == start_row + direction and board.grid[end_row][end_col] is None:
                return True
            # Первый ход на 2 клетки
            if ((self.color == 'white' and start_row == 6) or
                    (self.color == 'black' and start_row == 1)):
                if end_row == start_row + 2 * direction and board.grid[end_row][end_col] is None:
                    return True
        # Взятие фигуры
        elif abs(end_col - start_col) == 1 and end_row == start_row + direction:
            target = board.grid[end_row][end_col]
            return target is not None and target.color != self.color

        return False


class Rook(Piece):
    def symbol(self):
        return 'R' if self.color == 'white' else 'r'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Ладья ходит по прямой
        if start_row != end_row and start_col != end_col:
            return False

        # Проверка, что нет фигур на пути
        if start_row == end_row:  # Горизонтальное движение
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board.grid[start_row][col] is not None:
                    return False
        else:  # Вертикальное движение
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board.grid[row][start_col] is not None:
                    return False

        # Проверка конечной позиции
        target = board.grid[end_row][end_col]
        return target is None or target.color != self.color


class Knight(Piece):
    def symbol(self):
        return 'N' if self.color == 'white' else 'n'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Конь ходит буквой "Г"
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)

        if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
            return False

        target = board.grid[end_row][end_col]
        return target is None or target.color != self.color


class Bishop(Piece):
    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Слон ходит по диагонали
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False

        # Проверка, что нет фигур на пути
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step

        while row != end_row and col != end_col:
            if board.grid[row][col] is not None:
                return False
            row += row_step
            col += col_step

        target = board.grid[end_row][end_col]
        return target is None or target.color != self.color


class Queen(Piece):
    def symbol(self):
        return 'Q' if self.color == 'white' else 'q'

    def can_move(self, board, start_pos, end_pos):
        # Ферзь сочетает возможности ладьи и слона
        rook_move = Rook(self.color).can_move(board, start_pos, end_pos)
        bishop_move = Bishop(self.color).can_move(board, start_pos, end_pos)
        return rook_move or bishop_move


class King(Piece):
    def symbol(self):
        return 'K' if self.color == 'white' else 'k'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Король ходит на одну клетку в любом направлении
        if abs(end_row - start_row) > 1 or abs(end_col - start_col) > 1:
            return False

        target = board.grid[end_row][end_col]
        return target is None or target.color != self.color


class Board:
    """Класс, представляющий шахматную доску"""

    def __init__(self):
        self.setup_board()
        self.move_count = 0

    def setup_board(self):
        """Инициализация начальной расстановки фигур"""
        self.grid = [[None for _ in range(8)] for _ in range(8)]

        # Расстановка пешек
        for i in range(8):
            self.grid[1][i] = Pawn('black')
            self.grid[6][i] = Pawn('white')

        # Расстановка ладей
        self.grid[0][0] = self.grid[0][7] = Rook('black')
        self.grid[7][0] = self.grid[7][7] = Rook('white')

        # Расстановка коней
        self.grid[0][1] = self.grid[0][6] = Knight('black')
        self.grid[7][1] = self.grid[7][6] = Knight('white')

        # Расстановка слонов
        self.grid[0][2] = self.grid[0][5] = Bishop('black')
        self.grid[7][2] = self.grid[7][5] = Bishop('white')

        # Расстановка ферзей
        self.grid[0][3] = Queen('black')
        self.grid[7][3] = Queen('white')

        # Расстановка королей
        self.grid[0][4] = King('black')
        self.grid[7][4] = King('white')

    def display(self):
        """Отображение доски в консоли"""
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                piece = self.grid[row][col]
                print(piece.symbol() if piece else '.', end=" ")
            print(f"{8 - row}")
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        """Попытка перемещения фигуры"""
        start_pos = self.parse_position(start)
        end_pos = self.parse_position(end)

        if not start_pos or not end_pos:
            print("Некорректные координаты")
            return False

        piece = self.grid[start_pos[0]][start_pos[1]]
        if not piece:
            print("На начальной позиции нет фигуры")
            return False

        if not piece.can_move(self, start_pos, end_pos):
            print("Невозможно выполнить такой ход")
            return False

        # Выполняем ход
        self.grid[end_pos[0]][end_pos[1]] = piece
        self.grid[start_pos[0]][start_pos[1]] = None
        self.move_count += 1
        return True

    def parse_position(self, pos_str):
        """Преобразует строку типа 'e2' в координаты (ряд, колонка)"""
        if len(pos_str) != 2:
            return None
        col = ord(pos_str[0].lower()) - ord('a')
        if col < 0 or col > 7:
            return None
        try:
            row = 8 - int(pos_str[1])
            if row < 0 or row > 7:
                return None
            return (row, col)
        except ValueError:
            return None


class ChessGame:
    """Основной класс игры"""

    def __init__(self):
        self.board = Board()
        self.current_player = 'white'

    def play(self):
        """Основной игровой цикл"""
        print("Шахматы. Для хода введите две позиции, например: e2 e4")
        while True:
            self.board.display()
            print(f"Ход {'белых' if self.current_player == 'white' else 'черных'}")

            move = input("Введите ход (например, 'e2 e4'): ").strip().split()
            if len(move) != 2:
                print("Некорректный ввод. Используйте формат 'e2 e4'")
                continue

            if self.board.move_piece(move[0], move[1]):
                self.current_player = 'black' if self.current_player == 'white' else 'white'
            else:
                print("Попробуйте снова.")


if __name__ == "__main__":
    game = ChessGame()
    game.play()
    