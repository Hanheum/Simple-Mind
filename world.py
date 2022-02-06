from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
from time import time
import pyautogui

image_name = input('image name:')
code_start_time = time()

models = [load_model('banana.obj')]
colors = [color.yellow]
foods = []
positions = []

class food(Entity):
    def __init__(self, model, color, position):
        super().__init__(
            model=model,
            color=color,
            position=position,
            collider=mesh,
            scale=0.01
        )

def get_random_position():
    x = random.randint(-25, 25)
    z = random.randint(-25, 25)
    position = Vec3(x, 1, z)
    return position

app = Ursina()

start_time = time()
new_food_index = random.randint(0, int(len(models) - 1))
new_food = food(model=models[new_food_index], color=colors[new_food_index], position=get_random_position())

def update():
    global start_time, new_food, new_food_index
    present_time = time()
    '''if present_time-start_time > 60:
        new_food_index = random.randint(0, int(len(models)-1))
        new_food = food(model=models[new_food_index], color=colors[new_food_index], position=get_random_position())
        start_time = present_time'''

    if held_keys['g']:
        screen_shot = pyautogui.screenshot()
        screen_shot.save('D:\\PycharmProjects\\Mind\\mind_dataset\\no_food\\'+image_name+'{}.jpg'.format(round(time()-code_start_time, 3)))

player = FirstPersonController()

floor_texture = load_texture('./grass.jpg')
sky_texture = load_texture('./sky.jpg')

floor = Entity(model='cube', scale_x=100, scale_z=100, texture=floor_texture, collider='box', texture_scale=(50, 50))
sky = Entity(model='sphere', scale=100, collider='mesh', texture=sky_texture, double_sided=True)

app.run()