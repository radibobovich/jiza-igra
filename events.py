import random


# def events(a):
#     eval(a[random.randrange(0, len(a))])()


def uronil():
    return {'output': 'Вы уронили котлету. Штраф 200 рублей.', 'deltabalance': -200}


def podnal():
    return {'output': 'Вы подняли бабла. +300 рублей.', 'deltabalance': 300}