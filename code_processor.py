import numpy as np
from math import copysign
from params import *
from file_manager import FileManager
from image_processor import ImageGenerator


class InitCodes:
    def __init__(self):
        if bool_generate_again:
            self.catalan_codes = self.catalan(cnt, ind, arches, init)
            pair_indexes = list(map(EncodingProcessor.catal_into_arch_indx, self.catalan_codes))
            inner, external = EncodingProcessor.making_arches(pair_indexes)
            self.inner = np.array(EncodingProcessor.remove_repeated(inner))
            self.external = np.array(EncodingProcessor.remove_repeated(external))
            self.neg_inner = np.array(EncodingProcessor.make_negatives(self.inner))
            self.neg_external = np.array(EncodingProcessor.make_negatives(self.external))
            print('Codes were generated successfully')

            if bool_save_codes:
                FileManager.write_code(catalan_path, self.catalan_codes)
                FileManager.write_code(pair_indx_path, pair_indexes)
                FileManager.write_code(inner_code_path, self.inner)
                FileManager.write_code(external_code_path, self.external)
                FileManager.write_code(neg_inner_code_path, self.neg_inner)
                FileManager.write_code(neg_external_code_path, self.neg_external)
                print(f'Codes were saved successfully')

        else:
            self.inner = np.array(FileManager.read_codes(inner_code_path))
            self.external = np.array(FileManager.read_codes(external_code_path))
            self.neg_inner = np.array(FileManager.read_codes(neg_inner_code_path))
            self.neg_external = np.array(FileManager.read_codes(neg_external_code_path))
            print(f'Codes were loaded successfully')

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


class EncodingProcessor:
    @staticmethod
    def catal_into_arch_indx(number: int) -> list[tuple]:
        stack_ind_1 = []
        ans = []
        for i, digit in enumerate(str(int(number))):
            if digit == '1':
                stack_ind_1.append(i)
            else:
                ans.append((stack_ind_1.pop(), i))
        return ans

    @staticmethod
    def making_arches(codes: list[list[tuple]]):
        inner, external = [], []
        for indexes in codes:
            positions = [0] * arches
            for (x, y) in indexes:
                arch_len = (y - x + 1) // 2
                positions[x] = arch_len
            if EncodingProcessor.external_checker(positions):
                external.append(positions)
            if not any(border < x for x in positions):
                inner.append(positions)
        return inner, external

    @staticmethod
    def external_checker(code: list[int]) -> bool:
        counter = 0
        for digit in code:
            if digit > 0:
                counter += 1
                if counter > border:
                    return False
            else:
                counter -= 1
        return True


    @staticmethod
    def remove_repeated(codes: list[list[int]]) -> list[list[int]]:
        non_repeated = []
        for block in codes:
            to_check = [np.roll(block, i) for i in range(len(block))]
            to_check = [tuple(shifted) for shifted in to_check]

            if all(elem not in non_repeated for elem in to_check):
                non_repeated.append(to_check[0])
        return non_repeated

    @staticmethod
    def make_negatives(codes: list[int]) -> list[int]:
        ans = []
        for code in codes:
            code = np.array(code)
            output = np.zeros_like(code)

            non_zero_indices = code.nonzero()[0]
            output[non_zero_indices] = code[non_zero_indices]
            output[2 * code[non_zero_indices] + non_zero_indices - 1] = -code[non_zero_indices]
            output = output.tolist()
            ans.append(output)
        return ans

    @staticmethod
    def sign(y) -> int:
        return int(copysign(1, y))

    @staticmethod
    def ar_mod(number: int, base: int):
        if number < 0:
            return number + base
        elif 0 <= number < base:
            return number
        else:
            return number - base

    def cyclic_check(self, code1: list[int], code2: list[int]) -> bool:
        i = 0
        base = len(code1)
        for counter in range(base):
            elem1 = code1[i]
            elem2 = code2[i]
            i = i + 2 * elem2 - self.sign(elem2)
            i = self.ar_mod(i, base=base)
            elem2 = code2[i]
            elem1 = code1[i]
            i = i + 2 * elem1 - self.sign(elem1)
            i = self.ar_mod(i, base=base)
            if i == 0 and counter < -1 + base // 2:
                return False
        return True

    # @staticmethod
    # def axes_of_symmetry(code):
    #     axes = []
    #     sum = 0
    #     left_index = 0
    #     for i, digit in enumerate(code):
    #         sum += digit
    #         if sum == 0:
    #             axes.append((left_index + i) // 2 + 1)
    #             left_index = i + 1
    #     return axes
    @staticmethod
    def axes_of_symmetry(code):
        sum = 0
        for i, digit in enumerate(code):
            sum += digit
            if sum == 0:
                return i // 2 + 1

    @staticmethod
    def symmetric_inner_code(code, ax):
        code = (-1 * np.roll(code, -ax))[::-1]
        return np.roll(code, ax).tolist()

    # @staticmethod
    # def cusum_double_check(code):
    #     s1 = 0
    #     s2 = 0
    #     for digit in code:
    #         if digit < 0:
    #             s1 += 1
    #         else:
    #             break
    #
    #     for digit in reversed(code):
    #         if digit > 0:
    #             s2 += 1
    #         else:
    #             break
    #
    #     return max(s1, s2)

    @staticmethod
    def cusum(code):
        s = 0
        for i, digit in enumerate(code):
            try:
                _ = code[i + 2 * digit - 1]
            except IndexError:
                s += 1
        return s

    def Bezu(self, ex_code, in_code):
        n = len(ex_code)
        bezu_arr = np.zeros(n+1, dtype=int)

        for i, (elem1, elem2) in enumerate(zip(ex_code, in_code), start=1):
            bezu_arr[i] = self.sign(elem1) + self.sign(elem2) + bezu_arr[i-1]
        bezu_arr = bezu_arr[1:]
        # if min(bezu_arr) < 0:
        bezu_arr += self.cusum(in_code)
        return bezu_arr

    @staticmethod
    def max_sum(code):
        return sum(sorted(code)[-2:])

    def Bezu_prohibit(self, code, bezu_code):
        # print(code)
        # print(bezu_code)
        indices = np.where((code == 1) | (code == -1))[0]
        pairs = bezu_code[indices]

        # print(pairs)
        odd = pairs[1::2]
        even = pairs[::2]
        # print(odd, even)

        if (self.max_sum(odd) > deg) or (self.max_sum(even) > deg):
            return False
        else:
            return True



