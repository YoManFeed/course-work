import numpy as np
import timeit

class EncodingProcessor:
    def catalan(self, cnt: int, ind: int, arches: int, init: np.ndarray) -> np.ndarray:
        global generated_numbers
        if cnt <= arches - ind - 2:
            init[ind] = '1'
            self.catalan(cnt + 1, ind + 1, arches, init)
        if cnt > 0:
            init[ind] = '0'
            self.catalan(cnt - 1, ind + 1, arches, init)
        if ind == arches:
            if cnt == 0:
                generated_numbers = np.append(generated_numbers, int(''.join(init)))
        return generated_numbers

    @staticmethod
    def catal_into_arch_indx_vectorize(number):
        stack_ind_1 = []
        ans = []
        for i, digit in enumerate(str(int(number))):
            if digit == '1':
                stack_ind_1.append(i)
            elif stack_ind_1:
                ans.append((stack_ind_1.pop(), i))
        return ans

    @staticmethod
    def catal_into_arch_indx_loop(number):
        stack_ind_1 = []
        ans = []
        for i, digit in enumerate(str(int(number))):
            if digit == '1':
                stack_ind_1.append(i)
            elif stack_ind_1:
                ans.append((stack_ind_1.pop(), i))
        return ans

    @staticmethod
    def catal_into_arch_indx_map(number):
        stack_ind_1 = []
        ans = []
        for i, digit in enumerate(str(int(number))):
            if digit == '1':
                stack_ind_1.append(i)
            elif stack_ind_1:
                ans.append((stack_ind_1.pop(), i))
        return ans


# Глобальные параметры
deg = 10
arches = deg * 2
border = deg / 2  # какие длины дуг запрещены для внутренних кодировок

# Для каталана
generated_numbers = np.array([], dtype=int)
init = list(np.zeros(arches))  # пустой список, куда будем писать последовательности
cnt = 0  # разница между 1 и 0
ind = 0  # индекс, по которому пишем число в список

process = EncodingProcessor()
catalan_codes = process.catalan(cnt, ind, arches, init)

print(catalan_codes)

# Vectorize
vectorized_func = np.vectorize(EncodingProcessor.catal_into_arch_indx_vectorize, otypes=[object])
vectorize_time = timeit.timeit(lambda: vectorized_func(catalan_codes), number=1)

import time
# Loop
start = time.time()
temp_2 = [EncodingProcessor.catal_into_arch_indx_loop(x) for x in catalan_codes]
loop_time = time.time() - start

# Map
start = time.time()
temp_3 = list(map(EncodingProcessor.catal_into_arch_indx_map, catalan_codes))
map_time = time.time() - start


print(f"Vectorize Time: {vectorize_time}")
print(f"Loop Time: {loop_time}")
print(f"Map Time: {map_time}")
