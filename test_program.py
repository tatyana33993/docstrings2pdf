#!/usr/bin/env python34
import unittest
import docstrings as d


class Testdocstrings(unittest.TestCase):
    def test_get_docstrings_none(self):
        result = d.get_docstrings('example.txt')
        self.assertIsNotNone(result)

    def test_get_docstrings_class_with_comments(self):
        result = d.get_docstrings('example.txt')
        s = set()
        for key in result.keys():
            if key[:key.find('.')] != '' and key[key.find('.') + 1:] == '':
                s.add(key[:key.find('.')])
        self.assertTrue(len(s) == 2)

    def test_get_docstrings_def_with_comments(self):
        result = d.get_docstrings('example.txt')
        s = []
        for key in result.keys():
            if key[:key.find('.')] == '' and key[key.find('.')+1:] != '':
                s.append(key[key.find('.')+1:])
        self.assertTrue(len(s) == 4)

    def test_get_docstrings_class_def_with_comments(self):
        result = d.get_docstrings('example.txt')
        s = []
        for key in result.keys():
            if key[:key.find('.')] != '' and key[key.find('.')+1:] != '':
                s.append(key[key.find('.')+1:])
        self.assertTrue(len(s) == 6)

    def test_get_docstrings_module_with_comments(self):
        result = d.get_docstrings('example.txt')
        s = []
        for key in result.keys():
            if key[:key.find('.')] == '' and key[key.find('.')+1:] == '':
                s.append('.')
        self.assertTrue(len(s) == 1)

    def test_get_current_class_first(self):
        res = d.get_current_class('class Game:', '', '')
        self.assertEqual(res[0], 'Game')
        self.assertEqual(res[1], '')

    def test_get_current_class_second(self):
        res = d.get_current_class('class Player:', 'Game', 'get_move')
        self.assertEqual(res[0], 'Player')
        self.assertEqual(res[1], '')

    def test_get_current_def_first(self):
        res = d.get_current_def('def get_move():', '')
        self.assertEqual(res, 'get_move')

    def test_get_current_def_second(self):
        res = d.get_current_def('def get_score():', 'get_move')
        self.assertEqual(res, 'get_score')

    def test_get_current_comm_start_comm(self):
        comm, current_comm, dic = d.get_current_comm('"""', 'Game',
                                                     'get_score',
                                                     False, '', {})
        self.assertTrue(comm)
        self.assertEqual(current_comm, '')
        self.assertEqual(dic, {})

    def test_get_current_comm_comm(self):
        comm, current_comm, dic = d.get_current_comm('Count score of'
                                                     ' Game Reversi',
                                                     'Game', 'get_score',
                                                     True, '', {})
        self.assertTrue(comm)
        self.assertEqual(current_comm, 'Count score of Game Reversi')
        self.assertEqual(dic, {})

    def test_get_current_comm_end_comm(self):
        comm, current_comm, dic = d.get_current_comm('"""', 'Game',
                                                     'get_score',
                                                     True,
                                                     'Count score of'
                                                     ' Game Reversi', {})
        self.assertFalse(comm)
        self.assertEqual(current_comm, '')
        self.assertEqual(dic, {'Game.get_score':
                               ''"""Count score of Game Reversi"""''})

    def test_get_current_comm_pass(self):
        comm, current_comm, dic = d.get_current_comm('a = b + 5', 'Game',
                                                     'get_score',
                                                     False, '',
                                                     {'Game.get_score':
                                                      '"""Count score of '
                                                      'Game Reversi"""'})
        self.assertFalse(comm)
        self.assertEqual(current_comm, '')
        self.assertEqual(dic, {'Game.get_score':
                               '"""Count score of Game Reversi"""'})


if __name__ == '__main__':
    unittest.main()