if __name__ == "__main__":

    EP = EncodingProcessor()
    IG = ImageGenerator()
    # # print(EP.Bezu([2,1,-1,-2,1,-1,2,1,-1,-2,1,-1], [-1,3,2,1,-1,-2,-3,2,1,-1,-2,1]))
    # res = EP.Bezu([2,1,-1,-2,1,-1,2,1,-1,-2,1,-1], [1,-1,-2,3,2,1,-1,-2,-3,1,-1,2])
    # # res = EP.Bezu([6,1,-1,2,1,-1,-2,1,-1,1,-1,-6], [3,2,1,-1,-2,-3,1,-1,1,-1,1,-1])
    # # res[-1] = 10
    # EP.Bezu_prohibit(np.array([2,1,-1,-2,1,-1,2,1,-1,-2,1,-1]), res)
    #
    # # EP.max_sum([ 4, 4, 4, 2, 2, 2, 2, 10])
    #
    # # a = np.array([1, -1, -3, 3, 2, 1, -1, -2, -3, 3, 1, -1])
    #
    # ex = np.array([4,3,1,-1,1,-1,-3,-4,2,1,-1,-2])
    # inn = np.array([-1,-2,3,1,-1,1,-1,-3,1,-1,2,1])
    # # bezu = np.array([2,2,4,4,4,4,2,0,2,2,2,2])
    # # inn = np.array([2,1,-1,-2,-3,3,2,1,-1,-2,-3,3])
    #
    # print(f'ex =  {ex}')
    # print(f'inn = {inn}')
    # print(f'EP.cusum(inn) = {EP.cusum(inn)}')
    # print(f'EP.Bezu(ex, inn) = {EP.Bezu(ex, inn)}')
    # print(EP.Bezu_prohibit(inn, EP.Bezu(ex, inn)))

    ex = np.array([5,4,1,-1,1,-1,1,-1,-4,-5,1,-1])
    inn = np.array([-1,1,-1,-3,3,1,-1,1,-1,-3,3,1])

    # IG.draw(ex, inn, res=None, show=True)
    #
    # ax = EP.axes_of_symmetry(ex)
    # symmetric_check = (-1 * np.array(inn)[::-1]).tolist()
    #
    # IG.draw(ex, symmetric_check, res=None, show=True)
    #
    # external_check = EP.symmetric_inner_code(inn, ax)
    #
    # ex = ex
    # IG.draw(ex, external_check, res=None, show=True)
    test = np.array([1,2,3,4,5,6,7,8])
    print(np.roll(test, 2))