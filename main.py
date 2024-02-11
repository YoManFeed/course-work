import numpy as np

from code_processor import InitCodes, EncodingProcessor
from my_logging import show_logs, show
from image_processor import *
from tqdm import tqdm


if __name__ == '__main__':
    show_logs(False)
    initialisation = InitCodes()

    ex_start = 0
    ex_end = 810
    in_start = 0
    # in_end = None

    inner = initialisation.inner[in_start:]
    neg_inner = initialisation.neg_inner[in_start:]
    external = initialisation.external[ex_start:ex_end]
    neg_external = initialisation.neg_external[ex_start:ex_end]

    code_proc = EncodingProcessor()

    img_gen = ImageGenerator()
    inner_arches = img_gen.inner_arches
    external_arches = img_gen.external_arches

    img_proc = ImageProcessor()
    i = 0

    for ex_counter, (external_line, external_line_neg) in tqdm(enumerate(zip(external, neg_external), start=ex_start+1), desc="Processing External", unit="lines", total=len(external)):
        for inn_counter, (inner_line, inner_line_neg) in enumerate(zip(inner, neg_inner), start=in_start+1):

            for step in range(rotation_steps):
                shifted_inner_code = np.roll(inner_line_neg, step)
                if code_proc.cyclic_check(external_line_neg, shifted_inner_code):
                    ax = code_proc.axes_of_symmetry(external_line_neg)
                    symmetric_check = (-1 * np.array(shifted_inner_code)[::-1]).tolist()
                    external_check = (code_proc.symmetric_inner_code(inner_line_neg, ax))

                    # if (ex_counter, shifted_inner_code.tolist()) not in result: # (нет эффекта, когда все запреты вкл)
                    if (ex_counter, symmetric_check) not in result:
                        if (ex_counter, external_check) not in result:
                            res = code_proc.Bezu(external_line_neg, shifted_inner_code)

                            if code_proc.Bezu_prohibit(shifted_inner_code, res):
                            # if True:
                                result.append((ex_counter, external_check))
                                if bool_draw_circle:
                                    img_gen.draw(external_line_neg, shifted_inner_code, step, inn_counter, ex_counter)

    # print(i)
    print(len(result))
