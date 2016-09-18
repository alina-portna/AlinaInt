"""
Думаю, что можно обойтись классами: Юзер, Статья, Коммент, Поток.
А Авторитет и Популярность могут остаться атрибутами класса Юзер. Мне так кажется проще поскольку они привязаны к юзеру -
при формировании авторитета юзера1 нужно вытянуть данные всех, кто на него подписался и их авторитеты.
Изменения Авторитета и Популярности происходят после запуска перевычисления с помощью recalc_auth и recalc_popul методов.
Изменения происходят поскольку изменяются атрибуты interpeople, articles и comments обьекта (данного юзера) при поступлении к ним новых данных.
Массивы interusers, interpeople, articles и некоторые др. атрибуты в классах User, Article, Comment должны регулярно обновляться при поступлении новых взаимодействий.
"""
from math import log, fabs, copysign, pi, atan

class User(object):
    def __init__(self, user_id, interpeople, articles, comments, Authority, Popularity, Flowrating ):
        self.user_id = user_id
        self.interpeople = interpeople
        """- массив, где каждая строка - список:
        (user_id, addedtofriends, subscribed, complained, authwhensubscr, authwhencomp) - пользователь, который хоть как-то взаимодействовал с данным юзером + инфо о взаимодействии."""

        self.articles = articles
        """- массив, где каждый эл - (article_id, article_rating).
        В этот словарь поступает новый эл-нт каждый раз, когда появляется новый обьект класса Article с атрибутом author, который равен user_id."""

        self.comments = comments
        """- массив, где каждый эл - (comment_id, comment_rating)
        В этот словарь поступает новый эл-нт каждый раз, когда появляется новый обьект класса Comment с атрибутом owner, который равен user_id."""

        self.Authority = Authority
        self.Popularity = Popularity
        self.Flowrating = Flowrating
        """
        Authority(articles, interpeople)
        Popularity(interpeople, comments)
        Flowrating(articles)
        - переменные, которым присваиваются значения раз в сутки\ поcле изменений в переменных  interpeople, articles, comments
        (когда новый юзер делает какую-то оценку этому либо уже оценивший меняет свою оценку)
        """

    def recalc_auth(self):
        sum_art = 0
        av = 3
        for article in self.articles:
            sum_art += article[1]
        if len(self.articles) != 0: # приметка: если юзер удаляет все статьи, av снова = 3. можно так оставить.
            av = sum_art/len(self.articles)
        #print("av = %s" % av)

        sum_scores = 0
        for i in range(len(self.interpeople)):
            if self.interpeople[i][2] == 1: # значит юзер под индексом i подписан на данного юзера
                sum_scores += pow(self.interpeople[i][4],1.2)/10 #добавляется pow(authwhensubscr юзера под индексом i,1.2)/10
                #p1 = pow(self.interpeople[i][4],1.2)/10
                #print("добавляем %s" % p1)
            if self.interpeople[i][2] == 1:  # значит юзер под индексом i пожаловался на данного юзера
                sum_scores -= 2*pow(self.interpeople[i][5], 1.2) / 10 #отнимается 2*pow(authwhencomp юзера под индексом i,1.2)/10
                #p2 = 2*pow(self.interpeople[i][5], 1.2) / 10
                #print("отнимаем %s" % p2)
        self.Authority = av + fauth(sum_scores)

    def recalc_popul(self):
        sum1 = 0
        for comment in self.comments:
            sum1 += copysign(1, 2*comment[1] - 1)*pow(2*comment[1] - 1,2)

        sum2 = 0
        for person in self.interpeople:
            if person[1] == 1: # person is addedtofriends
                sum2 +=1
            if person[2] == 1:  # person is subscribed
                sum2 +=1

        self.Popularity = 3 + Flam1(sum1) + Flam2(sum2*0.125)

"""ДОДЕЛАТЬ: Авторитет и Популярность юзера по умолчанию = 3. Можно присваивать атрибутам обьекта эти значения при его обьявлении."""

def fauth(x):
    if x > 4:
        return log(x, 4)
    elif x >= -4:
        return x / 4
    else:
        return - log(fabs(x), 4)

