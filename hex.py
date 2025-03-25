class Piece:
    """Базовый класс для всех шахматных фигур"""

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
    """Пешка"""

    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def can_move(self, board, start_pos, end_pos):
        # Реализация стандартных правил для пешки
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = -1 if self.color == 'white' else 1

        # Обычный ход
        if start_col == end_col:
            if end_row == start_row + direction and board.grid[end_row][end_col] is None:
                return True
            if not self.has_moved and end_row == start_row + 2 * direction and board.grid[end_row][end_col] is None:
                return board.grid[start_row + direction][start_col] is None

        # Взятие
        elif abs(end_col - start_col) == 1 and end_row == start_row + direction:
            return board.grid[end_row][end_col] is not None and board.grid[end_row][end_col].color != self.color

        return False


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
                if board.grid[start_row][col] is not None:
                    return False
        else:  # Вертикальное движение
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board.grid[row][start_col] is not None:
                    return False

        target = board.grid[end_row][end_col]
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
            if board.grid[row][col] is not None:
                return False
            row += row_step
            col += col_step

        target = board.grid[end_row][end_col]
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


class Griffin(Piece):
    """Грифон - сочетает движения коня и слона"""

    def symbol(self):
        return 'G' if self.color == 'white' else 'g'

    def can_move(self, board, start_pos, end_pos):
        knight = Knight(self.color)
        bishop = Bishop(self.color)
        return knight.can_move(board, start_pos, end_pos) or bishop.can_move(board, start_pos, end_pos)


class Centaur(Piece):
    """Кентавр - ходит как конь или король"""

    def symbol(self):
        return 'C' if self.color == 'white' else 'c'

    def can_move(self, board, start_pos, end_pos):
        knight = Knight(self.color)
        king = King(self.color)
        return knight.can_move(board, start_pos, end_pos) or king.can_move(board, start_pos, end_pos)


class Crossbowman(Piece):
    """Арбалетчик - ходит на 2 или 3 клетки по вертикали/горизонтали"""

    def symbol(self):
        return 'A' if self.color == 'white' else 'a'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if start_row != end_row and start_col != end_col:
            return False

        distance = max(abs(end_row - start_row), abs(end_col - start_col))
        if distance not in {2, 3}:
            return False

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

        target = board.grid[end_row][end_col]
        return target is None or target.color != self.color


class Board:
    """Шахматная доска"""

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.move_count = 0

    def setup_board(self):
        """Расстановка фигур с новыми типами"""
        # Пешки
        for i in range(8):
            self.grid[1][i] = Pawn('black')
            self.grid[6][i] = Pawn('white')

        # Ладьи
        self.grid[0][0] = self.grid[0][7] = Rook('black')
        self.grid[7][0] = self.grid[7][7] = Rook('white')

        # Кентавры вместо коней
        self.grid[0][1] = self.grid[0][6] = Centaur('black')
        self.grid[7][1] = self.grid[7][6] = Centaur('white')

        # Грифоны вместо слонов
        self.grid[0][2] = self.grid[0][5] = Griffin('black')
        self.grid[7][2] = self.grid[7][5] = Griffin('white')

        # Арбалетчики вместо ферзей
        self.grid[0][3] = Crossbowman('black')
        self.grid[7][3] = Crossbowman('white')

        # Короли
        self.grid[0][4] = King('black')
        self.grid[7][4] = King('white')

    def display(self):
        """Отображение доски"""
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                piece = self.grid[row][col]
                print(piece.symbol() if piece else '.', end=" ")
            print(f"{8 - row}")
        print("  a b c d e f g h")

    def move_piece(self, start, end):
        """Выполнение хода"""
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

        self.grid[end_pos[0]][end_pos[1]] = piece
        self.grid[start_pos[0]][start_pos[1]] = None
        piece.update_position()
        self.move_count += 1
        return True

    def parse_position(self, pos_str):
        """Преобразование строки в координаты"""
        if len(pos_str) != 2:
            return None
        col = ord(pos_str[0].lower()) - ord('a')
        row = 8 - int(pos_str[1])
        if 0 <= row < 8 and 0 <= col < 8:
            return (row, col)
        return None


class ChessGame:
    """Управление игровым процессом"""

    def __init__(self):
        self.board = Board()
        self.current_player = 'white'

    def play(self):
        """Основной игровой цикл"""
        print("Шахматы с новыми фигурами: Грифон (G), Кентавр (C), Арбалетчик (A)")
        while True:
            self.board.display()
            print(f"\nХод {'белых' if self.current_player == 'white' else 'черных'}")

            move = input("Введите ход (например 'e2 e4'): ").split()
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
