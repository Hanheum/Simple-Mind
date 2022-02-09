from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from time import time
import pyautogui

image_name = input('image name:')
code_start_time = time()

model = load_model('banana.obj')
foods = []
positions = []

class Voxel(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            model='sphere',
            color=color.yellow,
            position=position,
            collider='mesh',
        )

def get_random_position():
    x = random.randint(-25, 25)
    z = random.randint(-25, 25)
    position = Vec3(x, 1, z)
    return position

app = Ursina()

start_time = time()

for i in range(100):
    new_food = Voxel(position=get_random_position())

def update():
    global start_time, new_food, new_food_index
    present_time = time()
    '''if present_time-start_time > 60:
        new_food_index = random.randint(0, int(len(models)-1))
        new_food = food(model=models[new_food_index], color=colors[new_food_index], position=get_random_position())
        start_time = present_time'''

    if held_keys['g']:
        screen_shot = pyautogui.screenshot()
        x_start = 256
        y_start = 144
        x_end = 2304
        y_end = 1152
        image = screen_shot.crop((x_start, y_start, x_end, y_end))
        image = image.resize((700, 700))
        for a in range(7):
            for b in range(7):
                x_start = a * 100
                y_start = b * 100
                x_end = x_start + 100
                y_end = y_start + 100
                cropped_image = image.crop((x_start, y_start, x_end, y_end))
                cropped_image.save('./saved_images/{}.png'.format(time()))

player = FirstPersonController()

floor_texture = load_texture('./grass.jpg')
sky_texture = load_texture('./sky.jpg')

floor = Entity(model='cube', scale_x=100, scale_z=100, texture=floor_texture, collider='box', texture_scale=(50, 50))
sky = Entity(model='sphere', scale=100, collider='mesh', texture=sky_texture, double_sided=True)

app.run()