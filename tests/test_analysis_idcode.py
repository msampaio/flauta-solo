# -*- coding: utf-8 -*-

import unittest
import analysis.idcode as idcode


class TestUtils(unittest.TestCase):
    def test_id_code_parser(self):
        codes = ['EF00001',
                 'EF00001-Telemann 12 Fantasias',
                 'ET00001_01a',
                 'ET00001_03d',
                 'ET00001_01bE',
                 'ET00001_12aE']
        answers = [
            {'source_origin': 'E', 'source_type': 'F', 'source_id': '00001', 'source_expansion': False},
            {'source_origin': 'E', 'source_type': 'F', 'source_id': '00001', 'source_expansion': False, 'source_suffix': 'Telemann 12 Fantasias'},
            {'source_origin': 'E', 'source_type': 'T', 'source_id': '00001', 'source_song_number': '01', 'source_movement': 'a', 'source_expansion': False},
            {'source_origin': 'E', 'source_type': 'T', 'source_id': '00001', 'source_song_number': '03', 'source_movement': 'd', 'source_expansion': False},
            {'source_origin': 'E', 'source_type': 'T', 'source_id': '00001', 'source_song_number': '01', 'source_movement': 'b', 'source_expansion': True},
            {'source_origin': 'E', 'source_type': 'T', 'source_id': '00001', 'source_song_number': '12', 'source_movement': 'a', 'source_expansion': True}
            ]
        self.assertEqual(idcode.id_code_parser(codes[0]), answers[0])
        self.assertEqual(idcode.id_code_parser(codes[1]), answers[1])
        self.assertEqual(idcode.id_code_parser(codes[2]), answers[2])
        self.assertEqual(idcode.id_code_parser(codes[3]), answers[3])
        self.assertEqual(idcode.id_code_parser(codes[4]), answers[4])
        self.assertEqual(idcode.id_code_parser(codes[5]), answers[5])

    def test_id_code_maker(self):
        self.assertEqual(idcode.id_code_maker('E', 'T', '00001', '23', 'a', True, 'Foobar'), 'ET00001_23aE-Foobar')
