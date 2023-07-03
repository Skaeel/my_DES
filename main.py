from handlers.base_functions.functions import encode
from handlers.base_functions.functions import decode
from handlers.base_functions.functions import find_indexes
from handlers._init_key.key import key_generation


def key_usage():
    print('!!! KEY_USAGE:')
    print('- The key must only consist of 1 and 0')
    print('- The key consists of 8 blocks of 7 bits')
    print('- Each block is separated from the other by a space character.')


def menu():
    print(10*'=' + ' DES encryption decryption by Dmitriy Alimov ' + '='*10)
    print('1) Auto encrypt by random key')
    print('2) Encrypt with your key')
    print('3) Decrypt')
    print('4) Auto encrypt decrypt')


def user_choice():
    menu()
    choice = input('Your choice -->> ')

    while choice != 'exit':
        if choice == '1':
            string = input('Enter your string: ')
            key = key_generation()
            replacement_idx = find_indexes(string)
            print(f'RESULT: {encode(string, key, replacement_idx)}')

        elif choice == '2':
            string = input(('Enter yout string: '))
            key_usage()
            key = input('Enter your key:')
            replacement_idx = find_indexes(string)
            print(f'RESULT: {encode(string, key, replacement_idx)}')

        elif choice == '3':
            string = input('Enter your encrypted string:')
            key_usage()
            key = input('Enter your key:')
            replacement_idx = find_indexes(string)
            print(f'RESULT: {decode(string, key, replacement_idx)}')

        elif choice == '4':
            string = input('Enter your string:')
            key = key_generation()
            replacement_idx = find_indexes(string)
            encode_string = encode(string, key, replacement_idx)
            decode_string = decode(encode_string, key, replacement_idx)
            print(f'Encode RESULT: {encode_string}')
            print(f'Decode RESULT: {decode_string}')

        else:
            print('ERROR: Incorrect input.')

        print(10*'=' + ' "exit" to finish the program ' + '='*10 + '\n\n')
        menu()
        choice = input('Your choice -->> ')


def main():
    user_choice()


if __name__ == '__main__':
    main()
