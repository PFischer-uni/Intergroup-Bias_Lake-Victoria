from otree.api import *
doc = """
comprehension question 1
"""


class C(BaseConstants):
    NAME_IN_URL = 'comprehension1'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NEXT = "Ifuatayo"
    WAIT = "Tafadhali subiri!"
    STYLE = "<style> .otree-body {font-size: 1.5em;}</style>"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz1 = models.StringField(label='Ukweli au Uwongo? Ikiwa wachezaji wote wawili watatia kiasi sawa kwenye chungu,'
                                     ' wote watapata kiasi sawa.   ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz1_solution = models.BooleanField()
    quiz2 = models.StringField(label='Ukweli au Uwongo? Ikiwa wewe na mchezaji mwenzako mtaweka tokeni 10 kwenye'
                                     ' chungu, mtapata zaidi kuliko ikiwa wewe na mchezaji mwenzako mtaweka tokeni 0 kwenye chungu.  ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz2_solution = models.BooleanField()
    quiz3 = models.StringField(label='Ukweli au Uwongo? Ikiwa utaweka tokeni chini ya mchezaji mwenzako kwenye chungu,'
                                     ' utapata zaidi kuliko mchezaji mwenzako.    ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz3_solution = models.BooleanField()
    quiz4 = models.StringField(label='Okutebereza bwoteeka obubonero kkumi (10) mu nsuuwa ate muzannyi munno n’ateeka '
                                     'obubonero ziro (0) mu nsuuwa, ani afuna ekingi?',
                               choices=['ofuna kingi', 'muzanyi munno afuna kingi'],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz4_solution = models.BooleanField()


# PAGES
class quiz1(Page):
    form_model = 'player'
    form_fields = ['quiz1']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz1 == "Ukweli":
            player.quiz1_solution = True
        else:
            player.quiz1_solution = False

class quiz1_solution(Page):
    form_model = 'player'


class quiz2(Page):
    form_model = 'player'
    form_fields = ['quiz2']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz2 == 'Ukweli':
            player.quiz2_solution = True
        else:
            player.quiz2_solution = False

class quiz2_solution(Page):
    form_model = 'player'

class quiz3(Page):
    form_model = 'player'
    form_fields = ['quiz3']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz3 == 'Ukweli':
            player.quiz3_solution = True
        else:
            player.quiz3_solution = False


class quiz3_solution(Page):
    form_model = 'player'


class quiz4(Page):
    form_model = 'player'
    form_fields = ['quiz4']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz4 == 'muzanyi munno afuna kingi':
            player.quiz4_solution = True
        else:
            player.quiz4_solution = False


class quiz4_solution(Page):
    form_model = 'player'


page_sequence = [quiz1, quiz1_solution, quiz2, quiz2_solution, quiz3, quiz3_solution]