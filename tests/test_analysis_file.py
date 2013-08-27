# -*- coding: utf-8 -*-

import unittest
import analysis.file as file


class TestUtils(unittest.TestCase):
    def test_idCodeParser(self):
        codes = ['EF00001',
                 'EF00001-Telemann 12 Fantasias',
                 'ET00001_01a',
                 'ET00001_03d',
                 'ET00001_01bE',
                 'ET00001_12aE']
        answers = [
            {'sourceOrigin': 'E', 'sourceType': 'F', 'sourceId': '00001', 'sourceExpansion': False},
            {'sourceOrigin': 'E', 'sourceType': 'F', 'sourceId': '00001', 'sourceExpansion': False, 'sourceSuffix': 'Telemann 12 Fantasias'},
            {'sourceOrigin': 'E', 'sourceType': 'T', 'sourceId': '00001', 'sourceSongNumber': '01', 'sourceMovement': 'a', 'sourceExpansion': False},
            {'sourceOrigin': 'E', 'sourceType': 'T', 'sourceId': '00001', 'sourceSongNumber': '03', 'sourceMovement': 'd', 'sourceExpansion': False},
            {'sourceOrigin': 'E', 'sourceType': 'T', 'sourceId': '00001', 'sourceSongNumber': '01', 'sourceMovement': 'b', 'sourceExpansion': True},
            {'sourceOrigin': 'E', 'sourceType': 'T', 'sourceId': '00001', 'sourceSongNumber': '12', 'sourceMovement': 'a', 'sourceExpansion': True}
            ]
        self.assertEqual(file.idCodeParser(codes[0]), answers[0])
        self.assertEqual(file.idCodeParser(codes[1]), answers[1])
        self.assertEqual(file.idCodeParser(codes[2]), answers[2])
        self.assertEqual(file.idCodeParser(codes[3]), answers[3])
        self.assertEqual(file.idCodeParser(codes[4]), answers[4])
        self.assertEqual(file.idCodeParser(codes[5]), answers[5])

    def test_idCodeMaker(self):
        self.assertEqual(file.idCodeMaker('E', 'T', '00001', '23', 'a', True, 'Foobar'), 'ET00001_23aE-Foobar')
