import numpy as np
from math import copysign
from params import *
from file_manager import FileManager


class InitCodes:
    def __init__(self):
        if bool_generate_again:
            self.catalan_codes = self.catalan(cnt, ind, arches, init)
            pair_indexes = list(map(EncodingProcessor.catal_into_arch_indx, self.catalan_codes))
            inner, external = EncodingProcessor.making_arches(pair_indexes)
            self.inner = EncodingProcessor.remove_repeated(inner)
            self.external = EncodingProcessor.remove_repeated(external)
            self.neg_inner = EncodingProcessor.make_negatives(self.inner)
            self.neg_external = EncodingProcessor.make_negatives(self.external)
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
            self.inner = FileManager.read_codes(inner_code_path)
            self.external = FileManager.read_codes(external_code_path)
            self.neg_inner = FileManager.read_codes(neg_inner_code_path)
            self.neg_external = FileManager.read_codes(neg_external_code_path)
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
        if bool_prohibit:
            counter = 0
            for digit in code:
                if digit > 0:
                    counter += 1
                    if counter > border:
                        return False
                else:
                    counter -= 1
            return True
        else:
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

    @staticmethod
    def axes_of_symmetry(code):
        axes = []
        sum = 0
        left_index = 0
        for i, digit in enumerate(code):
            sum += digit
            if sum == 0:
                axes.append((left_index + i) // 2 + 1)
                left_index = i + 1
        return axes

    @staticmethod
    def symmetric_inner_code(code, ax):
        code = (-1 * np.roll(code, -ax))[::-1]
        return np.roll(code, ax).tolist()
