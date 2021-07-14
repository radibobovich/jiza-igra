import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import datetime
from datetime import timedelta
import random
from events import *
random.seed(None)
rand = random.Random()
root = Tk()
# окно
root.iconbitmap('icons/icon.ico')
root['bg'] = 'snow'
root.title('Жиза-игра')
root.wm_attributes('-alpha', 1)
root.geometry('640x480')
root.resizable(width=False, height=False)


health = 100
food = 100
rest = 100
balance = 2500
date = datetime.datetime(2020, 5, 17)
balanceVar = StringVar()
balanceVar.set(balance)
workid = ''


class Work: # class of work types to carry individual salary etc.
    def __init__(self, workType, id, deltabalance, deltafood, deltarest, randomevents):
        self.workType = workType
        self.id = id
        self.deltabalance = deltabalance
        self.deltafood = deltafood
        self.deltarest = deltarest
        self.randomevents = randomevents
    def dowork(self):
        global food, rest, balance, workid
        if checkstats(deltafood=self.deltafood, deltarest=self.deltarest):
            #eval(self.randomevents[rand.randrange(0, len(self.randomevents))])()
            #events(self.randomevents)
            #event = events.events(self.randomevents)
            if random.random() > 0.8:
                event = eval(self.randomevents[random.randrange(0, len(self.randomevents))])() # event is a variable that contains info about random event. It's a dictionary
            textprint(event['output'])
            balance += event['deltabalance']
            textprint('Вы поработали.')
            food += self.deltafood
            rest += self.deltarest
            balance += self.deltabalance
            refresh()

# a lot of random events
# mcdonalds
# def uronil():
#     textprint('аааа уронили уронили')
# def podnal():
#      textprint('ааа подняли')
# def obosralsya():
#     textprint('пахнет говном')
# def zasmeyalsya():
#      textprint('ржомба лмао')

mcdonalds = Work(workType='Макдональдс', id='mcdonalds', deltabalance=600, deltafood=-10, deltarest=-50, randomevents=['uronil', 'podnal'])
dns = Work(workType='DNS', id='dns', deltabalance=500, deltafood=-20, deltarest=-40, randomevents=['obosralsya', 'zasmeyalsya'])
courier = Work(workType='Курьер', id='courier', deltabalance=800, deltafood=-40, deltarest=-50, randomevents=[])
cladman = Work(workType='Кладмен', id='cladman', deltabalance=5000, deltafood=-40, deltarest=-60, randomevents=[])
cassir = Work(workType='Кассир', id='cassir', deltabalance = 800, deltafood=-50, deltarest=-70, randomevents=[])
worksmas = [mcdonalds, dns, courier, cladman]

# functions


def resetbtns():
    Btn1.configure(text='-', command=NONE)
    Btn2.configure(text='-', command=NONE)
    Btn3.configure(text='-', command=NONE)
    Btn4.configure(text='-', command=NONE)


def setwork():
    global workid
    if listBox.curselection() == (): # exception if user didn't selected work
        messagebox.showinfo(title='Подсказка', message='Выберите работу из списка справа')
    else:
        workid = worksmas[listBox.curselection()[0]].id
        textprint('Теперь ваша работа - ' + eval(workid).workType)
        listBox.delete(0, 'end')
        resetbtns()
        Btn1.configure(text=eval(workid).workType, command=eval(workid).dowork)
        Btn2.configure(text='Сменить работу', command=changework)

def changework():
    textprint('Выберите работу из списка. ')
    for i in range(len(worksmas)): # fills listBox with works
        listBox.insert(i, worksmas[i].workType)
    Btn1.configure(text='Ок', command=setwork)


def dowork():
    global balance, food, rest
    eval(workid).dowork()


def work():
    resetbtns()
    listBox.delete(0, 'end')
    if workid == '':
        changework()
    else:
        Btn1.configure(text=eval(workid).workType, command=eval(workid).dowork)
        Btn2.configure(text='Сменить работу', command=changework)



class Food:

    """
    Class of food types to carry different prices etc.
    """

    def __init__(self, name, id, deltabalance, deltafood):
        self.name = name
        self.id = id
        self.deltabalance = deltabalance
        self.deltafood = deltafood
    def eat(self):
        global balance, food
        if checkstats(deltabalance=self.deltabalance, deltafood=self.deltafood):
            balance += self.deltabalance
            textprint('Вы поели. Сытость: ' + str(food))
            refresh()


sandwich = Food('Бутерброд (30) (+10)', 'sandwich', -30, 10)
pelmeni = Food('Пельмени (140) (+50)', 'pelmeni', -140, 50)
chebupeli = Food('Чебупели (80) (+35)', 'chebupeli', -80, 35)
foodmas = [sandwich, pelmeni, chebupeli]


