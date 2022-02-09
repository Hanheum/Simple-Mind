import tensorflow as tf
import numpy as np
from pyautogui import screenshot
from ursina import *
import random
from threading import Thread
from time import time, sleep
from math import atan, degrees

model_path = './mind_AI.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

will_to_live = 10
happiness = 0
count = 10
count2 = 0

def see():
    screen = screenshot()
    x_start = 256
    y_start = 144
    x_end = 2304
    y_end = 1152
    screen_crop = screen.crop((x_start, y_start, x_end, y_end))
    return screen_crop

def find_food(image):
    image = image.resize((700, 700))
    positives = []
    possibilities = []
    for a in range(7):
        for b in range(7):
            x_start = a*100
            y_start = b*100
            x_end = x_start+100
            y_end = y_start+100
            cropped_image = image.crop((x_start, y_start, x_end, y_end))
            saving_image = cropped_image.copy()
            cropped_image = cropped_image.resize((100, 100))
            cropped_image = np.array(cropped_image)
            cropped_image = np.expand_dims(cropped_image, axis=0)

            interpreter.set_tensor(input_details[0]['index'], cropped_image.astype(np.float32))
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            output_data2 = np.argmax(output_data)
            if output_data2 == 0:
                positives.append((a, b))
                possibilities.append(output_data[0][0])
                saving_image.save('./saved_images/{}.png'.format(time()))

    if len(positives) == 0:
        return False
    else:
        biggest = max(possibilities)
        biggest_index = possibilities.index(biggest)
        the_one = positives[biggest_index]
        px = 100*the_one[0]+50
        py = 100*the_one[1]+50
        x = (2048/700)*px
        y = (1152/700)*py
        position = (x, y)
        return position

def go_to_food(my_position, food_position):
    try:
        one_step_x = (food_position.x - my_position.x) / 100
        one_step_z = (food_position.z - my_position.z) / 100

        rotation = degrees(atan((food_position.x - my_position.x) / (food_position.z - my_position.z)))
        creature.world_rotation = Vec3(0, rotation, 0)

        for i in range(100):
            creature.world_position = Vec3(my_position.x + one_step_x * i, 1, my_position.z + one_step_z * i)
            sleep(0.02)
    except:
        pass

def eat():
    print('eatting food')

def random_movement():
    next_move = random.randint(0, 9)
    if next_move != 9:
        creature.world_rotation += (0, 10, 0)
    else:
        position = get_random_position()
        go_to_food(creature.world_position, position)

class food(Entity):
    def __init__(self, model, color, position):
        super().__init__(
            model=model,
            color=color,
            position=position,
            collider='mesh'
        )

def get_random_position():
    x = random.randint(-25, 25)
    z = random.randint(-25, 25)
    position = Vec3(x, 1, z)
    return position

app = Ursina()

creature = Entity(model='cube', color=color.white, collider='box', position=Vec3(0, 1, 0), rotation=Vec3(0, 0, 0))

start_time = time()
new_food = food(model='sphere', color=color.yellow, position=get_random_position())

def update():
    global start_time, new_food

    camera.world_position = creature.world_position+Vec3(0, 1, 0)
    camera.world_rotation = creature.world_rotation

    present_time = time()
    if present_time-start_time > 10:
        new_food = food(model='sphere', color=color.yellow, position=get_random_position())
        start_time = present_time

def mind():
    global happiness, will_to_live, count2
    live = True
    while live:
        sight = see()
        food_location = find_food(sight)
        if food_location != False:
            go_to_food(creature.world_position, new_food.world_position)
            eat()
            good_or_bad = random.randint(0, 1)
            if good_or_bad == 0:
                happiness -= 1
            else:
                happiness += 1
        else:
            random_movement()

        print('happiness:{}\nwill to live:{}'.format(happiness, will_to_live))

        count2 += 1
        if count == count2:
            count2 = 0
            if happiness >= 0:
                if happiness > 5:
                    will_to_live += 1
            else:
                will_to_live -= 1
                if will_to_live <= 0:
                    live = False
                    print('dead')

mind_thread = Thread(target=mind)
mind_thread.start()

floor_texture = load_texture('./grass.jpg')
sky_texture = load_texture('./sky.jpg')
floor = Entity(model='cube', scale_x = 100, scale_z = 100, texture=floor_texture, texture_scale=(50, 50), collider='box')
sky = Entity(model='sphere', scale=100, collider='mesh', texture=sky_texture, double_sided=True)

app.run()