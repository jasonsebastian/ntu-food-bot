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
`index.py` is the main file which needs to be executed for the bot to run. In the code, the bot is instantiated using 2 classes, `FoodStarter` and `Fooder`. `FoodStarter` is instantiated every time a unique user sends a message to the bot. The instance of `FoodStarter`’s task is to prompt the user to start. Once the user chooses to start, the instance of `FoodStarter` is closed, and the instance of `Fooder` comes in to place. The instance of `Fooder` only handles messages sent when the inline keyboard is pressed.

#### food.py
`food.py` helps `index.py` in building in-line keyboard buttons, retrieving the list of stalls for each canteen and gives the url of Google Maps search query for searching canteen location.

The first function defined are `no_pref_canteens_kbd()`. It takes no parameter and returns the in line keyboard button for all the canteens.

The second function is `halal_canteens_kbd()` which function is similar with `no_pref_canteens_kbd()`, but it just returns the in-line keyboard button for canteens that have at least one halal food stall.

Then, `get_stalls()` takes halal preference and the name of the canteen that were chosen by the user as parameters, then it returns the list of stalls that matches the user preference. If the user prefers halal food, then it simply check the canteen name using if - elif chain, than returns the stall names as list. If the user does not have any preference, it opens `data.json`, then store the name of stalls with the keyword `canteen` into list `stalls`, then return it.

`build_kbd(stalls)` helps to build inline keyboard button alignment into appropriate rows and columns. 

Then the last function is `get_url(canteen)` that returns the URL string of the Google Maps URL search query for each canteen.

#### ratings.py
`ratings.py` helps to access and write to `data.json`. The first function is called `get_rating(canteen, stall)`.
```python
def get_rating(canteen, stall):
    with open('/app/bot/data.json', 'r') as file:
        data = json.load(file)
    return data[canteen][stall][0]
```
Then there is also a function called `store_rating(canteen, stall, rating)`. `data.json` only stores the total rating voted and current rating. The number of people is not stored explicitly, so here it is calculated by the equation
$$ p = \frac{t}{r} $$
which $t$ represents the total number of vote and $r$ as the current rating. To avoid division by 0 error, if $r = 0$, p is simply $0$. Then it writes it into the `json` file.

### How it works
It is probably best if we explain about the concept of flavors.

Regardless of the type of objects received, `telepot` generically calls everything the user sends as “message” (with a lowercase “m”). A message’s flavor depends on the underlying object:
 - a Message object gives the flavor `chat`
 - a CallbackQuery object gives the flavor `callback_query`

A `DelegatorBot` is able to spawn delegates. The code is spawning `FoodStarter` and `Fooder` per chat id. Then, the bot calls `MessageLoop` which makes the bot to run forever.

Inside `FoodStarter`, there are two code blocks worth paying attention to.
```python
if content_type != 'text':
	return
```
This code block checks whether the user sent a text-type message. If not, the code will escape the `on_chat_message` function. 
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
This code block sends ‘Press START to order some food…” to the user with an inline keyboard, containing a button labeled ‘START’. Throughout the code, messages along with their respective keyboards will be sent by replacing this first message.

Inside `Fooder`, the functions can be categorized into 2: user-defined functions and built-in functions. The latter will be discussed first.

There are 3 built-in functions; `on_callback_query`, `on__idle` and `on_close`. `on_callback_query`'s task is to handle 

#### How to run it locally
To run it on local machine, first you have to create a new bot from BotFather in Telegram and get the token. Download all the file in the `bot` directory, then paste the token you have to `TOKEN` in line 271 of `index.py`. You would not be able to run without changing the token as it will results in webhook error.

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
