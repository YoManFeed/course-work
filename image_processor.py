import my_logging
from params import *
from file_manager import FileManager
import cv2
from PIL import Image


class ImageGenerator:
    def __init__(self):
        self.inner_quantity, self.external_quantity = FileManager().get_quantity()
        self.inner_arches = ImageProcessor().read_arches(quantity=self.inner_quantity, draw_circle=True)
        self.external_arches = ImageProcessor().read_arches(quantity=self.external_quantity, draw_circle=False)

    # @staticmethod
    def draw(self, external_line_neg, shifted_inner_code, step=None, inn_counter=None, ex_counter=None, res=None, show=False):
        code_external = [max(0, x) for x in external_line_neg]
        code_inner = [max(0, x) for x in shifted_inner_code]
        # code_inner = [max(0, x) for x in shifted_inner_code.tolist()]
        inner_circle = self.gather_arches(code=code_inner, arches_type=self.inner_arches)
        external_circle = self.gather_arches(code=code_external, arches_type=self.external_arches)
        self.combining(
            inner=inner_circle, external=external_circle, external_line=external_line_neg, step=step,
            inner_line=shifted_inner_code, ex_counter=ex_counter, inn_counter=inn_counter, res=res, show=show)

    # makes inner and external
    def gather_arches(self, code, arches_type):
        temp = arches_type[0]  # Change inner to external to show/hide circle
        for i in range(rotation_steps):
            angle = i * rotation_angle
            arch_index = code[i]
            if arch_index != 0:
                rotated = self.rotation(arches_type[arch_index], angle)
                temp = self.combine(temp, rotated)
        return temp

    def rotation(self, image, angle):
        rot_mat = cv2.getRotationMatrix2D(angle=-angle, scale=1., center=(256, 256))
        rotated_circle = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderMode=1)
        return rotated_circle

    def combine(self, img1, img2):
        alpha_1 = img1[:, :, 3]
        alpha_2 = img2[:, :, 3]

        rgb_1 = img1[:, :, :3]
        rgb_2 = img2[:, :, :3]

        merged_alpha = cv2.bitwise_or(alpha_1, alpha_2)
        merged_bw = cv2.bitwise_and(rgb_1, rgb_2)

        result = np.zeros_like(img1)
        result[:, :, :3] = merged_bw
        result[:, :, 3] = merged_alpha

        return result

    def combining(self, inner, external, external_line, inner_line, step=None, inn_counter=None, ex_counter=None, res=None, show=None):
        # combining
        combination = cv2.addWeighted(external, 0.5, inner, 0.5, 0)
        gray = cv2.cvtColor(combination, cv2.COLOR_BGR2HSV)[:, :, 2]
        T = cv2.ximgproc.niBlackThreshold(gray, maxValue=255, type=cv2.THRESH_BINARY_INV, blockSize=81,
                                          k=0.1, binarizationMethod=cv2.ximgproc.BINARIZATION_WOLF)
        grayb = (gray > T).astype("uint8") * 255

        # smoothing
        dst = cv2.GaussianBlur(grayb, (3, 3), 0)

        # labeling
        if bool_labeling:
            upper_text = ''.join([str(num) if num < 0 else f' {num}' for num in external_line])
            bottom_text = ''.join([str(num) if num < 0 else f' {num}' for num in inner_line])
            if res is None:
                pass
            else:
                extra_text = ''.join([str(num) if num < 0 else f' {num}' for num in res])
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 0.8
            font_color = (120, 0, 120)
            thickness = 1

            # Координаты начальной точки для текста
            org_1 = (25, 25)
            org_2 = (25, 50)
            cv2.putText(dst, upper_text, org_1, font, font_scale, font_color, thickness)
            cv2.putText(dst, bottom_text, org_2, font, font_scale, font_color, thickness)

            if res is None:
                pass
            else:
                org_3 = (25, 75)
                cv2.putText(dst, extra_text, org_3, font, font_scale, font_color, thickness)

        # saving
        if bool_save_pics and ex_counter is not None and inn_counter is not None and step is not None:
            FileManager.make_dirs(ex_counter)
            new_filename = f'circle_e{ex_counter}_i{inn_counter}_s{step}.png'
            output_path = os.path.join(f'{output_folder}/external_{ex_counter}', new_filename)
            # output_path = os.path.join(f'{output_folder}', new_filename)
            FileManager.save_img(img=dst, path=output_path)

        if show:
            my_logging.show_me(dst)


        # coloring
        # if bool_color_bgrd:
        #     output_path_colored = os.path.join(f'{output_folder}_colored/external_{ex_counter}', new_filename)
        #     data_colored = Image.fromarray(self.coloring(image=dst))
        #     data_colored.save(output_path_colored)

class ImageProcessor:
    def __init__(self):
        pass

    @staticmethod
    def remove_background(image):
        """
        Sometimes artefacts occurs on the image. Try another method to read the image:
        image = cv2.imread(image_path)  # with white background
        image = read_transparent_png(image_path)  # with transparent background
        """
        # makes mask that shows if pixel falls into a specific range in BGR color space
        lower_color = np.array([200, 200, 200], dtype=np.uint8)
        upper_color = np.array([255, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(image, lower_color, upper_color)

        # creates alpha channel where all pixels in range are transparent
        alpha_channel = np.where(mask > 0, 0, 255).astype(np.uint8)
        image_with_transparency = cv2.merge((image[:, :, :3], alpha_channel))

        # coloring all pixels that are not transparent
        black_mask = (alpha_channel == 255)
        image_with_transparency[black_mask] = [0, 0, 0, 255]

        return image_with_transparency

    @staticmethod
    def read_transparent_png(img_path):
        image_4channel = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        alpha_channel = image_4channel[:, :, 3]
        rgb_channels = image_4channel[:, :, :3]

        # White Background Image
        white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

        # Alpha factor
        alpha_factor = alpha_channel[:, :, np.newaxis].astype(np.float32) / 255.0
        alpha_factor = np.concatenate((alpha_factor, alpha_factor, alpha_factor), axis=2)

        # Transparent Image Rendered on White Background
        base = rgb_channels.astype(np.float32) * alpha_factor
        white = white_background_image.astype(np.float32) * (1 - alpha_factor)
        final_image = base + white

        return final_image.astype(np.uint8)

    @staticmethod
    def read_arches(quantity, draw_circle):
        img_paths = np.empty(quantity + 1, dtype=object)
        images = np.empty(quantity + 1, dtype=object)

        if draw_circle:
            img_paths[0] = FileManager().image_path_circle
        else:
            img_paths[0] = FileManager().image_path_transparent

        if quantity == FileManager().inner_quantity:
            arch_type = 'inner'
        else:
            arch_type = 'external'

        images[0] = ImageProcessor().remove_background(ImageProcessor.read_transparent_png(img_paths[0]))
        for i in range(1, quantity + 1):
            img_paths[i] = os.path.join(current_dir, f'{arch_type}/deg_{deg}/{arch_type}_arch_{i}.png')
            images[i] = ImageProcessor.remove_background(ImageProcessor.read_transparent_png(img_paths[i]))
        return images