def choosefood(): # called when the eat button pressed
    resetbtns()
    listBox.delete(0, 'end')
    textprint('Выберите, чем подкрепиться. ')
    for i in range(len(foodmas)):
        listBox.insert(i, foodmas[i].name)
    Btn1.configure(text='Ок', command=choosefoodok)


def choosefoodok(): # called when the OK button pressed
    global balance
    if listBox.curselection() == ():
        messagebox.showinfo(title='Подсказка', message='Выберите еду из списка справа')
    else:
        selectionindex = listBox.curselection()[0]
        eval(foodmas[selectionindex].id).eat()


def sleep(): # called when the sleep button pressed
    global food
    if checkstats(deltafood=-10, alert=False):
        food -= 10
    else:
        if checkstats(deltahealth=-10) == 'death':
            death('hungry')
            return None
    checkstats(deltarest=1000)
    nextday()


def nextday(): # called when sleep called and player didn't died
    global date, rest, food, health, balance
    date += timedelta(days=1)
    print(date.strftime('%d'))
    if date.strftime('%d') == '01':
        if checkstats(deltabalance=-15000, alert=False):
            print('квартплата')
            textprint('Квартплата! -15000')
            balance -= 15000
        else:
            print('умер')
            death('bankrupt')
    refresh()
    textprint('Утро ' + formatdate(date))

#def commonskills():


#def workskills():
    #for i in range())

class Study:
    def __init__(self, name, id, mp_balance=0, mp_food=0, mp_rest=0, cost=0):
        self.name = name
        self.id = id
        self.mp_balance = balance
        self.mp_food = food
        self.mp_rest = rest

#skillbox = Study(name='Курсы программирования', id=skillbox, type)
def study(): # called when the Study button pressed
    resetbtns()
    #Act1.configure(text='Навыки', command=commonskills)
    #Act2.configure(text='Профнавыки', command=workskills)
    #textprint('У вас в стране нет образования, вы живете в Руанде.')


# buttons
Act1 = Button(root, text='Работа', command=work)
Act1.place(relx=0.017, rely=0.023, height=25, width=90)
Act2 = Button(root, text='Учёба', command=study)
Act2.place(relx=0.183, rely=0.023, height=25, width=90)
Act3 = Button(root, text='Еда', command=choosefood)
Act3.place(relx=0.35, rely=0.023, height=25, width=90)
Act4 = Button(root, text='Сон', command=sleep)
Act4.place(relx=0.517, rely=0.023, height=25, width=90)
Btn1 = Button(root, text='-')
Btn1.place(relx=0.017, rely=0.113, height=25, width=90)
Btn2 = Button(root, text='-')
Btn2.place(relx=0.183, rely=0.113, height=25, width=90)
Btn3 = Button(root, text='-')
Btn3.place(relx=0.35, rely=0.113, height=25, width=90)
Btn4 = Button(root, text='-')
Btn4.place(relx=0.517, rely=0.113, height=25, width=90)

# stat bars
healthVar = IntVar()
healthVar.set(health)
healthBar = Progressbar(root, length='120', variable=healthVar)
healthBar.place(relx=0.05, rely=0.91, relwidth=0.201, relheight=0.0, height=22)
foodVar = IntVar()
foodVar.set(food)
foodBar = Progressbar(root, length='120', variable=foodVar)
foodBar.place(relx=0.299, rely=0.91, relwidth=0.201, relheight=0.0, height=22)
restVar = IntVar()
restVar.set(rest)
restBar = Progressbar(root, length='120', variable=restVar)
restBar.place(relx=0.55, rely=0.91, relwidth=0.201, relheight=0.0, height=22)
# images for stats
healthCanvas = Canvas(root)
healthCanvas.place(relx=0.017, rely=0.91, relheight=0.051, relwidth=0.038)
healthIcon = ImageTk.PhotoImage(Image.open('icons/health-icon.png'))
healthCanvas.create_image(2, 2, anchor=NW, image=healthIcon)

foodCanvas = Canvas(root)
foodCanvas.place(relx=0.266, rely=0.91, relheight=0.051, relwidth=0.038)
foodIcon = ImageTk.PhotoImage(Image.open('icons/food-icon.png'))
foodCanvas.create_image(2, 2, anchor=NW, image=foodIcon)

restCanvas = Canvas(root)
restCanvas.place(relx=0.517, rely=0.91, relheight=0.051, relwidth=0.038)
restIcon = ImageTk.PhotoImage(Image.open('icons/rest-icon.png'))
restCanvas.create_image(2, 2, anchor=NW, image=restIcon)


