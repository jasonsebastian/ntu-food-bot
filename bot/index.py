import sys
import time
import telepot
import telepot.helper
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)
import food
import ratings
from emoji import emojize

"""
index.py

Send a chat message to the bot. It will ask several questions
to know your preferences, and then gives back a list of canteens.
"""


class FoodStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(FoodStarter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        '''Handles chat message sent from user.'''
        content_type, chat_type, chat_id = telepot.glance(msg)
        self._received_msg = msg['text']

        '''Do nothing if message sent is not a text.'''
        if content_type != 'text':
            return

        # For debugging purposes.
        print('chat [' + content_type + ', ' + chat_type +
              ', ' + str(chat_id) + ']')

        self.sender.sendMessage(
            'Press START to order some food ...',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                            text='START', callback_data='start')]
                    ]
            )
        )
        self.close()  # let Fooder take over

    def on_close(self, ex):
        pass


class Fooder(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(Fooder, self).__init__(*args, **kwargs)

        self._user_choice = []
        self._stage_count = 0

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(
                                            msg, flavor='callback_query')

        if query_data != 'start':

            if query_data == 'back' and self._user_choice:
                # Make sure that empty list is not being popped.
                self._user_choice.pop()

                self._stage_count -= 1  # Go to the previous stage.

            else:
                # Add user's choice to user_choice list.
                self._user_choice.append(query_data)
                self._stage_count += 1

            # For debugging purposes.
            print('callback_query [' + str(query_id) + ', ' +
                  str(from_id) + ', ' + query_data + ']')

        # Go to function according to self._stage_count.
        if self._stage_count == 0:
            self._halal()
        elif self._stage_count == 1:
            self._place()
        elif self._stage_count == 2:
            self._stalls()
        elif self._stage_count == 3:
            self._rate_taste()
        elif self._stage_count == 4:
            self._rate_price()
        elif self._stage_count == 5:
            self._thank_you()

        # For debugging purposes.
        print(self._user_choice)
        print('stage_count =', self._stage_count)
        print('no_kbd =', self._no_kbd)

    def _halal(self):
        '''Ask if user wants halal or veggie food.'''

        smiling_imp = emojize(':smiling_imp:', use_aliases=True)
        keyboard = [
            [InlineKeyboardButton(
                text='Halal food',
                callback_data='halal')],
            [InlineKeyboardButton(
                text=('Everything I eat ' + smiling_imp),
                callback_data='no-pref')]
        ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        self._msg_sent = (
            'Hello, I\'m here to help you find your food!\n\n')
        self._msg_sent += 'Do you have any food preference?'

        time.sleep(1)
        self.editor.editMessageText(self._msg_sent, reply_markup=markup)

    def _place(self):
        '''Ask the user where to eat.'''

        # Set keyboard according to preference.
        if self._user_choice[0] == 'no-pref':
            keyboard = food.no_pref_canteens_kbd()
        else:
            keyboard = food.halal_canteens_kbd()

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        time.sleep(1)
        self.editor.editMessageText(
            'Where do you want to eat?', reply_markup=markup)

    def _stalls(self):
        '''Display the stalls in the canteen preferred by the user.'''

        halal_pref = self._user_choice[0]
        canteen = self._user_choice[1]
        stalls = food.get_stalls(halal_pref, canteen)

        self._msg_sent = (
            'Here is the list of available stalls in ' +
            canteen + ', based on your preference.\n\n')

        stalls_msg = ''
        num_of_stalls = len(stalls)
        star = emojize(':star:', use_aliases=True)

        for i in range(num_of_stalls):
            rating = ratings.get_rating(canteen, stalls[i])
            stalls_msg += (str(i + 1) + '. ' + stalls[i] + ' ' +
                           (int(rating) * star) + '\n')

        self._msg_sent += stalls_msg + '\n'

        if num_of_stalls != 1:
            keyboard = food.build_kbd(stalls)
            self._msg_sent += 'So which stall looks appetizing?'
        else:
            keyboard = [
                [InlineKeyboardButton(text='Yes',
                                      callback_data=stalls[0])],
                [InlineKeyboardButton(text='No',
                                      callback_data='back')]
            ]
            self._msg_sent += 'So do you want to eat at this stall?'

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        time.sleep(1)
        self.editor.editMessageText(self._msg_sent, reply_markup=markup)

    def _rate_taste(self):
        canteen = self._user_choice[1]
        stalls = self._user_choice[2]

        self._msg_sent = 'Here\'s the location of the canteen you chose.\n\n'
        self._msg_sent += food.get_url(canteen) + '\n\n'
        self._msg_sent += 'Thank you for choosing!\n\n'

        halal_pref = self._user_choice[0]
        stalls = self._user_choice[2]

        self._msg_sent += ('You choosed ' + stalls +
                           ', please enjoy your meal.\n\n' +
                           'How\'s the taste?')

        keyboard = [
            [InlineKeyboardButton(text='Yummy :D',
                                  callback_data=4)],
            [InlineKeyboardButton(text='Okay lah',
                                  callback_data=3)],
            [InlineKeyboardButton(text='Not so good',
                                  callback_data=2)]
            ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        time.sleep(1)
        self.editor.editMessageText(self._msg_sent, reply_markup=markup)

    def _rate_price(self):

        halal_pref = self._user_choice[0]
        canteen = self._user_choice[1]
        stalls = self._user_choice[2]

        keyboard = [
            [InlineKeyboardButton(text='Worth it!',
                                  callback_data=1)],
            [InlineKeyboardButton(text='Fair lah',
                                  callback_data=0)],
            [InlineKeyboardButton(text='Walaweee :(',
                                  callback_data=-1)]
            ]

        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

        time.sleep(1)
        self.editor.editMessageText(
            'How about the price?', reply_markup=markup)

    def _thank_you(self):

        self._msg_sent = 'Thank you for rating and using our bot!\n\n'
        self._msg_sent += 'This message will disappear in 20 seconds.'

        canteen = self._user_choice[1]
        stalls = self._user_choice[2]
        taste = self._user_choice[3]
        price = self._user_choice[4]

        previous = ratings.get_rating(canteen, stalls)
        ratings.store_rating(canteen, stalls, int(taste) + int(price))
        now = ratings.get_rating(canteen, stalls)

        # For debugging purposes.
        print('Stored the rating, previous was = ', previous,
              ' now is = ', now)

        time.sleep(1)
        self.editor.editMessageText(self._msg_sent, reply_markup=None)

        time.sleep(20)
        self.editor.deleteMessage()
        self.close()

    def on__idle(self, event):
        '''Handles the bot when user is idle for 30 seconds.'''
        pass

    def on_close(self, ex):
        pass


if __name__ == '__main__':
    TOKEN = '425956090:AAFzuvErNrhomansNwzid3u0wr8oYtLhaxU'

    bot = telepot.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, FoodStarter, timeout=3),
        pave_event_space()(
            per_callback_query_origin(), create_open, Fooder, timeout=30),
    ])
    MessageLoop(bot).run_as_thread()
    print('Listening ...')

    # Keep the program running.
    while True:
        time.sleep(10)
