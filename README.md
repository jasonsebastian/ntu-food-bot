Where's My Food?
----------

### Table of Contents

 1. Introduction
 2. Solution
 3. How it works
 4. Flowcharts
 5. Constraints and limitations
 6. Future Development
 7. Conclusion

## Introduction
### Background
Having a good meal during lunchtime and enjoying the short breaks in the middle of a hectic schedule is a pleasure for everyone, especially NTU students who are asserted to use said time as wise as possible to keep up with the pace of this fast-changing world.

### Problem
With the high amount of tasks and assignments, sometimes going to a canteen to have lunch will be troublesome due to the number of people queuing blocking our way to see the menu. This results in a lot of time lost to only looking at menus and walking around trying to figure out what to eat. Moreover, the various menus and stall choices available in NTU sometimes can be confusing to choose from, especially since there is no reference on hand to know what to expect from said stall. These often makes us end up choosing a random meal and regretting the meal that has been bought or simply going back to the same stall over and over again, which tends to get boring over time. Furthermore, for our muslim peers it is even harder as they do not know which stalls are halal or not.

> #### Why do we care? 
> When every individual can decide quickly which stall they want to buy their food from, the assumption that the time needed to finish their food is the same, the crowd level in the canteen should decrease. Consequently, this will ease the mobility and more seats in the canteen will be available, making others’ movements also faster.

## Solution
### Description
As we can see, the majority of people like to eat the stall's or type of food they are familiar with. In general cases, those who want to try new food is only because they received suggestion from others.

We created a bot named "Where's My Food?", a chat bot in Telegram whose id is '@ntu_food_bot' (case sensitive), which helps people decide what they should eat.

To use this bot, the user needs to download the Telegram app from Play Store or App Store if it has not been installed yet. Then, the user can search for ‘ntu_food_bot’ in Telegram. The bot will then give simple instructions to follow.

The code for this bot is written in Python. The bot will first ask the user whether they want to browse for halal food or non-halal food, then ask which canteen they would prefer to eat at. In return, the bot sends back a list of the food stalls, matching the user’s preferences. Afterwards, the user is prompted to choose which stall to eat at. In return, the bot gives the url that directs the user to the Google Maps Application or Google Maps website with the location of said canteen. The user is asked to rate the stall after eating the meal. The rating provided goes into a database, and it is used to generate the ratings for the next user.

### Source Code
#### Overview

The program is broken down into 1 `python` file, 2 `python` modules and 1 `json` file. The 3 modules are `index.py`, `food.py`, and `ratings.py`. An additional python module `index.py` works as the main program to run the bot. `food.py` consists of some function about in-line keyboard building and processing data. `ratings.py` helps the main program to get data and write data into database. The `json` file mentioned earlier named `data.json` acts as the database. 

#### index.py
`index.py` is the main file which needs to be executed for the bot to run. In the code, the bot is instantiated using 2 classes, `FoodStarter` and `Fooder`. `FoodStarter` is instantiated every time a unique user sends a message to the bot. The instance of `FoodStarter`’s task is to prompt the user to start. Once the user chooses to start, the instance of `FoodStarter` is closed, and the instance of `Fooder` comes into place. The instance of `Fooder` only handles messages sent when the inline keyboard is pressed.

#### food.py
`food.py` helps `index.py` in building the in-line keyboard buttons, retrieving the list of stalls for each canteen and then gives the Google Maps URL search query for locating said canteen.

The first function defined is `no_pref_canteens_kbd`. It takes no parameters and returns the in line keyboard button for all the canteens.

The second function is `halal_canteens_kbd`, which is similar to `no_pref_canteens_kbd`, but it returns the inline keyboard button for only the canteens that have at least one halal food stall.

Next, `get_stalls` takes the user’s halal preference and the name of the canteen that was chosen as parameters then returns the list of stalls that matches the user’s preference. If the user prefers halal food, then it simply checks the canteen’s name using an if - elif chain and returns the stall names as a list. If the user does not have any preferences, it opens `data.json`, then stores the names of the stalls with the keyword `canteen` into the list `stalls`, then returns it.

`build_kbd` helps build the inline keyboard button alignment into an appropriate number of rows and columns. 

Finally, the last function is `get_url`, which returns the URL string of the Google Maps URL search query for each canteen.

#### ratings.py
`ratings.py` helps access and write to `data.json`. The first function is called `get_rating(canteen, stall)`.