textBox = Text(root, state='disabled') # the box that shows all in-game messages
textBox.place(relx=0.017, rely=0.267, relheight=0.54, relwidth=0.74)

inputText = Entry(root) # not used actually
inputText.place(relx=0.016, rely=0.848, height=20, relwidth=0.633)
BtnInput = Button(root, text='Ок')
BtnInput.place(relx=0.668, rely=0.844, height=24, width=57)

Separator1 = ttk.Separator(root) # cosmetics
Separator1.place(relx=0.016, rely=0.223,  relwidth=0.97)

balanceText = Message(root, textvariable=balanceVar, width=200) # shows balance
balanceText.place(relx=0.831, rely=0.915, relheight=0.051, relwidth=0.141)
balanceCanvas = Canvas(root)
balanceCanvas.place(relx=0.815, rely=0.915, relheight=0.051, relwidth=0.038)
balanceIcon = ImageTk.PhotoImage(Image.open('icons/balance-icon.png'))
balanceCanvas.create_image(2, 2, anchor=NW, image=balanceIcon)

dateVar = StringVar() # tkinter variable to use in date widget
dateVar.set(date.strftime("%d")+'.'+date.strftime("%m")+'.'+date.strftime("%Y"))
dateText = Message(root, textvariable=dateVar, width=100) # shows current date
dateText.place(relx=0.815, rely=0.87, relheight=0.051, relwidth=0.157)
listBox = Listbox(root)
listBox.place(relx=0.768, rely=0.269, relheight=0.538, relwidth=0.21)

BtnSave = Button(root, text='Сохранение')
BtnSave.place(relx=0.831, rely=0.113, height=24, width=97)


def formatdate(date):

    """
    Converts Python date to string date in format dd.mm.yyyy .
    :param date: Date in Python date format
    """

    return date.strftime("%d")+'.'+date.strftime("%m")+'.'+date.strftime("%Y")


def textprint(text):  # функция для корректного вывода текста в TextBox

    """
    Prints something in the textBox.
    :param text: text that you need to print in. Should be a string.
    """

    textBox.configure(state='normal')
    textBox.insert(tkinter.END, '\n' + text)
    textBox.configure(state='disabled')
    textBox.see('end')


def start():
    global health, food, rest, balance, date, workid
    health = 100
    food = 100
    rest = 100
    balance = 2500
    workid = ''
    date = datetime.datetime(2020, 5, 17)
    textBox.configure(state='normal')
    textBox.insert(tkinter.END, 'Жиза-игра v0.2 Alpha')
    textBox.configure(state='disabled')
    nextday()


def refresh():
    """
    Refreshes all visual bars and texts.
    """
    dateVar.set(date.strftime("%d") + '.' + date.strftime("%m") + '.' + date.strftime("%Y"))
    healthVar.set(health)
    foodVar.set(food)
    restVar.set(rest)
    balanceVar.set(balance)


def death(type):
    if type == 'hungry':
        textprint('Вы умерли. Причина: голод\n')
    elif type == 'bankrupt':
        textprint('Вас выселили из квартиры. Игра закончена\n')
    else:
        print('игра говно')
    start()


def checkstats(deltafood=0, deltarest=0, deltabalance=0, deltahealth=0, alert=True):

    """
    Checking can action be done depending on the current stats and values required.
    Also can limit stats to their max if you want to up some stats
    :param alert: if False, function don't print a reason why this actions cannot be done. Default is True
    :return: True if action can be done and False if not
    """

    global health, food, rest, balance
    maxhealth, maxfood, maxrest = 100, 100, 100
    if health + deltahealth < 0:
        return 'death'
    else:
        health += deltahealth
    if food + deltafood < 0 and alert:
        textprint('Вы слишком голодны для этого действия.')
        textprint('Требуется сытости: '+ str(abs(deltafood)) + ', ваша сытость: ' + str(food))
    if rest + deltarest < 0 and alert:
        textprint('Вы слишком устали для этого действия.')
        textprint('Требуется бодрости: ' + str(abs(deltarest)) + ', ваша бодрость: '+ str(rest))
    if balance + deltabalance < 0 and alert:
        textprint('У вас недостаточно денег для этого действия.')
        textprint('Требуется денег: ' + str(abs(deltabalance)) + ', ваш баланс: ' + str(balance))
    if (food + deltafood < 0) or (rest + deltarest < 0) or (balance + deltabalance < 0):
        return False
    else:
        if deltahealth > 0:
            health += deltahealth
            if health > maxhealth:
                health = maxhealth
        if deltafood > 0:
            food += deltafood
            if food > maxfood:
                food = maxfood
        if deltarest > 0:
            rest += deltarest
            if rest > maxrest:
                rest = maxrest
        return True
start()
root.mainloop()