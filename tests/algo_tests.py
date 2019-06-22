import unittest

from cstechnion.algo.algo import *


class AlgoTests(unittest.TestCase):
    @staticmethod
    def test_huffman():
        assert huffman([('A', 8), ('B', 4), ('C', 2), ('D', 1)]) == [('A', '0'), ('B', '10'), ('C', '110'),
                                                                     ('D', '111')]
        assert huffman([('A', 4), ('B', 2), ('C', 1), ('D', 1)]) == [('D', '000'), ('C', '001'), ('B', '01'),
                                                                     ('A', '1')]
        assert huffman([('A', 1), ('B', 2), ('C', 3), ('D', 2)]) == [('C', '00'), ('B', '01'), ('D', '10'), ('A', '11')]

        text = 'Hi you guys!\nMy name is Tom.\n:)'
        hist = get_char_hist(text)
        huff_code = huffman(hist)
        assert huff_code == [(' ', '000'), ('o', '0010'), ('g', '00110'), ('e', '00111'), (')', '01000'),
                             ('M', '01001'), (':', '01010'), ('n', '01011'), ('T', '01100'), ('!', '01101'),
                             ('a', '01110'), ('H', '01111'), ('\n', '1000'), ('i', '1001'), ('u', '1010'),
                             ('s', '1011'), ('y', '110'), ('m', '1110'), ('.', '1111')]
        enc_text = huffman_encode(text, huff_code)
        dec_text = huffman_decode(enc_text, huff_code)
        assert text == dec_text


if __name__ == '__main__':
    unittest.main()
