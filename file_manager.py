from params import *
from icecream import ic
from PIL import Image


class FileManager:
    def __init__(self):
        current_dir = os.getcwd()
        self.output_path = os.path.join(current_dir, 'output.png')
        self.image_path_circle = os.path.join(current_dir, 'circle.png')
        self.image_path_transparent = os.path.join(current_dir, 'transparent.png')
        self.inner_quantity, self.external_quantity = self.get_quantity()
        if bool_save_pics:
            self.make_dirs(self.external_quantity)


    def get_quantity(self):
        for kind in ['inner', 'external']:
            try:
                all_files = os.listdir(os.path.join(current_dir, f'{kind}/deg_{deg}'))
                png_files = [file for file in all_files if file.endswith('.png')]
                if kind == 'inner':
                    self.inner_quantity = len(png_files)
                else:
                    self.external_quantity = len(png_files)
            except FileNotFoundError:
                raise ValueError('В папке нет картинок дуг')
        return self.inner_quantity, self.external_quantity

    @staticmethod
    def read_codes(file_path):
        with open(file_path) as file:
            return [list(map(int, line.split())) for line in file]

    # @staticmethod


    @staticmethod
    def write_code(path: str, codes: list or np.ndarray) -> None:
        # flag = 1
        # print(isinstance(codes, list))
        if isinstance(codes, list):
            with open(path, mode='w') as file:
                for elem in codes:
                    elem = list(map(str, elem))
                    item = " ".join(elem)
                    file.write("%s\n" % item)
        elif type(codes) is np.ndarray:
            np.savetxt(path, codes, fmt='%d')
        else:
            ic('Raise Error: Unexpected file type!', type(codes))
            # flag = 0
        # if bool_show_log and flag:
        #     ic(path.split(sep='/')[-1][:-4])
        #     ic('file saved!')

    @staticmethod
    def make_dirs(ex_counter):
        if f'external_{ex_counter}' not in os.listdir(output_folder):
            os.mkdir(f'{output_folder}/external_{ex_counter}')


    @staticmethod
    def save_img(img, path):
        data = Image.fromarray(img)
        data.save(path)
