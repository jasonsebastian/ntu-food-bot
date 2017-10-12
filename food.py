import math
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import json


def no_pref_canteens_kbd():
    kbd = [
            [InlineKeyboardButton(text='Canteen 1',
                                  callback_data='Canteen 1'),
             InlineKeyboardButton(text='Canteen 2',
                                  callback_data='Canteen 2')],
            [InlineKeyboardButton(text='Canteen 4',
                                  callback_data='Canteen 4'),
             InlineKeyboardButton(text='Canteen 9',
                                  callback_data='Canteen 9')],
            [InlineKeyboardButton(text='Canteen 11',
                                  callback_data='Canteen 11'),
             InlineKeyboardButton(text='Canteen 13',
                                  callback_data='Canteen 13')],
            [InlineKeyboardButton(text='Canteen 14',
                                  callback_data='Canteen 14'),
             InlineKeyboardButton(text='Canteen 16',
                                  callback_data='Canteen 16')],
            [InlineKeyboardButton(text='Canteen A',
                                  callback_data='Canteen A'),
             InlineKeyboardButton(text='Canteen B',
                                  callback_data='Canteen B')],
            [InlineKeyboardButton(text='North Hill Canteen',
                                  callback_data='North Hill Canteen')],
            [InlineKeyboardButton(text='Go back.',
                                  callback_data='back')]
          ]
    return kbd


def halal_canteens_kbd():
    kbd = [
            [InlineKeyboardButton(text='Canteen 2',
                                  callback_data='Canteen 2'),
             InlineKeyboardButton(text='Canteen 9',
                                  callback_data='Canteen 9')],
            [InlineKeyboardButton(text='Canteen 11',
                                  callback_data='Canteen 11'),
             InlineKeyboardButton(text='Canteen 16',
                                  callback_data='Canteen 16')],
            [InlineKeyboardButton(text='Canteen A',
                                  callback_data='Canteen A'),
             InlineKeyboardButton(text='Canteen B',
                                  callback_data='Canteen B')],
            [InlineKeyboardButton(text='North Hill Canteen',
                                  callback_data='North Hill Canteen')],
            [InlineKeyboardButton(text='Go back.',
                                  callback_data='back')]
          ]

    return kbd


def get_stalls(halal_pref, canteen):

    if halal_pref == 'halal':
        if canteen == 'Canteen 2':
            stalls = ['Ayam Penyet']
        elif canteen == 'Canteen 9':
            stalls = ['Indian']
        elif canteen == 'Canteen 11':
            stalls = ['Indian Food']
        elif canteen == 'Canteen 16':
            stalls = ['Indian Food']
        elif canteen == 'Canteen A':
            stalls = ['Malay BBQ', 'Indian Cuisine']
        elif canteen == 'Canteen B':
            stalls = ['Nasi Padang', 'Ban Mian & Fish Soup',
                      'Indian Cuisine', 'Yong Tau Foo']
        elif canteen == 'North Hill Canteen':
            stalls = ['Noor Anisha\'s Nasi Padang']
        else:
            stalls = ['Indian']
    else:
        with open('/app/bot/data.json', 'r') as file:
            data = json.load(file)
        data = data[canteen]
        stalls = []
        for word in data:
            stalls.append(word)
    return stalls


def build_kbd(stalls):
    '''Build the inline keyboard.'''
    kbd_row = []
    kbd = []
    num_of_cells = len(stalls)
    index = 1

    div_three = num_of_cells % 3  # 1
    div_four = num_of_cells % 4  # 3
    div_five = num_of_cells % 5  # 2

    if div_three == 0:
        col = 3
    elif div_four == 0:
        col = 4
    elif div_five == 0:
        col = 5
    else:
        div = [3 - div_three, 4 - div_four, 5 - div_five]  # [2, 1, 3]
        div.sort()
        if div[0] == 4 - div_four:
            col = 4
        elif div[0] == 3 - div_three:
            col = 3
        else:
            col = 5

    # Set the ideal number of rows and columns.
    if num_of_cells % 3 == 0:
        col = 3
    elif num_of_cells % 4 == 0:
        col = 4
    else:
        col = 5

    for rows in range(math.ceil(num_of_cells / col)):
        if num_of_cells >= col:
            for i in range(col):
                kbd_row.append(
                    InlineKeyboardButton(text=str(index),
                                         callback_data=stalls[index - 1])
                    )
                index += 1
            kbd.append(kbd_row)
            kbd_row = []
            num_of_cells -= col
        else:
            for i in range(num_of_cells):
                kbd_row.append(
                    InlineKeyboardButton(text=str(index),
                                         callback_data=stalls[index - 1])
                    )
                index += 1
            kbd.append(kbd_row)

    kbd.append([InlineKeyboardButton(
                    text='Not interested.',
                    callback_data='back')])

    return kbd


def get_url(canteen):
    addresses = {
        'Canteen 1': 'Canteen+1,+21+Nanyang+Cir',
        'Canteen 2': 'Food+Court+2,+35+Students+Walk',
        'Canteen 4': 'NTU+Canteen+4,+10+Nanyang+Drive',
        'Canteen 9': 'Canteen+9,+24+Nanyang+Ave',
        'Canteen 11': 'Food+Court+11,+20+Nanyang+Ave',
        'Canteen 13': 'Food+Court+13,+32+Nanyang+Cres',
        'Canteen 14': 'Canteen+14,+34+Nanyang+Cres',
        'Canteen 16': 'Food+Court+16,+50+Nanyang+Walk',
        'Canteen A': 'North+Spine+Food+Court,+76+Nanyang+Drive',
        'Canteen B': 'Koufu+@+the+South+Spine,+Nanyang+Link',
        'North Hill Canteen': 'North+Hill+Food+Court+64+Nanyang+Cres'
    }

    location_url = ('https://www.google.com/maps/search/?api=1&query=' +
                    addresses[canteen])

    return location_url
