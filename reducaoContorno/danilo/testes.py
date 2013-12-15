# -*- coding: utf-8 -*-

import unittest
# FIXME: remover capitalização após correção do módulo reducaoMorris
from reducaoMorris import Etapa1
from reducaoMorris import Etapa2

class TestUtils(unittest.TestCase):

    def test_Etapa1(self):
        self.assertEqual(Etapa1([0, 1, 2, 3], 0), [0, 3])
        self.assertEqual(Etapa1([0, 2, 1, 3], 0), [0, 2, 3])
        self.assertEqual(Etapa1([1, 0, 3, 2], 0), [1, 3, 2])
        self.assertNotEqual(Etapa1([0, 1, 0], 0), [1])

    def test_Etapa2(self):
        self.assertEqual(Etapa2([0, 1, 2, 3], 0), [0, 3])
        self.assertEqual(Etapa2([0, 2, 1, 3], 0), [0, 1, 3])
        self.assertEqual(Etapa2([1, 0, 3, 2], 0), [1, 0, 2])
        self.assertNotEqual(Etapa2([0, 1, 0], 0), [1])

if __name__ == '__main__':
    unittest.main()
