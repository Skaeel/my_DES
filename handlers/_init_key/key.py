import random


def replacement_by_table(block: str, table: tuple) -> str:
    '''
        Замена блока по таблице.
    '''
    result = ''
    for i in table:
        result += block[i - 1]

    return result


def key_generation() -> str:
    '''
        Генерация 56 битного ключа в бинарном виде.
        Каждый символ по 7 бит
    '''
    key = ''
    for i in range(8):
        for j in range(7):
            rand_bit = random.randint(0, 1)
            if rand_bit == 0:
                key += str(rand_bit)
            else:
                key += str(rand_bit)
        if i != 7:
            key += ' '

    return key


def add_bit(key: str) -> str:
    '''
        Добавляем биты чётности и получаем изначальный 64 битный ключ.
        Каждый символ по 8 бит.
        Биты четности при перестановке по таблице CD не учитываются.
    '''
    # Проверка ключа на правильность(если вводят руками)
    spaces = 0
    ones_zeros = 0
    for i in key:
        if i == ' ':
            spaces += 1
        elif i == '1' or i == '0':
            ones_zeros += 1
    if len(key) != 63:
        return False
    elif spaces != 7:
        return False
    elif ones_zeros != 56:
        return False

    key_symbols_list = key.split(' ')
    add_bits_list = []
    for symbol in key_symbols_list:
        ones = 0
        for bit in symbol:
            if bit == '1':
                ones += 1
        if ones % 2 == 0:
            add_bits_list.append(symbol + '1')
        else:
            add_bits_list.append(symbol + '0')
        ones = 0

    key_string = ''
    for symbol in add_bits_list:
        key_string += symbol

    return key_string


def CD_permutation(key: str) -> str:
    '''
        Перестановка ключа по таблице CD.
    '''
    key = add_bit(key)
    if key == False:
        print('ERROR: Key input is incorrect.')
        exit()

    first_key = key[:64]

    CD_table = (
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
    )

    return replacement_by_table(first_key, CD_table)


def left_shift(block: str, number_of_shifts: int) -> str:
    '''
        Циклический сдвиг влево.
    '''
    for i in range(number_of_shifts):
        block = block[1:] + block[0]

    return block


def i_shift_CD_block(key: str, i: int) -> str:
    '''
        Смещаем C блок и D блок по отдельности, с помощью циклического сдвига.
    '''
    CD_block = CD_permutation(key)

    shift_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)

    number_shifts = shift_table[i]
    C_block, D_block = CD_block[:28], CD_block[28:]
    shifted_C_block = left_shift(C_block, number_shifts)
    shifted_D_block = left_shift(D_block, number_shifts)

    return shifted_C_block + shifted_D_block


def get_i_key(key: str, i: int) -> str:
    '''
        Получаем ключ для текущей итерации(1-16).
        С помощью конечной перестановки ключа.
    '''
    CD_block = i_shift_CD_block(key, i)

    get_i_key_table = (
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
    )

    return replacement_by_table(CD_block, get_i_key_table)