def Flam1(x):
    list_x_popul = [0, 40, 50, 60, 70, 80, 90, 100]
    angles_popul = [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
    y0 = 0
    return(Lam(list_x_popul, angles_popul, y0, x))

def Flam2(x):
    list_x_popul2 = [0, 40, 50, 60, 70, 80, 90, 100, 140, 160, 180, 200, 1000, 5000]
    angles_popul2 = [1, 1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05, 0.01, 0.005, 0.001]
    y02 = 0
    return(Lam(list_x_popul2, angles_popul2, y02, x))

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


user1 = User("u1", [["u3", 1, 0, 0, 3, 0],["u4", 0, 1, 0, 4, 8]], [["a1",7],["a2",9]], [["c1", 0.5], ["c2", 0.99]], 4, 0, 0)
user2 = User("u2", [["u5", 1, 0, 0, 3]], [], [], 4, 10, 0)

print("user1 popul before = %s" % user1.Popularity)
user1.recalc_popul()
print("user1 popul after = %s" % user1.Popularity)

print("user1 auth before = %s" % user1.Authority)
user1.recalc_auth()
print("user1 auth after = %s" % user1.Authority)
"""
print(user1.interpeople)
print(user2.interpeople)
print(len(user1.interpeople))
# по умолчанию присваивать authwhensubscr = 3, authwhencomp = 3
"""
if len("Если юзер2 добавил в друзья юзер1")%2 == 1:
    """Вместо этого условия в if statement должно быть условие клика по кнопке "добавить"
    Здесь дополняется элемент в user1.interpeople либо актуализируется существующий там в зависимости
    от того взаимодействовал ли уже юзер2 с юзером1"""
    interusers = []
    user2wasfound = 0
    for i in range(len(user1.interpeople)):
        if user1.interpeople[i][0] == user2.user_id:
            user1.interpeople[i][1] = 1  # addedtofriends = 1
            user2wasfound = 1
    if user2wasfound == 0:
        user1.interpeople.append([user2.user_id, 1, 1, 0, user2.Authority, 0]) # 2 и 3 эл. - единицы, поскольку добавление в друзья идет сразу с подпиской
        #ПС: эл. authwhensubscr (присвоила ему user2.Authority) не должен изменяться при "добалении\удалении" из друзей, только при подписке.
        #Cделал так лишь потому, что юзера все равно не было еще в списке, а подписка осуществилась автоматически.
#print(user1.interpeople)

if len("Если юзер2 удалил из друзей юзер1 ")%2 == 1:
    interusers = []
    for i in range(len(user1.interpeople)):
        if user1.interpeople[i][0] == user2.user_id:
            user1.interpeople[i][1] = 0  # addedtofriends = 0
"""
print("after adding to fr")
print(user1.interpeople)
print(user2.interpeople)
print(len(user1.interpeople))
"""
if len("Если юзер2 подписался на юзер1 ")%2 == 1:
    interusers = []
    user2wasfound = 0
    for i in range(len(user1.interpeople)):
        if user1.interpeople[i][0] == user2.user_id:
            user1.interpeople[i][2] = 1  # subscribed = 1
            user1.interpeople[i][4] = user2.Authority   #эту строку нужно добавлять только при действии "подписка" и
            # нельзя изменять значение авторитета в interpeople при добавлении в друзья.
            user2wasfound = 1
    if user2wasfound == 0:
        user1.interpeople.append([user2.user_id, 0, 1, 0, user2.Authority, 0])

if len("Если юзер2 отписался от юзер1 ")%2 == 1:
    interusers = []
    for i in range(len(user1.interpeople)):
        if user1.interpeople[i][0] == user2.user_id:
            user1.interpeople[i][2] = 0  # subscribed = 0
            user1.interpeople[i][4] = 0 #  Authority = 0

"""Cделать аналогичные изменения в user1.interpeople при клике на "пожаловаться" и его отмене.
    если юзер2 пожаловался на юзер1:
    user1.interpeople[k][3] = 1, где индекс k соостветствует юзеру2
    user1.interpeople[k][5] = user2.Authority
    если юзер2 отменил пожаловаться на юзер1:
    user1.interpeople[k][3] = 0, где индекс k соостветствует юзеру2
    user1.interpeople[k][5] = 0
"""
"""
print("after subscr")
print(user1.interpeople)
print(user2.interpeople)
print(len(user1.interpeople))
"""

class Article(object):
    def __init__(self, article_id, flow, author, auth_wwrote, interusers, shares, comments, watches, artrating ):
        self.article_id = article_id
        self.flow = flow
        self.author = author
        self.auth_wwrote = auth_wwrote #авторитет автора когда он написал статью
        self.interusers = interusers
        """
        interusers - массив, где каждый элемент:
        (user_id, value, Flowrating_wt, Auth_wt, Popul_wt, weight)
        wt - when was touched (liked\disliked)
        Flowrating_wt, Auth_wt, Popul_wt должны обновляться (вытягиваются текущие из данного юзера), но только тогда, когда изменяется значение в value,
        то есть при клике на лайк/ дислайк
        value == 1/ -1 / 0 - лайк/ дислайк/ отсутствие оценки
        """
        self.shares = shares #кол-во шарингов статьи
        self.comments = comments #кол-во комментов к статье
        self.watches = watches #кол-во просмотров
        self.artrating = artrating

    def recalc_interusers(self):
        #пересчитывает вес голосов юзеров
        for user in self.interusers:    #можно делать пересчет не для всех, а только тех, у которых произошло изменение в полях лайк и дислайк
            self.interusers[5] = log(self.interusers[2]+1,4) + self.interusers[3]/3 +  log(self.interusers[4]-2,8)

    def recalc_artrating(self):
        recalc_interusers(self)
        C = 7.0
        M = 10.0
        N = 0.0
        sum_wlikes = 0
        sum_wdislikes = 0
        for user in self.interusers:
            if self.interusers[user][1] == 1: #user поставил лайк
                sum_wlikes += self.interusers[user][5]
                N += 1
            elif self.interusers[user][1] == -1:  # user поставил дислайк
                sum_wdislikes += self.interusers[user][5]
                N += 1 # расчитываю, что юзер не может нажать одновременно и лайкнуть и дислайкнуть.
        self.artrating = sum_wlikes/(sum_wlikes + sum_wdislikes)*N/(N+M) + C*M/(N+M) + 2/pi * (atan(self.shares/40) +2/3 * atan(self.comments/40) + 1/3 * atan(self.watches/80))



class Comment(object):
    def __init__(self, comment_id, owner, interusers, commrating):
        self.comment_id = comment_id
        self.owner = owner
        self.interusers = interusers
        """
        interusers - массив, где каждый элемент:
        (user_id, flowrating_wt, auth_wt, popul_wt, value)   (wt - when was touched (liked\disliked\complained))
        value == 1/ -1 / -2  - лайк/ дислайк/ пожаловался на коммент
        """
        self.commrating # ДОДЕЛАТЬ: при обьявлении обьекта положить по умолчанию равным 0


class Flow(object):
    def __init__(self, articles, subscrquantity):
        self.articles = articles
        self.subscrquantity = subscrquantity
    """
    из articles берутся статьи только этого потока c рейтингом статьи и auth_wwrote
    и высчитывается качество потока
    затем вместе с subscrquantity подсчитывается рейтинг потока
    """

"""
Немного устаревшее. Сами зависимости уже частично изменились, а подход в реализации упростила.
class UserPopularity(User):
    popularity = 3.0
    comm_component = 0.0
    if __name__ == '__main__':
        def up(self, popularity, comm_component):
            self.comm_component = self.commlikes
            self.popularity = f1(self.popularity - self.comm_component , self.directlikes, self.commlikes) + self.comm_component
            # функция f записана условно. должен идти расчет при каждом новом поступлении в directlikes
            # comm_component отделила чтобы прирост популярности не зависел от полученных ранее комментов.
            # Если сделаем чтобы на вес прямого лайка влияли лайки за статьи, то нужно будет добавить в f зависимость от
            # artlikes, либо же от Авторитета

            # Понимаю, что сейчас это все очень условно, поскольку зависимости не устаканены.
            # Неожиданных связей будет больше и может лучше держать рейтинги\авторитеты как переменные в одном классе - Юзер.
            # Потому что уже, например, хочется чтобы популярность, которая образовуется, сохранялась в родительский класс Юзер в directlikes
            # на случай какого-нибудь сбоя.
            # А может это могут быть разные классы, но лучше чтобы без наследования. Не хватает понимания связей между классами..
            # Потому мне хотелось бы сначала понять что от чего будет зависеть в рейтингах, а чтобы потом выбиралось как лучше кодить.

class UserAuthority(User):
    authority = 3.0
    def up_and_down(self):
        authority = 3.0 + len(self.directlikes) + f2(self.artlikes)
#расчет идет при каждом изменении в directlikes или artlikes\ раз в сутки
"""
