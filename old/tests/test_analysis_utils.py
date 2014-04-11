# -*- coding: utf-8 -*-

import unittest
import datetime
import analysis._utils as _utils

class TestUtils(unittest.TestCase):
    def test_date_parser(self):
        self.assertEqual(_utils.date_parser('00010101'), datetime.date(1, 1, 1))
        self.assertEqual(_utils.date_parser('19991231'), datetime.date(1999, 12, 31))
        self.assertNotEqual(_utils.date_parser('00010101'), datetime.date(1999, 12, 31))
        self.assertNotEqual(_utils.date_parser('19991231'), datetime.date(1, 1, 1))

    def test_name_parser(self):
        self.assertEqual(_utils.name_parser('Johann Sebastian Bach'), ('Johann Sebastian', 'Bach'))
        self.assertEqual(_utils.name_parser('Prename Surname'), ('Prename', 'Surname'))
        self.assertNotEqual(_utils.name_parser('Johann Sebastian Bach'), ('Johann', 'Sebastian Bach'))
        self.assertNotEqual(_utils.name_parser('Johann Sebastian Bach'), ('Johann Sebastian Bach'))

    def test_equality_comparisons(self):
        class ClassOne(object):
            pass

        class ClassTwo(object):
            pass

        class_one = ClassOne()
        class_one.arg = True

        class_two = ClassTwo()

        class_three = ClassOne()
        class_three.arg = False

        self.assertEqual(_utils.equality_comparisons(class_one, class_one), True)
        self.assertNotEqual(_utils.equality_comparisons(class_one, class_two), True)
        self.assertNotEqual(_utils.equality_comparisons(class_one, class_three), True)

if __name__ == '__main__':
    unittest.main()
