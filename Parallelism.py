from multiprocessing import Pool
from json import load
import numpy as np


def element(args):
    index, A, B = args[0], args[1], args[2]
    i, j = index
    res = 0
    f = open('prom.txt', 'a')
    N = A.shape[1] or B.shape[0]
    for k in range(N):
        res += A[i, k] * B[k, j]
    f.write(str(res) + '\n')  # Запись в промежуточный файл
    f.close()
    return res


def check_matrix(matrix1, matrix2):
    if matrix1.shape[1] == matrix2.shape[0]:
        return True
    else:
        print('Такие матрицы нельзя перемножить!')


def generate_map(matrix1, matrix2):
    args = []
    for i in range(matrix1.shape[0]):
        for j in range(matrix2.shape[1]):
            args.append(((i, j), matrix1, matrix2))
    return args


def write_result_to_file(matrix, filename):
    file = open(filename, 'w')
    for line in matrix:
        for elem in line:
            file.write(f'{elem}\t')
        file.write('\n')
    file.close()


if __name__ == '__main__':
    with open('matrix1.json', 'r') as f:
        matrix1 = np.matrix(load(f))

    with open('matrix2.json', 'r') as f:
        matrix2 = np.matrix(load(f))

    p = Pool(5)
    if check_matrix(matrix1, matrix2):
        open('prom.txt', 'w').close()
        args = generate_map(matrix1, matrix2)
        result = np.array(p.map(element, args))
        matrix = result.reshape(matrix1.shape[0], matrix2.shape[1])
        print(matrix)
        write_result_to_file(matrix, 'result.txt')
    else:
        file = open('result.txt', 'w')
        file.close()
