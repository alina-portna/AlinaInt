list_x_popul = [0, 40, 50, 60, 70, 80, 90, 100]
angles_popul = [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
y0 = 0
x = 75

""" Lam задает кусочно ломаную функцию, которая проходит через все точки из list_x
и соединяет каждую пару (list_x[i-1], list_x[i]) отрезком прямой, которая имеет угол наклона angles[i]
Lam возвращает значение этой функции в точке x.
Предполагается использовать функцию для популярности и рейтинга пользователя в местах."""
def Lam(list_x, angles, y0, x):
    list_y = points(list_x, angles, y0)
    if x >= list_x[-1]:
        y = list_y[-1] + angles[-1] * (x - list_x[-1])
    elif x <= list_x[0]:
        y = angles[0]*x + y0
    else:
        a = find_interval(list_x, x)
        y = (x - list_x[a])*(list_y[a+1] - list_y[a])/(list_x[a+1] - list_x[a]) + list_y[a]
    return(y)

def points(list_x, angles, y0):
    y = [y0]
    for i in range(1,len(list_x)):
        new = y[i-1] + angles[i]*(list_x[i] - list_x[i-1])
        y.append(new)
    return(y)

def find_interval(list_x, x):
    a = 0
    c = len(list_x)
    b = round(len(list_x)/2)
    while c != a+1:
        if x >= list_x[b]:
            a = b
            b = round((c + b)/2)
        else:
            c = b
            b = round((a + b)/2)
    return a
# x is in interval [a, a+1]

#print(points(list_x_popul, angles_popul, y0))
#print(Lam(list_x_popul, angles_popul, y0, x))
#print(find_interval(list_x_popul, x))



# Функция La такая же как и Lam, была лишь немного изменена чтобы можно было отразить ее на графике.
# Чтобы увидить график функции - при запуске программы ввести: La(x)
def La(x):
    list_x = [0, 40, 50, 60, 70, 80, 90, 100]
    angles = [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
    y0 = 0
    list_y = points(list_x, angles, y0)
    if x >= list_x[-1]:
        y = list_y[-1] + angles[-1] * (x - list_x[-1])
    elif x <= list_x[0]:
        y = angles[0] * x + y0
    else:
        a = find_interval(list_x, x)
        y = (x - list_x[a]) * (list_y[a + 1] - list_y[a]) / (list_x[a + 1] - list_x[a]) + list_y[a]
    return (y)



"""
vwp - Voice weight for places
vwp возвращает вес голоса для голосования в М&М
Чтобы было видно на графике - масштаб увеличен на 10. На самом деле вес должен изменяться от 1 до 5 для рейтинга от 0 до 45
В данном подобраном случае...
    for i in range(0, 20):
    list_x.append(i*50)
        angles = [0, 0.2]
        a -= 0.03
... уклон меняется около 6 раз, каждые 5 б рейтинга.
выходит, что вес голоса меняется от 1 до 5 для пользователей с рейтингом в м\м от 0 до 40
Можно было бы уточнить - сделать переход плавнее. Может доделаю, если найду отражение графика получше. На этом плохо видно.
"""
def vwp(x):
    list_x = [0, 50, 100, 150, 200, 250, 300, 350]
    """
    list_x = []
    for i in range(0, 10):
        list_x.append(i*50)
    """

    angles = [0, 0.2, 0.17, 0.14, 0.11, 0.08, 0.05, 0.02]
    """
    angles = [0, 0.2]
    a = angles[1]
    for i in range(2, len(list_x) + 1):
        a -= 0.03
        if a>= 0:
            angles.append(a)
        else:
            angles.append(0)
    """

    y0 = 10
    list_y = points(list_x, angles, y0)
    if x >= list_x[-1]:
        y = list_y[-1] + angles[-1] * (x - list_x[-1])
    elif x <= list_x[0]:
        y = angles[0] * x + y0
    else:
        a = find_interval(list_x, x)
        y = (x - list_x[a]) * (list_y[a + 1] - list_y[a]) / (list_x[a + 1] - list_x[a]) + list_y[a]

    if y <=50:
        return (y)
    else:
        return(50)

print(vwp(1000))


# Lam_by_2str строит функцию по набору точек с заданными координатами
def Lam_by_2str(x):
    list_x = [0, 50, 100, 150, 200]
    angles = [0, 0]
    list_y = [10, 20, 30, 40, 50]
    if x > list_x[-1]:
        y = list_y[-1] + angles[-1] * (x - list_x[-1])
    elif x <= list_x[0]:
        y = angles[0] * x + list_y[0]
    else:
        a = find_interval(list_x, x)
        y = (x - list_x[a]) * (list_y[a + 1] - list_y[a]) / (list_x[a + 1] - list_x[a]) + list_y[a]
    return (y)
#print(vwp(10.00000001))




from math import *
from tkinter import *

f = input("f(x): ")

root = Tk()

canv = Canvas(root, width = 1000, height = 1000, bg = "white")
canv.create_line(500,1000,500,0,width=2,arrow=LAST)
canv.create_line(0,500,1000,500,width=2,arrow=LAST)

First_x = -500;

for i in range(16000):
	if (i % 800 == 0):
		k = First_x + (1 / 16) * i
		canv.create_line(k + 500, -3 + 500, k + 500, 3 + 500, width = 0.5, fill = 'black')
		canv.create_text(k + 515, -10 + 500, text = str(k), fill="purple", font=("Helvectica", "10"))
		if (k != 0):
			canv.create_line(-3 + 500, k + 500, 3 + 500, k + 500, width = 0.5, fill = 'black')
			canv.create_text(20 + 500, k + 500, text = str(k), fill="purple", font=("Helvectica", "10"))
	try:
		x = First_x + (1 / 16) * i
		new_f = f.replace('x', str(x))
		y = -eval(new_f) + 500
		x += 500
		canv.create_oval(x, y, x + 1, y + 1, fill = 'black')
	except:
		pass
canv.pack()
root.mainloop()

"""очередная попытка закомитить"""






