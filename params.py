import numpy as np
import os

bool_generate_again = 1  # Надо ли ещё раз генерировать коды через данную степень
bool_save_codes = 0      # Надо ли сохранять коды
bool_draw_circle = 0     # Надо ли рисовать круг
bool_color_bgrd = 0      # Надо ли красить и сохранять задний фон
bool_show_log = 1        # Показывать логи
bool_save_pics = 1       # Надо ли сохранять картинки
bool_prohibit = 1        # Надо ли запрещать расположения
bool_labeling = 1        # Надо ли писать коды на картинках

# Глобальные параметры
deg = 6
arches = deg * 2
border = deg / 2  # какие длины дуг запрещены для внутренних кодировок

rotation_steps = arches
rotation_angle = 360/rotation_steps

# Для каталана
generated_numbers = np.array([], dtype=int)
init = list(np.zeros(arches))  # пустой список, куда будем писать последовательности
cnt = 0  # разница между 1 и 0
ind = 0  # индекс, по которому пишем число в список

current_dir = os.getcwd()
output_folder = os.path.join(current_dir, 'output')

catalan_path = os.path.join(current_dir, f'codes/catalan_codes_deg_{deg}.txt')
pair_indx_path = os.path.join(current_dir, f'codes/pair_indx_codes_deg_{deg}.txt')
inner_code_path = os.path.join(current_dir, f'codes/inner_codes_deg_{deg}.txt')
external_code_path = os.path.join(current_dir, f'codes/external_codes_deg_{deg}.txt')
neg_inner_code_path = os.path.join(current_dir, f'codes/neg_inner_codes_deg_{deg}.txt')
neg_external_code_path = os.path.join(current_dir, f'codes/neg_external_codes_deg_{deg}.txt')

result = []

