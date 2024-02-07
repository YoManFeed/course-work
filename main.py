from code_processor import InitCodes, EncodingProcessor
from my_logging import show_logs, show
from image_processor import *
from tqdm import tqdm


if __name__ == '__main__':
    show_logs(False)
    initialisation = InitCodes()
    inner = initialisation.inner
    external = initialisation.external
    neg_inner = initialisation.neg_inner
    neg_external = initialisation.neg_external

    external = external[:4]
    neg_external = neg_external[:4]

    code_proc = EncodingProcessor()

    img_gen = ImageGenerator()
    inner_arches = img_gen.inner_arches
    external_arches = img_gen.external_arches

    img_proc = ImageProcessor()

    for ex_counter, (external_line, external_line_neg) in tqdm(enumerate(zip(external, neg_external), start=1), desc="Processing External", unit="lines", total=len(external)):
        for inn_counter, (inner_line, inner_line_neg) in enumerate(zip(inner, neg_inner), start=1):

            FileManager.make_dirs(ex_counter)

            for step in range(rotation_steps):
                shifted_inner_code = np.roll(inner_line_neg, step)
                external_line_neg = np.roll(external_line_neg, 0)
                if code_proc.cyclic_check(external_line_neg, shifted_inner_code):

                    ax = code_proc.axes_of_symmetry(external_line_neg)[0]
                    symmetric_check = (-1 * np.array(shifted_inner_code)[::-1]).tolist()
                    external_check = (code_proc.symmetric_inner_code(inner_line_neg, ax))
                    # codes_counter += 1

                    if (ex_counter, shifted_inner_code.tolist()) not in result:
                        if (ex_counter, symmetric_check) not in result:
                            if (ex_counter, external_check) not in result:
                                result.append((ex_counter, external_check))

                                if bool_draw_circle:
                                    img_gen.draw(external_line_neg, shifted_inner_code, step, inn_counter, ex_counter)
    # print(f'Всего расположений 8-й степени с учётом запретов: {len(result)}')
