import cv2
import math
from settings import *
from working_with_images import show_me


def generate_circle_points(center, radius, num_points):
    points = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi
        x = center[0] + int(radius * math.cos(angle))
        y = center[1] + int(radius * math.sin(angle))
        points.append((x, y))
    return points


def connect_circles(image, x, y, alpha, r, R):
    R_c = round((math.sqrt(R ** 2 + (r * R / (R + r)) ** 2) + math.sqrt(r ** 2 + (r ** 2 / (R + r)) ** 2)))
    phi = math.atan((r / (R + r)))
    image = cv2.ellipse(image, (x, y), (R_c, R_c), 0, 180 + math.degrees(phi),
                        180 + math.degrees(alpha) - math.degrees(phi), colour, 2)
    return image


def draw_inner_arch(image, x1, y1, x2, y2, i, alpha):
    center = ((x1 + x2) // 2, (y1 + y2) // 2)
    ro = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) / 2
    axes = (int(ro), int(math.sqrt(5) * ro / (4*(i+1))))
    angle = -75 + i * math.degrees(alpha / 2)
    image = cv2.ellipse(image, center, axes, angle, 0, 180, colour, thickness)
    return image


if __name__ == '__main__':
    image_size = (512, 512)
    center = (image_size[0] // 2, image_size[1] // 2)
    thickness = 3

    deg = 4
    num_points = 2 * deg
    R = image_size[0] // 4
    D = 2*R
    r = R // (deg+2)
    colour = (0, 0, 0, 255)
    thickness = 2
    alpha = 2 * math.pi / num_points

    points = generate_circle_points(center, R, num_points)
    points = points[num_points // 2:] + points[:num_points // 2]

    n_channels = 4
    blanc_img = np.zeros((image_size[0], image_size[1], n_channels), dtype=np.uint8)

    for i, point in enumerate(points):
        if i % 2 == 1:
            angle = i * alpha
            r_upd = r + r * (i // 2)
            center = (round(point[0] - r_upd * math.sin(angle)), round(point[1] + r_upd * math.cos(angle)))

            image = blanc_img.copy()
            # image = cv2.ellipse(image, (D, D), (R, R), 0, 0, 360, (255, 255, 255), 2)

            image = cv2.ellipse(image, (R, D - r_upd), (r_upd, r_upd), 0, 90, 180, colour, thickness)
            image = cv2.ellipse(image, center, (r_upd, r_upd), 0, 180 + math.degrees(angle), 270 + math.degrees(angle), colour, thickness)
            image = connect_circles(image, D, D, angle, r_upd, R)
            # show_me(image)

            cv2.imwrite(f"./external/deg_{deg}/external_arch_{i // 2 + 1}.png", image)

            if i // 2 < deg // 2:
                image = blanc_img.copy()
                result = draw_inner_arch(image, points[0][0], points[0][1], point[0], point[1], i - 1, alpha)
                cv2.imwrite(f"./inner/deg_{deg}/inner_arch_{i // 2 + 1}.png", image)
                # show_me(result)
