import json


def get_rating(canteen, stall):
    with open('/app/bot/data.json', 'r') as file:
        data = json.load(file)
    return data[canteen][stall][0]


def store_rating(canteen, stall, rating):
    with open('/app/bot/data.json', 'r') as file:
        data = json.load(file)

    acc_rating = data[canteen][stall][1]
    avg_rating = data[canteen][stall][0]

    if acc_rating == 0:
        n = 1
    else:
        n = acc_rating / avg_rating
        n += 1

    acc_rating += rating
    avg_rating = acc_rating / n

    data[canteen][stall][0] = avg_rating
    data[canteen][stall][1] = acc_rating

    with open('/app/bot/data.json', 'w') as file:
        json.dump(data, file)
