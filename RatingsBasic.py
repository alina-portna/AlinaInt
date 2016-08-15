
class User(object):
    def __init__(self, directlikes, artlikes, commlikes ):
        """
        :param directlikes:  - это перечень пар (авторитет, популярность) всех юзеров, которые лайкнули данного
        :param artlikes - перечень всех оценок статей, то ли их сумма, то ли среднее оценок. еще не решено что нужно
        :param commlikes: - перечень весов лайков за комменты юзера\или же сумма лайков
        """
        self.directlikes = directlikes
        self.artlikes = artlikes
        self.commlikes = commlikes

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