```python
def get_rating(canteen, stall):
    with open('/app/bot/data.json', 'r') as file:
        data = json.load(file)
    return data[canteen][stall][0]
```

Then there is also a function called `store_rating(canteen, stall, rating)`. `data.json` only stores the total rating voted and current rating. The number of people is not stored explicitly, but is calculated by the equation
$$ p = \frac{t}{r} $$
where $t$ represents the total number of vote and $r$ as the current rating. To avoid division by 0 error, if $r = 0$, p is simply $0$. Then it writes it into the `json` file.

### How it works
It is probably best if we explain about the concept of flavors.

Regardless of the type of objects received, `telepot` generically calls everything the user sends as “message” (with a lowercase “m”). A message’s flavor depends on the underlying object:
 - a `Message` object gives the flavor **chat**
 - a `CallbackQuery` object gives the flavor **callback_query**

And now, we get to the main theme.

A `DelegatorBot` is able to spawn delegates. The code is spawning `FoodStarter` and `Fooder` per chat id. Then, the bot calls `MessageLoop` which makes the bot to run forever.

There are only two methods inside `FoodStarter`, `on_chat_message` and `on_close`.

`on_chat_message` handles all messages with `chat` flavor, and `on_close` is called when the object is closed.

There are two code blocks worth paying attention to.

```python
if content_type != 'text':
    return
```

This code block checks whether the user sent a text-type message. If not, the code will escape the `on_chat_message` method. 

```python
self.sender.sendMessage(
    'Press START to order some food ...',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text='START', callback_data='start')]
                ]
            )
        )
```

This code block sends *Press START to order some food...* to the user with an inline keyboard, containing a button labeled *START*. Throughout the code, messages along with their respective keyboards will be sent by replacing this first message, which means that there will only be at most one message and one inline keyboard.

Inside `Fooder`, the methods can be categorized into two types: user-defined methods and built-in methods. The latter will be discussed first.

There are 3 built-in methods; `on_callback_query`, `on__idle` and `on_close`.

`on_callback_query`'s task is to handle all messages with `callback_query` flavor, `on__idle` is called when the user is idle for the duration specified in the timeout parameter (line 266), and `on_close`'s method is previously explained.

There are two attributes initialized here, `_user_choice` and `_stage_count`.

`_user_choice` is a list where all of the user's choices will be stored. `_stage_count` is an integer attribute and it indicates the *stage* the user is currently on. *Stage* is different for each different question asked to the user.

In `on_callback_query` method, the code checks if the user has already pressed the *START* button. If so, then `_halal` is called. If the user presses the keyboard from `_halal`, `_stage_count` will increment and the `query_data` will be appended to a list called `_user_choice`. `_stage_count` will continue to increment as the program progresses.

Two exceptions are handled in this method.

```python
if query_data == 'back' and self._user_choice:
    # Make sure that empty list is not being popped.
    self._user_choice.pop()

    self._stage_count -= 1  # Go to the previous stage.
```

The first one is when the user presses the *BACK* button in each stage, as shown on the code above. `_user_choice` will pop its last element and `_stage_count` will decrement.

The second is implicitly written on the code. If the user keeps sending random text messages and presses the *START* button, the keyboard from `_halal` will continue to pop up. In other words, in order to continue the user must press one of the button of the inline keyboard.

Each of the user-defined functions corresponds to one stage, and as previously mentioned, the stages are accessed by evaluating the value of `_stage_count`. The order of the stages can be seen from the code below.

```python
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
```

Also, on every stage, whenever the message needs concatenation operations, the attribute `_msg_sent` is used.

In `_halal`, a keyboard containing *Halal food* and *Everything I eat* is set up. `editor.editMessageText` edits the previous message and keyboard if present. Each of the user-defined method will have this `editor.editMessageText` method, which as previously mentioned, will replace the previous message and send a new one.

Another thing to notice is that the `editor.editMessageText` is always paired with `time.sleep(1)`. An example code would be from line 119-120.

```python
time.sleep(1)
self.editor.editMessageText(self._msg_sent, reply_markup=markup)
```

In `_place`, the code first retrieves keyboard according to the user’s halal preference. This choice is retrieved using the list `_user_choice`.

```python
# Set keyboard according to preference.
if self._user_choice[0] == 'no-pref':
    keyboard = food.no_pref_canteens_kbd()
else:
    keyboard = food.halal_canteens_kbd()
```

