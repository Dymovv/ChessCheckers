class HexBoard:
    """Доска для гексагональных шахмат с правильным отображением"""

    def __init__(self):
        self.size = 5  # Радиус доски
        self.grid = {}  # Словарь для хранения фигур: (q, r) -> фигура
        self.setup_board()

    def display(self):
        """Отображает гексагональную доску в виде шестиугольника"""
        print("   Гексагональные шахматы (вид сверху)")
        print("      a   b   c   d   e   f   g   h   i")

        for r in range(-self.size, self.size + 1):
            # Отступ для формирования шестиугольника
            indent = abs(r) * "  "
            line = []

            for q in range(-self.size, self.size + 1):
                if self.is_valid_coord((q, r)):
                    piece = self.get_piece((q, r))
                    line.append(piece.symbol() if piece else '·')
                else:
                    line.append(' ')

            # Преобразуем координату r в номер строки
            row_num = r + self.size + 1
            print(f"{row_num:2} {indent}{'   '.join(line)} {row_num:2}")

        print("      a   b   c   d   e   f   g   h   i")

    def is_valid_coord(self, coord):
        """Проверяет валидность координат на шестиугольной доске"""
        q, r = coord
        return abs(q) <= self.size and abs(r) <= self.size and abs(q + r) <= self.size


class HexChessGame:
    """Класс для управления игрой с улучшенным интерфейсом"""

    def __init__(self):
        self.board = HexBoard()
        self.current_player = 'white'
        self.letters = 'abcdefghi'

    def parse_input(self, coord_str):
        """Преобразует буквенно-цифровые координаты в (q, r)"""
        if len(coord_str) != 2:
            return None

        col = coord_str[0].lower()
        row = coord_str[1]

        try:
            q = self.letters.index(col) - 4
            r = int(row) - 5
            return (q, r) if self.board.is_valid_coord((q, r)) else None
        except (ValueError, IndexError):
            return None

    def play(self):
        """Основной игровой цикл с улучшенным интерфейсом"""
        print("Добро пожаловать в гексагональные шахматы!")
        print("Пример хода: 'e5 d5' - перемещает фигуру с e5 на d5")

        while True:
            self.board.display()
            print(f"\nХод {'белых' if self.current_player == 'white' else 'черных'}")

            move = input("Введите ход (например 'e5 d5'): ").strip().lower().split()
            if len(move) != 2:
                print("Ошибка: нужно ввести две координаты, например 'e5 d5'")
                continue

            start = self.parse_input(move[0])
            end = self.parse_input(move[1])

            if not start or not end:
                print("Некорректные координаты! Используйте формат 'a1' до 'i9'")
                continue

            if self.board.move_piece(start, end):
                self.current_player = 'black' if self.current_player == 'white' else 'white'


# Улучшенная реализация фигур
class HexBishop(Piece):
    """Слон для гексагональных шахмат"""

    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def can_move(self, board, start, end):
        # Слон ходит по диагоналям в 3-х направлениях
        diff_q = end[0] - start[0]
        diff_r = end[1] - start[1]

        # Проверка движения по одной из диагоналей
        if (diff_q == 0 or diff_r == 0 or (diff_q + diff_r) == 0):
            step_q = 1 if diff_q > 0 else -1 if diff_q < 0 else 0
            step_r = 1 if diff_r > 0 else -1 if diff_r < 0 else 0

            # Проверка пути
            current = (start[0] + step_q, start[1] + step_r)
            while current != end:
                if board.get_piece(current) is not None:
                    return False
                current = (current[0] + step_q, current[1] + step_r)

            target = board.get_piece(end)
            return target is None or target.color != self.color

        return False


if __name__ == "__main__":
    game = HexChessGame()
    game.play()