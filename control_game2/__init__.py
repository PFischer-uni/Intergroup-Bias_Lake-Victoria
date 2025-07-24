from otree.api import *
doc = """
comprehension question 1
"""


class C(BaseConstants):
    NAME_IN_URL = 'comprehension2'
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
    quiz1 = models.StringField(label='Ukweli au Uwongo? Katika hatua ya kwanza ya mchezo, wewe na mchezaji mwenzako '
                                     'mnapokea tokeni 10 kutoka kwetu na mnachagua iwapo mtaziweka tokeni 10 katika chungu au mfukoni.  ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz1_solution = models.BooleanField()
    quiz2 = models.StringField(label='Ukweli au Uwongo? Baada ya wewe na mchezaji mwenzako kujua ikiwa mmeweka tokeni '
                                     '10 katika chungu au mfukoni, mnachagua katika hatua ya pili kwa kiasi gani mnataka kupunguza mapato ya mchezaji mwenzako.  ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz2_solution = models.BooleanField()
    quiz3 = models.StringField(label='Ni kiasi gani unapaswa kulipa ili kupunguza mapato ya mchezaji mwenzako kwa tokeni 3?  ',
                               choices=['1', '2', '3', '4'],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz3_solution = models.BooleanField()
    quiz4 = models.StringField(label='Onego ichul marom nade mondo iduok yuto mar jatugo wadu piny kod token 3?  ',
                                choices=['0', '1', '2', '3'],
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
        if player.quiz2 == "Ukweli":
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
        if player.quiz3 == '1':
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
        if player.quiz4 == '0':
            player.quiz4_solution = True
        else:
            player.quiz4_solution = False


class quiz4_solution(Page):
    form_model = 'player'


page_sequence = [quiz1, quiz1_solution, quiz2, quiz2_solution, quiz3, quiz3_solution]