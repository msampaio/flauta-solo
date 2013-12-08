# -*- coding: utf-8 -*-

import unittest
import datetime
import analysis._utils as _utils

class TestUtils(unittest.TestCase):
    def test_dateParser(self):
        self.assertEqual(_utils.dateParser('00010101'), datetime.date(1, 1, 1))
        self.assertEqual(_utils.dateParser('19991231'), datetime.date(1999, 12, 31))
        self.assertNotEqual(_utils.dateParser('00010101'), datetime.date(1999, 12, 31))
        self.assertNotEqual(_utils.dateParser('19991231'), datetime.date(1, 1, 1))

    def test_nameParser(self):
        self.assertEqual(_utils.nameParser('Johann Sebastian Bach'), ('Johann Sebastian', 'Bach'))
        self.assertEqual(_utils.nameParser('Prename Surname'), ('Prename', 'Surname'))
        self.assertNotEqual(_utils.nameParser('Johann Sebastian Bach'), ('Johann', 'Sebastian Bach'))
        self.assertNotEqual(_utils.nameParser('Johann Sebastian Bach'), ('Johann Sebastian Bach'))

    def test_equalityComparisons(self):
        class ClassOne(object):
            pass

        class ClassTwo(object):
            pass

        classOne = ClassOne()
        classOne.arg = True

        classTwo = ClassTwo()

        classThree = ClassOne()
        classThree.arg = False

        self.assertEqual(_utils.equalityComparisons(classOne, classOne), True)
        self.assertNotEqual(_utils.equalityComparisons(classOne, classTwo), True)
        self.assertNotEqual(_utils.equalityComparisons(classOne, classThree), True)

if __name__ == '__main__':
    unittest.main()
