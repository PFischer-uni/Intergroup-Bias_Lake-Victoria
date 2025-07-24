from otree.api import *
doc = """
comprehension question 1
"""


class C(BaseConstants):
    NAME_IN_URL = 'comprehension3'
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
    quiz1 = models.StringField(label='Ukweli au Uwongo? Katika hatua ya kwanza ya mchezo, unachagua kwa kiasi gani '
                                     'utapunguza mapato ya mchezaji mwenzako kulingana na kinachoendelea katika hatua ya pili ya mchezo.   ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz1_solution = models.BooleanField()
    quiz2 = models.IntegerField(label='Kuna hali 4 zinazoweza kutokea katika hatua ya pili ya mchezo. Je, ni mara ngapi '
                                      'unahitaji kuamua kwa kiasi gani utapunguza mapato ya mchezaji mwenzako? ',
                                 choices=[1, 2, 3, 4],
                                 widget=widgets.RadioSelect,
                                 blank=False
                                 )
    quiz2_solution = models.BooleanField()
    quiz3 = models.StringField(label='Ukweli au Uwongo? Ikiwa mchezaji mwenzako anachagua kupunguza mapato yako kwa '
                                     'tokeni 3 ikiwa utaweka tokeni 10 mfukoni, utaambiwa kuhusu hii kabla ya kuamua ikiwa utaweka tokeni 10 katika chungu au mfukoni mwako.',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz3_solution = models.BooleanField()
    quiz4 = models.StringField(label='Ukweli au Uwongo? Ikiwa utachagua kupunguza mapato ya mchezaji mwenzako kwa '
                                     'tokeni 6 ikiwa mchezaji mwenzako anaamua kuweka tokeni 10 katika chungu, atapewa'
                                     ' taarifa kuhusu hii kabla ya kuamua ikiwa ataweka tokeni 10 katika chungu au mfukoni mwake. ',
                               choices=["Ukweli", "Uwongo"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz4_solution = models.BooleanField()
    quiz5 = models.StringField(label='Kituufu oba Sikituufu? Mu mutendera owokubiri owo muzannyo, ggwe ne muzannyi '
                                     'munno mufuna obubonero 10 okuva gyetuli ne musalawo oba mu buteeka mu nuwa oba '
                                     'mu nawo.',
                               choices=["Kituufu", "Sikituufu"],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz5_solution = models.BooleanField()
    quiz6 = models.StringField(label='Okugeza ggwe ne muzannyi munno muteeka obubonero kkumi (10) mu nsuuwa. Mumbera'
                                     ' eno, olina okusalawo obutakedeza ku nfuna yo muzannyi munno. Mu mbetra eno '
                                     'muzannyi munno asazeewo okukendeza ku nfuna yo n’obubonero buatu (3). Ani afuna ekingi?',
                               choices=['ofuna kingi', 'muzanyi munno afuna kingi'],
                               widget=widgets.RadioSelect,
                               blank=False
                               )
    quiz6_solution = models.BooleanField()


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
        if player.quiz2 == 4:
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
        if player.quiz4 == 'Ukweli':
            player.quiz4_solution = True
        else:
            player.quiz4_solution = False


class quiz4_solution(Page):
    form_model = 'player'


class quiz5(Page):
        form_model = 'player'
        form_fields = ['quiz5']

        @staticmethod
        def before_next_page(player: Player, timeout_happened):
            if player.quiz5 == 'Kituufu':
                player.quiz5_solution = True
            else:
                player.quiz5_solution = False


class quiz5_solution(Page):
    form_model = 'player'


class quiz6(Page):
    form_model = 'player'
    form_fields = ['quiz6']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz6 == 'muzanyi munno afuna kingi':
            player.quiz6_solution = True
        else:
            player.quiz6_solution = False


class quiz6_solution(Page):
    form_model = 'player'


page_sequence = [quiz1, quiz1_solution, quiz2, quiz2_solution, quiz3, quiz3_solution,
                 quiz4, quiz4_solution]