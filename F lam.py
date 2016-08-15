list_x_popul = [0, 40, 50, 60, 70, 80, 90, 100]
angles_popul = [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
x = 75

""" Lam задает кусочно ломаную функцию, которая проходит через все точки из list_x
и соединяет каждую пару (list_x[i-1], list_x[i]) отрезком прямой, которая имеет угол наклона angles[i]
Lam возвращает значение этой функции в точке x.
Предполагается использовать функцию для популярности и рейтинга пользователя в местах."""
def Lam(list_x, angles, x):
    list_y = points(list_x, angles)
    if x > list_x[-1]:
        y = list_y[-1] + angles[-1] * (x - list_x[-1])
    elif x <= list_x[0]:
        y = angles[0]*x + list_x[0]
    else:
        a = find_interval(list_x, x)
        y = (x - list_x[a])*(list_y[a+1] - list_y[a])/(list_x[a+1] - list_x[a]) + list_y[a]
    return(y)

def points(list_x, angles):
    y = [0]
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

print(points(list_x_popul, angles_popul))
print(Lam(list_x_popul, angles_popul, x))
#print(find_interval(list_x_popul, x))



# Функция La такая же как и Lam, была лишь немного изменена чтобы можно было отразить ее на графике.
# Чтобы увидить график функции - при запуске программы ввести: La(x)
def La(x):
    list_x = [0, 40, 50, 60, 70, 80, 90, 100]
    angles = [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
    list_y = points(list_x, angles)
    if x > list_x[-1]:
        y = list_y[-1] + angles[-1] * (x - list_x[-1])
    elif x <= list_x[0]:
        y = angles[0] * x + list_x[0]
    else:
        a = find_interval(list_x, x)
        y = (x - list_x[a]) * (list_y[a + 1] - list_y[a]) / (list_x[a + 1] - list_x[a]) + list_y[a]
    return (y)


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










