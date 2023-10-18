from unittest import TestCase

class Player():
    def __init__(self, name):
        self.name = name

    def hi(self):
        print(f"Hi, my name is {self.name}")

class HitsMatch():
    __success = []
    __NowPlayer = 0
    __NowHoll = 0
    __table = []

    def __init__(self, H, players):
        self.__HollCount = H
        self.__players = players
        self.finished = False

        for i in range(len(players)):
            self.__success.append(False)
        for i in range(H):
            self.__table.append([0] * len(players))

    def change_holl(self):
        if all(self.__success):
            if self.__NowHoll < self.__HollCount - 1:
                self.__table[self.__NowHoll] = tuple(self.__table[self.__NowHoll])

                for i in range(len(self.__players)):
                    self.__success[i] = False
                    if self.__table[self.__NowHoll][i] == 10:
                        self.__NowPlayer = i
                self.__NowHoll += 1
            else:
                self.finished = True

    def change_player(self):
        if self.__NowPlayer < len(self.__players) - 1:
            self.__NowPlayer += 1
        else:
            self.__NowPlayer = 0
        self.change_holl()

    def counter_of_hits(self, success, now_player):
        self.__table[self.__NowHoll][self.__NowPlayer] += 1
        if success or self.__table[self.__NowHoll][self.__NowPlayer] == 9:
            self.__success[self.__NowPlayer] = True
            if self.__table[self.__NowHoll][self.__NowPlayer] == 9:
                self.__table[self.__NowHoll][self.__NowPlayer] += 1

    def hit(self, success=False):
        if self.finished:
            raise RuntimeError
        else:
            now_player = self.__players[self.__NowPlayer]
            self.counter_of_hits(success, now_player)
        self.change_player()
        while self.__success[self.__NowPlayer] and not self.finished:
            self.change_player()

    def get_table(self):
        table = [tuple(elem.name for elem in self.__players)]
        table.extend(self.__table[0:self.__NowHoll])

        now_points = []
        for _ in range(self.__NowHoll, self.__HollCount):
            now_points.append([None] * len(self.__players))
        for i in range(len(self.__players)):
            if self.__success[i]:
                now_points[0][i] = self.__table[self.__NowHoll][i]

        now_points = list(map(lambda x: tuple(x), now_points))

        table.extend(now_points)
        return table

    def get_winners(self):
        if not self.finished:
            raise RuntimeError
        else:
            points = [0]*len(self.__players)
            for i in range(len(self.__players)):
                for j in range(self.__HollCount):
                    points[i] += self.__table[j][i]

            min_point = min(points)
            result = []
            for i in range(len(points)):
                if points[i] == min_point:
                    result.append(self.__players[i])
            return result

class HitsMatchTestCase(TestCase):
    def test_scenario(self):
        players = [Player('A'), Player('B'), Player('C')]
        m = HitsMatch(3, players)

        self._first_hole(m)
        self._second_hole(m)

        with self.assertRaises(RuntimeError):
            m.get_winners()

        self._third_hole(m)

        with self.assertRaises(RuntimeError):
            m.hit()

        self.assertEqual(m.get_winners(), [
            players[0], players[2]
        ])

    def _first_hole(self, m):
        m.hit()     # 1
        m.hit()     # 2
        m.hit(True) # 3
        m.hit(True) # 1
        for _ in range(8):
            m.hit() # 2

        self.assertFalse(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (None, None, None),
            (None, None, None),
        ])

    def _second_hole(self, m):
        m.hit() # 2
        for _ in range(3):
            m.hit(True) # 3, 1, 2

        self.assertFalse(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (None, None, None),
        ])

    def _third_hole(self, m):
        m.hit()     # 3
        m.hit(True) # 1
        m.hit()     # 2
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (1, None, None),
        ])
        m.hit(True) # 3
        m.hit()     # 2
        m.hit(True) # 2

        self.assertTrue(m.finished)
        self.assertEqual(m.get_table(), [
            ('A', 'B', 'C'),
            (2, 10, 1),
            (1, 2, 1),
            (1, 3, 2),
        ])

Test = HitsMatchTestCase()
Test.test_scenario()