In `_stalls`, first the stalls are retrieved from a function which is defined in `food.py`, called `get_stalls`. Then, the code constructs a string on `_msg_sent` where a numbered list of canteens will show up.

```python
for i in range(num_of_stalls):
    rating = ratings.get_rating(canteen, stalls[i])
    stalls_msg += (str(i + 1) + '. ' + stalls[i] + ' ' +
                            (int(rating) * star) + '\n')
```

Ratings are also retrieved from the function `get_ratings` of `food.py`.

In the code, we use emoji to be displayed to the user. The method `emojize` returns an object which contains the emoji specified in its parameter.

```python
star = emojize(':star:', use_aliases=True)
```

An edge case to be taken care of is when there is only one stall that matches the user preferences.

```python
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
```

So, if indeed the displayed stall is only one, `_msg_sent` becomes *So do you want to et at this stall?*, instead of *So which stall looks appetizing?*.
 
In `_rate_taste`, first it retrieves the canteen and stall chosen from the attribute `_user_choice`.

```python
self._msg_sent = 'Here\'s the location of the canteen you chose.\n\n'
self._msg_sent += food.get_url(canteen) + '\n\n'
self._msg_sent += 'Thank you for choosing!\n\n'
```

Here it creates the message that contains the location of the canteen by seeking help from the function `get_url` from `food.py`. Then, question about how the the food taste is appended.

```python
keyboard = [
    [InlineKeyboardButton(text='Yummy :D',
                                        callback_data=4)],
    [InlineKeyboardButton(text='Okay lah',
                                        callback_data=3)],
    [InlineKeyboardButton(text='Not so good',
                                        callback_data=2)]
]
```

The code shown above is how the in-line keyboard button to asks the food taste. The score ranges from 2 - 4. Actually, the scoring system is 1 - 5. The steps from 2 - 4 to 1 - 5 will be explained later.

Then, as the previous methods done, it does `time.sleep(1)` then sends everything.

`_rate_price` is very similar to `_rate_taste`, but the message is simply 'How about the price?' a


#### How to run it locally
To run it on local machines, first you have to create a new bot from BotFather in Telegram and get the token. Download all the file in the `bot` directory, then paste the token you have to `TOKEN` in line 259 of `index.py`. You would not be able to run without changing the token as it will results in webhook error.

The next step is you should install the modules requirements by running

    pip install telepot
    pip install emoji
    pip install httplib2

in command prompt or terminal window.

Then, you should replace all of the `'/app/bot/data.json'` with simply `'data.json'` in `food.py` and `ratings.py`
Then run `index.py`, and try it from Telegram App. 

### Flowcharts
![Flowchart 1](https://lh3.googleusercontent.com/-6LCAV6EDwEA/Wd8PFSS7AZI/AAAAAAAAAdo/YI_wsNZl5_QsDqW4HHaocihdSZU-tRtjgCLcBGAs/s0/FLOWCHART+1+LG.jpg "Flowchart 1")

![enter image description here](https://lh3.googleusercontent.com/-CB2Unpslln0/Wd8PPN_DhbI/AAAAAAAAAdw/VlimIw-Vl0cLajSgP-OhbrGsHHXcojJbwCLcBGAs/s0/FLOWCHART+FINAL.jpg "Flowchart 2")

## Constraints and Limitations
One of the biggest limitations found in this chat bot is that one can spam '/start' to the chat bot and it will let the program to create a great number of instances of the bot class. It may take the system down.

The next limitation is that one can give fake ratings by using our bot repetitively to alter any stall's rate. This is a quite serious problem because if the information given is not reliable, then no one will use the bot.

## Future Development
If we had more time, we would implement a strategy to tackle those constraints stated above. To solve the '/start' spamming problem, one possible way is to check whether this user have already got an instance of bot class or not by analyzing the chat id. Then to solve the fake ratings problem, it may be done by record users’ voting history, to let the user vote only after some period of time after the preceding vote.

## Conclusion
Deciding what to eat may be annoying sometimes. Often we doubt stall's food. Moreover for our Muslim peers, they have to know which stall are halal. Therefore, 'Where's My Food?' chatbot helps to choose food based on your halal and canteen preferences, with live time ratings given by preceding users. It surely has some constraints and limitation, but with certain development it should be able to serve better.
