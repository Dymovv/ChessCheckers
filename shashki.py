class Piece:
    """Базовый класс для всех игровых фигур"""

    def __init__(self, color):
        self.color = color  # 'white' или 'black'

    def symbol(self):
        """Возвращает символ фигуры"""
        raise NotImplementedError

    def can_move(self, board, start_pos, end_pos):
        """Проверяет возможность хода"""
        raise NotImplementedError


class Checker(Piece):
    """Класс для шашки"""

    def __init__(self, color):
        super().__init__(color)
        self.is_king = False  # Флаг дамки

    def symbol(self):
        if self.is_king:
            return '★' if self.color == 'white' else '☆'
        return 'W' if self.color == 'white' else 'B'

    def can_move(self, board, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        direction = -1 if self.color == 'white' else 1

        # Проверка на выход за пределы доски
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        # Для дамки разрешаем ход назад
        if self.is_king:
            direction = 1 if abs(end_row - start_row) > 0 else -1

        # Обычный ход (без взятия)
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            return board.get_piece(end_pos) is None

        # Взятие шашки противника
        if abs(end_col - start_col) == 2 and abs(end_row - start_row) == 2:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            middle_piece = board.get_piece((middle_row, middle_col))

            # Проверяем что между начальной и конечной позицией есть шашка противника
            if (middle_piece is not None and
                    middle_piece.color != self.color and
                    board.get_piece(end_pos) is None):
                return True

        return False


class Board:
    """Класс игровой доски"""

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        self.move_count = 0

    def setup_board(self):
        """Расстановка шашек на доске"""
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Checker('black')

        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.grid[row][col] = Checker('white')

    def get_piece(self, pos):
        """Возвращает фигуру на указанной позиции"""
        row, col = pos
        return self.grid[row][col]

    def display(self):
        """Отображает доску в консоли"""
        print("   a b c d e f g h")
        print("  +-----------------+")
        for row in range(8):
            print(f"{8 - row} |", end="")
            for col in range(8):
                piece = self.grid[row][col]
                print(piece.symbol() if piece else '·', end=" ")
            print(f"| {8 - row}")
        print("  +-----------------+")
        print("   a b c d e f g h")

    def move_piece(self, start, end):
        """Выполняет ход шашки"""
        start_pos = self.parse_position(start)
        end_pos = self.parse_position(end)

        if not start_pos or not end_pos:
            print("Некорректные координаты!")
            return False

        piece = self.get_piece(start_pos)
        if not piece or not isinstance(piece, Checker):
            print("На начальной позиции нет шашки!")
            return False

        if not piece.can_move(self, start_pos, end_pos):
            print("Невозможно выполнить такой ход!")
            return False

        # Выполняем ход
        self.grid[end_pos[0]][end_pos[1]] = piece
        self.grid[start_pos[0]][start_pos[1]] = None

        # Если это было взятие - удаляем побитую шашку
        if abs(end_pos[0] - start_pos[0]) == 2:
            middle_row = (start_pos[0] + end_pos[0]) // 2
            middle_col = (start_pos[1] + end_pos[1]) // 2
            self.grid[middle_row][middle_col] = None
            print(f"Шашка на {chr(middle_col + ord('a'))}{8 - middle_row} взята!")

        # Проверяем, стала ли шашка дамкой
        if (piece.color == 'white' and end_pos[0] == 0) or (piece.color == 'black' and end_pos[0] == 7):
            piece.is_king = True
            print("Шашка стала дамкой!")

        self.move_count += 1
        return True

    def parse_position(self, pos_str):
        """Преобразует строку типа 'a3' в координаты (ряд, колонка)"""
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


class CheckersGame:
    """Класс управления игрой"""

    def __init__(self):
        self.board = Board()
        self.current_player = 'white'

    def play(self):
        """Основной игровой цикл"""
        print("Добро пожаловать в игру Шашки!")
        print("Для хода введите две позиции, например: a3 b4")
        print("Для взятия шашки перепрыгните через неё, например: a3 c5")

        while True:
            self.board.display()
            print(f"\nХод {'белых' if self.current_player == 'white' else 'черных'} (ход №{self.board.move_count + 1})")

            move = input("Введите ход (например, 'a3 b4'): ").strip().lower().split()
            if len(move) != 2:
                print("Ошибка: нужно ввести две позиции, например 'a3 b4'")
                continue

            if self.board.move_piece(move[0], move[1]):
                # Проверяем, можно ли сделать еще одно взятие этой же шашкой
                end_pos = self.board.parse_position(move[1])
                piece = self.board.get_piece(end_pos)

                # Если был взят противник, проверяем возможность продолжения взятия
                if abs(self.board.parse_position(move[0])[0] - end_pos[0]) == 2:
                    if self.can_capture_again(end_pos):
                        print("Можно продолжить взятие этой же шашкой!")
                        continue

                self.current_player = 'black' if self.current_player == 'white' else 'white'

    def can_capture_again(self, pos):
        """Проверяет, может ли шашка на данной позиции взять еще одну шашку"""
        piece = self.board.get_piece(pos)
        if not piece:
            return False

        row, col = pos
        directions = []

        # Для обычной шашки
        if not piece.is_king:
            directions = [(-1, -1), (-1, 1)] if piece.color == 'white' else [(1, -1), (1, 1)]
        else:  # Для дамки
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            # Проверяем возможность взятия в каждом направлении
            jump_row = row + 2 * dr
            jump_col = col + 2 * dc

            if 0 <= jump_row < 8 and 0 <= jump_col < 8:
                middle_row = row + dr
                middle_col = col + dc
                middle_piece = self.board.get_piece((middle_row, middle_col))

                if (middle_piece is not None and
                        middle_piece.color != piece.color and
                        self.board.get_piece((jump_row, jump_col)) is None):
                    return True

        return False


if __name__ == "__main__":
    game = CheckersGame()
    game.play()