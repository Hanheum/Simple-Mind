import tensorflow as tf
import numpy as np
from pyautogui import screenshot
from ursina import *
import random

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
            cropped_image = np.array(cropped_image)
            cropped_image = np.expand_dims(cropped_image, axis=0)

            interpreter.set_tensor(input_details[0]['index'], cropped_image)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            output_data2 = np.argmax(output_data)
            if output_data2 == 0:
                positives.append((a, b))
                possibilities.append(output_data[0][0])

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
    print('go to food')

def eat():
    print('eat')

def random_movement():
    print('random movement')

live = True
while live:
    sight = see()
    food_location = find_food(sight)
    if food_location != False:
        go_to_food(Vec3(0, 0, 0), Vec3(0, 0, 0))          #my position and food position
        eat()
        good_or_bad = random.randint(0, 1)
        if good_or_bad == 0:
            happiness -= 1
        else:
            happiness += 1
    else:
        random_movement()

    count2 += 1
    if count == count2:
        count2 = 0
        if happiness >= 0:
            if happiness>5:
                will_to_live += 1
        else:
            will_to_live -= 1
            if will_to_live <= 0:
                live = False