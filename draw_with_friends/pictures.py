from PIL import Image

left_colors = ['Red', 'Orange', 'Yellow', 'Green',
               'Blue', 'DarkBlue', 'Purple', 'Navy']

right_colors = ['White', 'Black', 'Grey', 'SaddleBrown',
                'Aqua', 'Lime', 'Silver', 'Maroon']

colors_rgb = {'Red': (255, 0, 0),
              'Orange': (255, 165, 0),
              'Yellow': (255, 255, 0),
              'Green': (0, 128, 0),
              'Blue': (0, 0, 255),
              'DarkBlue': (0, 0, 139),
              'Purple': (128, 0, 128),
              'Navy': (0, 0, 128),
              'White': (255, 255, 255),
              'Black': (0, 0, 0),
              'Grey': (128, 128, 128),
              'SaddleBrown': (139, 69, 19),
              'Aqua': (0, 255, 255),
              'Lime': (0, 255, 0),
              'Silver': (192, 192, 192),
              'Maroon': (128, 0, 0)}

size = 64


# Делает картинку полностью белой
def renew_picture():
    tmp = Image.open('static/picture.png')
    for i in range(size):
        for j in range(size):
            tmp.putpixel((i, j), colors_rgb['White'])

    tmp.save('static/picture.png')
    tmp.close()


# Красит данный пиксель в данный цвет
def set_pixel(x, y, color_):
    tmp = Image.open('static/picture.png')
    tmp.putpixel((x, y), colors_rgb[color_])
    tmp.save('static/picture.png')
    tmp.close()


button_positions = []  # доступные координаты квадратиков у картинки, меняются
button_positions_draw = []  # координаты квадратиков у картинки, еменяются
for i in range(8):
    for j in range(8):
        button_positions.append((i*64, j*64))
        button_positions_draw.append((i*64, j*64))
