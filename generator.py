import solver as sv

# print(sv.solve(cubestring="UUFUUFUUFRRRRRRRRRFFDFFDFFDDDBDDBDDBLLLLLLLLLBBUBBUBBU"))
import random


# cc = sv.cubie.CubieCube()
# cc.randomize()
# fc = cc.to_facelet_cube()
# fl = fc.to_string()

# print(fl)

# cg =  "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
# cg2 = "UUUUUUUUURRRRRRFFFFFFFFFLLLDDDDDDDDDLLLLLLBBBBBBBBBRRR"

# for i in range(len(cg)):
#     print(f"Было: {cg[i]}, Стало: {cg2[i]}, Индекс: {i}")

# Исходная строка
source_string = "1 2 21 4 5 24 7 8 27 16 13 10 17 14 11 18 15 12 19 20 30 22 23 33 25 26 36 28 29 52 31 32 49 34 35 46 37 38 39 40 41 42 43 44 45 9 47 48 6 50 51 3 53 54"

# # Разбиваем строку на массив (список)
# array = source_string.split(" ")
# string = ''
# for i in array:
#     if int(i) >=1 and int(i) <= 9:
#         string += 'U'
#     if int(i) >=10 and int(i) <= 18:
#         string += 'R'
#     if int(i) >=19 and int(i) <= 27:
#         string += 'F'
#     if int(i) >=28 and int(i) <= 36:
#         string += 'D'
#     if int(i) >=37 and int(i) <= 45:
#         string += 'L'
#     if int(i) >=46 and int(i) <= 54:
#         string += 'B'

# # Выводим массив
# print(string==cg2)


# start_string = 'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
# array = []
# end_string = ''
# def transform():
#     for i in range(54):
#         array.append(i)
#     return array
# array = transform()
# print(array)
# for i in range(len(array)):
#     array[i] = int(array[i]) - 1

# # print(array)
# transform_array_1 = [0, 1, 20, 3, 4, 23, 6, 7, 26, 15, 12, 9, 16, 13, 10, 17, 14, 11, 18, 19, 29, 21, 22, 32, 24, 25, 35, 27, 28, 51, 30, 31, 48, 33, 34, 45, 36, 37, 38, 39, 40, 41, 42, 43, 44, 8, 46, 47, 5, 49, 50, 2, 52, 53]
# transform_array_2 = [0, 1, 2, 3, 4, 5, 44, 41, 38, 6, 10, 11, 7, 13, 14, 8, 16, 17, 24, 21, 18, 25, 22, 19, 26, 23, 20, 15, 12, 9, 30, 31, 32, 33, 34, 35, 36, 37, 27, 39, 40, 28, 42, 43, 29, 45, 46, 47, 48, 49, 50, 51, 52, 53]
# start_array = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
# array_1 = []
# array_2 = []
# for i in range(54):
#     array_1.append(start_array[transform_array_1[i]])

# for i in range(54):
#     array_2.append(array_1[transform_array_2[i]] + 1)
# print(array_2)

