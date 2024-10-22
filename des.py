import os
import json
import multiprocessing
import string
import time
import sys
import math
import random
begin_replace_table = (
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17,  9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
)
end_replace_table = (
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
)
key_replace_table = (
    57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
)
key_select_table = (
    14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
)
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
p_box_replace_table = (
    16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25,
)
spin_table = (1, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 28)
def crypt(mode, data_in_, number_of_blocks, kkey, queues):
    line_good = ''
    counter = 0
    for g in range(number_of_blocks):
        line_in_bad = ''
        #получение 64-битовых блоков
        for elem in data_in_[g*8:(g+1)*8]:
            byte = bin(elem)[2:]
            while len(byte)<8:
                byte = '0'+byte
            line_in_bad += byte
        line_in_good = ''
        #начальная перестановка
        for i in range(64):
            line_in_good += line_in_bad[begin_replace_table[i]-1]
        if mode == 2:
            r_next = line_in_good[:32]
            l_next = line_in_good[32:]
        else:
            l_next = line_in_good[:32]
            r_next = line_in_good[32:]
        #16 раундов сети Фейстеля
        for i in range(1,17):
            l_current = l_next
            l_next = r_next
            #функция f
            r_next = bin(int(l_current,2)^int(f(r_next,kkey[i]),2))[2:]
            while len(r_next)<32:
                r_next = '0'+r_next
        if mode == 2:
            line_out = r_next+l_next
        else:
            line_out = l_next+r_next
        #конечная перестановка
        for i in range(64):
            line_good += line_out[end_replace_table[i]-1]
        #заполнение очередей
        if g == number_of_blocks - 1 or g % 125 == 0 and g > 0:
            queues[counter].put([chr(int(line_good[8*i:8*(i+1)],2)).encode('charmap') for i in range(len(line_good)//8)])
            counter += 1
            line_good = ''
def f(data_in, _key):
    b = ['']*8
    data_out = ''
    #расширение 32-битовой половины блока до 48 бит
    for i in range(48):
        data_out += data_in[extend_table[i]-1]
    #XOR данных и ключа
    data_in = bin(int(data_out,2)^int(_key,2))[2:]
    while len(data_in)<48:
        data_in = '0'+data_in
    #разбиение 48-битовой последовательности на 8 частей по 6 бит
    for i in range(8):
        b[i] = data_in[i*6:(i+1)*6]
    data_in = ''
    #применене S-преобразования
    for i in range(8):
        data_out = bin(s_box_table[i][int(b[i][0]+b[i][5],2)][int((b[i][1:5]),2)])[2:]
        while len(data_out)<6:
            data_out = '0'+data_out
        data_in += data_out
    # P-перестановка
    data_out = ''
    for i in range(32):
        data_out += data_in[p_box_replace_table[i]-1]
    return data_out
def crypt_data(data, data_size):
    global mode
    global k
    global cpu_count
    # Обработка отдельными процессами своих блоков
    blocks_count = math.ceil(data_size / 8)
    blocks_count_per_process = (blocks_count - 1) // cpu_count
    processes = []
    queues = []
    i = 0
    if blocks_count_per_process:
        for i in range(cpu_count):
            #запуск процессов
            queues.append([multiprocessing.Queue() for s in range(math.ceil(blocks_count_per_process / 125))])
            processes.append(multiprocessing.Process(target=crypt, args=(mode, data[8*blocks_count_per_process*i:8*blocks_count_per_process*(i+1)], blocks_count_per_process, k.copy(), queues[i])))
            processes[i].start()
    # работа с последними блоками в основном процессе
    blocks_left = blocks_count - blocks_count_per_process * cpu_count
    line_for_input = data[8*blocks_count_per_process*(i+1):]
    if mode == 1 and data_size % 8 != 0:
        for i in range(8 - data_size % 8):
            line_for_input = line_for_input[:len(line_for_input)//8*8]+b'\x14'+line_for_input[len(line_for_input)//8*8:]
    #ожидание завершения процессов
    if blocks_count_per_process:
        for i in range(cpu_count):
            processes[i].join()
    queues.append([multiprocessing.Queue() for s in range(math.ceil(blocks_left / 125))])
    crypt(mode, line_for_input, blocks_left, k, queues[-1])
    #обработка полученных очередей
    cyphers = [[] for i in range(cpu_count+1 if blocks_count_per_process else 1)]
    for i in range(cpu_count+1 if blocks_count_per_process else 1):
        for j in range(len(queues[i])):
            cyphers[i].extend(queues[i][j].get())
    ctr = 0
    #обработка последнего блока
    if mode == 2:
        while cyphers[-1][ctr-8] == b'\x14':
            cyphers[-1] = cyphers[-1][:ctr-8]+cyphers[-1][ctr-7:]
            ctr += 1
    return [_symbol for _cypher in cyphers for _symbol in _cypher]
def build_next_level(dictionary, path):
    directories = dictionary['dirs'].copy()
    dictionary['files'] = [{'name': file, 'size': os.stat(os.path.join(path, file)).st_size} for file in dictionary['files']]
    dictionary['dirs'] = [{'name': _dir, 'files': [file for file in os.listdir(os.path.join(path, _dir)) if os.path.isfile(os.path.join(path, _dir, file))], 'dirs': [dire for dire in os.listdir(os.path.join(path, _dir)) if os.path.isdir(os.path.join(path, _dir, dire))]} for _dir in directories]
    for i in range(len(directories)):
        build_next_level(dictionary['dirs'][i], 
            os.path.join(path, directories[i]))
def crypt_next_level(dictionary, path, _f_):
    for file in dictionary['files']:
        if file['size']:
            with open(os.path.join(path,file['name']), 'rb') as f_cur:
                for c in crypt_data(f_cur.read(),file['size']):
                    _f_.write(c)
    for dire in dictionary['dirs']:
        crypt_next_level(dire, os.path.join(path, dire['name']), _f_)
def scan_next_level(dictionary, path, _f_):
    for file in dictionary['files']:
        if file['size'] == 0:
            open(os.path.join(path, file['name']), 'w').close()
        else:
            with open(os.path.join(path, file['name']), 'wb') as f_out:
                for c in crypt_data(_f_.read(8*math.ceil(file['size']/8)), file['size']):
                    f_out.write(c)
    for dire in dictionary['dirs']:
        dir_path = os.path.join(path, dire['name'])
        os.mkdir(dir_path)
        scan_next_level(dire, dir_path, _f_)
key = ''
k = ['']*17
c = ['']*17
d = ['']*17
cd = ['']*17
byte = ''
k[0] = '0'
mode = 0
cpu_count = os.cpu_count()
if __name__ == '__main__':
    start_time = time.time()
    key_ = sys.argv[1]
    mode = int(sys.argv[2])
        # получение 56-битного ключа
    for i in range(len(key_)):
        byte = bin(ord(key_[i]))[2:]
        while len(byte)<8:
            byte = '0'+byte
        key += byte
    while len(key)%56 != 0:
        key += '00000000'
    for i in range(len(key)//56):
        k[0] = bin(int(k[0],2)^int(key[56*i:56*(i+1)],2))[2:]
    while len(k[0])<56:
        k[0] = '0'+k[0]
    # расширение ключа до 64 бит
    for i in range(8):
        count = 0
        for j in range(7):
            if k[0][j+8*i] == '1':
                count += 1
        if count % 2 == 1:
            k[0] = k[0][:7+8*i] + '0' + k[0][7+i*8:]
        else:
            k[0] = k[0][:7+8*i] + '1' + k[0][7+i*8:]
    # получение c и d блоков из 64-битного ключа
    for i in range(28):
        c[0] += k[0][key_replace_table[i] - 1]
        d[0] += k[0][key_replace_table[i + 28] - 1]
    # получение 16-ти c и d вариаций
    for i in range(16):
        c[i + 1] = c[0][spin_table[i]:] + c[0][:spin_table[i]]
        d[i + 1] = d[0][spin_table[i]:] + d[0][:spin_table[i]]
    # получение 16-ти 48-битных подключей
    for i in range(1,17):
        cd[i] = c[i] + d[i]
        for j in range(48):
            k[i] += cd[i][key_select_table[j]-1]
    # обработка файлов
    if mode == 1:
        data = {'files' : [sys.argv[i] for i in range(3,len(sys.argv)) if os.path.isfile(sys.argv[i])], 'dirs' : [sys.argv[i] for i in range(4,len(sys.argv)) if os.path.isdir(sys.argv[i])]}
        build_next_level(data, os.getcwd())
        #создание json файла для хранения информации о файлах
        with open('data.json', 'w') as file:
            json.dump(data, file)
        json_size = os.stat('data.json').st_size
        with open("TOP_SECRET.lol",'wb') as f2:
            for c in crypt_data(bytes(str(json_size).encode('charmap')), len(str(json_size))):
                f2.write(c)
            with open('data.json', 'rb') as file:
                for c in crypt_data(file.read(), json_size):
                    f2.write(c)
            crypt_next_level(data, os.getcwd(), f2)
        # дополнение до нужной длины
        with open("TOP_SECRET.lol", 'a') as f2:
            size = os.stat("TOP_SECRET.lol").st_size
            if size < int(sys.argv[3]):
                f2.write(''.join(random.choices(string.printable, k=int(sys.argv[3])-size)))
    else:
        k[1],k[2],k[3],k[4],k[5],k[6],k[7],k[8],k[9],k[10],k[11],k[12],k[13],k[14],k[15],k[16] = (
        k[16],k[15],k[14],k[13],k[12],k[11],k[10],k[9],k[8],k[7],k[6],k[5],k[4],k[3],k[2],k[1])
        with open(sys.argv[3], 'rb') as f_in:
            #извлечение json файла для использования в качестве словаря
            json_size = int(b''.join(crypt_data(f_in.read(8), 8)), 10)
            with open('data.json', 'wb') as file:
                for c in crypt_data(f_in.read(8*math.ceil(json_size/8)), json_size):
                    file.write(c)
            with open('data.json') as file:
                data = json.load(file)
            #поуровневое расшифрование файлов
            scan_next_level(data, os.getcwd(), f_in)
    #удаление временных файлов и вывод времени работы программы
    os.remove('data.json')
    print('прошедшее время: ', time.time() - start_time)