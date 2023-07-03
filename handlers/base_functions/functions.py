from .._init_key.key import get_i_key
from .._init_key.key import replacement_by_table
from transliterate import translit


def str_to_bin(s: str) -> str:
    '''
        Преобразование строки в двоичный вид.
    '''
    return ''.join(format(ord(symbol), '08b') for symbol in s)


def bin_to_str(s: list) -> str:
    '''
        Преобразование двоичного кода в строку.
    '''
    return ''.join([chr(i) for i in [int(b, 2) for b in s]])


def encode_input(enter: str) -> list:
    '''
        Разбиваем строку на блоки по 64 бита.
    '''
    result = []
    bin_str = str_to_bin(enter)

    if len(bin_str) % 64 != 0:
        for i in range(64 - len(bin_str) % 64):
            bin_str += '0'

    for i in range(len(bin_str) // 64):
        result.append(bin_str[i * 64:i * 64 + 64])

    return result


def decode_input(enter: str) -> list:
    '''
        Разбиваем зашифрованный текст на зашифрованные блоки. (Разделитель '0x')
    '''
    result = []
    input_list = enter.split("0x")[1:]

    int_list = [int("0x" + i, 16) for i in input_list]
    for i in int_list:
        bin_data = str(bin(i))[2:]
        while len(bin_data) < 64:
            bin_data = '0' + bin_data
        result.append(bin_data)

    return result


def replace_block_IP(block: str) -> str:
    '''
        Начальная перестановка IP.
    '''
    IP_table = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    )

    return replacement_by_table(block, IP_table)


def my_xor(str1: str, str2: str) -> str:
    '''
        XOR.
    '''
    result = ''
    for i in range(len(str1)):
        result += '0' if str1[i] == str2[i] else '1'

    return result


def block_extend(block: str) -> str:
    '''
        Функция расширения.
    '''
    extend_table = (
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    )

    return replacement_by_table(block, extend_table)


def S_box_replace(block: str) -> str:
    '''
        Преобразование S, состоящие из 8 преобразований S-блоков S1,S2,S3...S8.
    '''
    s_box_table = (
        (
            (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
            (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
            (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
            (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13),
        ),
        (
            (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
            (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
            (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
            (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9),
        ),
        (
            (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
            (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
            (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
            (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12),
        ),
        (
            (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14),
        ),
        (
            (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3),
        ),
        (
            (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
            (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
            (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
            (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13),
        ),
        (
            (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12),
        ),
        (
            (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
            (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
            (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
            (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11),
        )
    )

    result = ''
    for i in range(8):
        line_bit = block[i*6] + block[i*6 + 5]
        column_bit = block[i*6 + 1:i*6 + 5]
        line = int(line_bit, 2)
        column = int(column_bit, 2)
        value = s_box_table[i][line][column]
        value = str(bin(value))[2:]
        while len(value) < 4:
            value = '0' + value
        result += value

    return result


def permutation_P(block: str):
    '''
        Перестановка P.
    '''
    P_table = (
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    )

    return replacement_by_table(block, P_table)


def replace_block_reverse_IP(block: str) -> str:
    '''
        Конечная перестановка IP^-1
    '''
    reverse_IP_table = (
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
    )

    return replacement_by_table(block, reverse_IP_table)


def feistel_function(right: str, key: str, i: int) -> str:
    '''
        Функция Фейстеля.
    '''
    i_key = get_i_key(key, i)

    right = block_extend(right)
    my_xor_result = my_xor(right, i_key)
    s_box_result = S_box_replace(my_xor_result)
    result = permutation_P(s_box_result)

    return result


def encryption_decryption_cycle(block: str, key: str, is_decode: bool) -> str:
    '''
        Цикл шифрования(расшифрования) для одного блока.
    '''
    if is_decode:
        for i in range(15, -1, -1):
            left, right = block[0:32], block[32:64]
            next_left = right
            feistel_result = feistel_function(right, key, i)
            next_right = my_xor(left, feistel_result)
            block = next_right + next_left
    else:
        for i in range(16):
            left, right = block[:32], block[32:]
            next_left = right
            feistel_result = feistel_function(right, key, i)
            next_right = my_xor(left, feistel_result)
            block = next_right + next_left

    return block


def find_indexes(string: str) -> list:
    '''
        Поиск индексов кириллицы, если они есть и сохранение в список.
    '''
    result = []
    ru_alph = 'абвгдежзийклмнопрстуфхцчшщъыьэю'
    i = 0
    for symbol in string:
        if symbol.lower() in ru_alph:
            result.append(i)
        i += 1

    return result


def selective_transliteration(string: str, rep_idx: list, is_decode: bool) -> str:
    '''
        Посимвольная транслитерация символов кириллицы по списку индексов.
    '''
    result = ''
    i = 0
    for symbol in string:
        if i in rep_idx:
            if is_decode:
                result += translit(symbol, 'ru')
            else:
                result += translit(symbol, language_code='ru', reversed=True)
        else:
            result += symbol
        i += 1

    return result


def encode(string: str, key: str, rep_idx: list) -> str:
    '''
        Функция шифрования.
    '''
    string = selective_transliteration(string, rep_idx, False)

    encode_result = ''
    blocks = encode_input(string)

    for block in blocks:
        result_IP_permutation = replace_block_IP(block)
        block_result = encryption_decryption_cycle(result_IP_permutation,
                                                   key, False)
        block_result = replace_block_reverse_IP(block_result)
        encode_result += str(hex(int(block_result.encode(), 2)))

    return encode_result


def decode(string: str, key: str, rep_idx: list) -> str:
    '''
        Функция расшифрования.
    '''
    decode_result = []
    blocks = decode_input(string)

    for block in blocks:
        result_IP_permutation = replace_block_IP(block)
        block_result = encryption_decryption_cycle(result_IP_permutation,
                                                   key, True)
        block_result = replace_block_reverse_IP(block_result)
        for i in range(0, len(block_result), 8):
            decode_result.append(block_result[i:i+8])

    decode_result = bin_to_str(decode_result)

    return selective_transliteration(decode_result, rep_idx, True)
