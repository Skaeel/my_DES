from handlers._init_key.key import *
from handlers.base_functions.functions import *


class TestClass:
    def test1_basic_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = 'Hello, world!'
        replacement_idx = find_indexes(string)
        true_encode_string = '0x4831786d6f7920670x2a263c6135104000'
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test1_basic_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        encode_string = '0x4831786d6f7920670x2a263c6135104000'
        replacement_idx = find_indexes('Hello, world!')
        true_decode_string = 'Hello, world!'
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string

    def test2_incorrect_key_ascii(self):
        key = 'hahahah'
        assert add_bit(key) == False

    def test3_incorrect_key_spaces(self):
        key = '11011001010101100011000010000111000011010001000001010011'
        assert add_bit(key) == False

    def test4_incorrect_key_ones_zeros(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100002 1010011'
        assert add_bit(key) == False

    def test5_russian_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = 'Привет, мир!'
        replacement_idx = find_indexes(string)
        true_encode_string = '0x51666d7265252c300x3c3d226410054050'
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test5_russian_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        encode_string = '0x51666d7265252c300x3c3d226410054050'
        replacement_idx = find_indexes('Привет, мир!')
        true_decode_string = 'Привет, мир!'
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string

    def test6_two_lang_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = 'Привет, world!'
        replacement_idx = find_indexes(string)
        true_encode_string = '0x51666d7265252c300x262b322970314000'
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test6_two_lang_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        encode_string = '0x51666d7265252c300x262b322970314000'
        replacement_idx = find_indexes('Привет, world!')
        true_decode_string = 'Привет, world!'
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string

    def test7_empty_string_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = ''
        replacement_idx = find_indexes(string)
        true_encode_string = ''
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test7_empty_string_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        encode_string = ''
        replacement_idx = find_indexes('')
        true_decode_string = ''
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string

    def test8_one_symbol_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = ' '
        replacement_idx = find_indexes(string)
        true_encode_string = '0x7154500054054150'
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test8_one_symbol_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        encode_string = '0x7154500054054150'
        replacement_idx = find_indexes(' ')
        true_decode_string = ' '
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string

    def test9_more_spec_symbols_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = '''~!@#$%^&*()_+=-[];',./{}:"<>?'''
        replacement_idx = find_indexes(string)
        true_encode_string = '0x7f65002224305f270x2f3c685a2f7c6d1b0x1d7f236d'\
                            '2a3a6a2d0x3e36683f6b144000'
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test9_more_spec_symbols_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        encode_string = '0x7f65002224305f270x2f3c685a2f7c6d1b0x1d7f236d2a3a6a'\
                        '2d0x3e36683f6b144000'
        replacement_idx = find_indexes('''~!@#$%^&*()_+=-[];',./{}:"<>?''')
        true_decode_string = '''~!@#$%^&*()_+=-[];',./{}:"<>?'''
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string

    def test10_too_long_string_encode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        string = ''
        for i in range(100000):
            string += 'tensymbols'
        replacement_idx = find_indexes(string)
        with open('too_long_string.txt', 'r') as file:
            true_encode_string = file.read()
        encode_string = encode(string, key, replacement_idx)
        assert encode_string == true_encode_string

    def test10_too_long_string_decode(self):
        key = '1101100 1010101 1000110 0001000 0111000 0110100 0100000 1010011'
        with open('too_long_string.txt', 'r') as file:
            encode_string = file.read()
        true_decode_string = ''
        for i in range(100000):
            true_decode_string += 'tensymbols'
        replacement_idx = find_indexes(true_decode_string)
        decode_string = decode(encode_string, key, replacement_idx)
        assert decode_string.replace('\x00', '') == true_decode_string
        