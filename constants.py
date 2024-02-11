import os


class Constants:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.deg = 4
        self.arches = self.deg * 2
        self.border = self.deg / 2  # какие длины дуг запрещены для внутренних кодировок

    def get_quantity(self):
        for kind in ['inner', 'external']:
            try:
                all_files = os.listdir(os.path.join(self.current_dir, f'{kind}/deg_{self.deg}'))
                png_files = [file for file in all_files if file.endswith('.png')]
                if kind == 'inner':
                    self.inner_quantity = len(png_files)
                else:
                    self.external_quantity = len(png_files)
            except FileNotFoundError:
                raise ValueError('В папке нет картинок дуг')
        return self.inner_quantity, self.external_quantity