class GenerateString:
    def __init__(self):
        self.r0_dict = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]
        self.R1_dict = [0, 1, 20, 3, 4, 23, 6, 7, 26, 15, 12, 9, 16, 13, 10, 17, 14, 11, 18, 19, 29, 21, 22, 32, 24, 25, 35, 27, 28, 51, 30, 31, 48, 33, 34, 45, 36, 37, 38, 39, 40, 41, 42, 43, 44, 8, 46, 47, 5, 49, 50, 2, 52, 53]
        self.L1_dict = [53, 1, 2, 50, 4, 5, 47, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 0, 19, 20, 3, 22, 23, 6, 25, 26, 18, 28, 29, 21, 30, 32, 24, 34, 35, 42, 39, 36, 43, 40, 37, 44, 41, 38, 45, 46, 33, 48, 49, 30, 51, 52, 27]
        self.B1_dict = [11, 14, 17, 3, 4, 5, 6, 7, 8, 9, 10, 35, 12, 13, 34, 15, 16, 33, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 36, 39, 42, 2, 37, 38, 1, 40, 41, 0, 43, 44, 51, 48, 45, 52, 49, 46, 53, 50, 47]
        self.F1_dict = [0, 1, 2, 3, 4, 5, 44, 41, 38, 6, 10, 11, 7, 13, 14, 8, 16, 17, 24, 21, 18, 25, 22, 19, 26, 23, 20, 15, 12, 9, 30, 31, 32, 33, 34, 35, 36, 37, 27, 39, 40, 28, 42, 43, 29, 45, 46, 47, 48, 49, 50, 51, 52, 53]
        self.U1_dict = [6, 3, 0, 7, 4, 1, 8, 5, 2, 45, 46, 47, 12, 13, 14, 15, 16, 17, 9, 10, 11, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 18, 19, 20, 39, 40, 41, 42, 43, 44, 36, 37, 38, 48, 49, 50, 51, 52, 53]
        self.D1_dict = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 24, 25, 26, 18, 19, 20, 21, 22, 23, 42, 43, 44, 33, 30, 27, 34, 31, 28, 35, 32, 29, 36, 37, 38, 39, 40, 41, 51, 52, 53, 45, 46, 47, 48, 49, 50, 15, 16, 17]
        self.rotate_dict = self.create_rotate_dict(count=5)
        self.letter_rotate = {
            "R": self.R1_dict,
            "L": self.L1_dict,
            "B": self.B1_dict,
            "F": self.F1_dict,
            "U": self.U1_dict,
            "D": self.D1_dict
        }
        self.end_dict = self.rotate()
        self.end_dict_normal = self.to_number_end_dict(self.end_dict)
        self.final_string = self.end_dict_to_final_string(self.end_dict_normal)

    def create_rotate_dict(self, count=2):
        rotate_dict = []
        letter_dict = ['R', 'L', 'B', 'F', 'U', 'D']
        
        for i in range(count):
            # rotate_dict.append([letter_dict[random.randint(0, 5)], random.randint(1, 3)])
            rotate_dict.append(letter_dict[random.randint(0, 5)])
        return rotate_dict
    
    def rotate(self):
        start_dict = self.r0_dict
        current_dict = []
        for i in self.rotate_dict: # Убедитесь, что вы используете правильный список для итерации
            # print(self.letter_rotate)
            transform_dict = self.letter_rotate[i]
            for k in range(54):
                current_dict.append(start_dict[transform_dict[k]])
            start_dict = current_dict
            current_dict = []
        return start_dict
    
    def to_number_end_dict(self, end_dict):
        dict = []
        for num in end_dict:
            dict.append(1+ num)
        return dict
    
    def end_dict_to_final_string(self, end_dict_normal):
        string = ''
        # dict = {
        #     0: 'U',
        #     1: 'R',
        #     2: 'F',
        #     3: 'D',
        #     4: 'L',
        #     5: 'B'
        # }
        # for i in self.end_dict:
        #     string += dict[i // 9]
        for i in end_dict_normal:
            if int(i) >=1 and int(i) <= 9:
                string += 'U'
            if int(i) >=10 and int(i) <= 18:
                string += 'R'
            if int(i) >=19 and int(i) <= 27:
                string += 'F'
            if int(i) >=28 and int(i) <= 36:
                string += 'D'
            if int(i) >=37 and int(i) <= 45:
                string += 'L'
            if int(i) >=46 and int(i) <= 54:
                string += 'B'
        
        return string



StrYing = GenerateString()
print(StrYing.rotate_dict)
print(StrYing.end_dict_normal)
print(StrYing.final_string)


def count_letters(s):
    # Создаем пустой словарь для подсчета букв
    letter_counts = {}
    
    # Проходим по каждому символу в строке
    for letter in s:
        # Если буква уже есть в словаре, увеличиваем ее счетчик
        if letter in letter_counts:
            letter_counts[letter] += 1
        # Если буквы еще нет в словаре, добавляем ее с счетчиком 1
        else:
            letter_counts[letter] = 1
    
    return letter_counts

# Исходная строка
s = StrYing.final_string

# Вызываем функцию и выводим результат
print(count_letters(s))
print(sorted(count_letters(StrYing.end_dict_normal)))

# print(sv.solve(StrYing.end_dict_to_final_string(StrYing.to_number_end_dict(StrYing.D1_dict))))
print(sv.solve(s))




