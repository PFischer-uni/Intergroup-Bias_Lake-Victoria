from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'game1'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLIER = 1.2
    NEXT = "Ifuatayo"
    WAIT = "Tafadhali subiri!"
    STYLE = "<style> .otree-body {font-size: 1.5em;}</style>"
    POCKET = "Mfuko"
    POT = "Chungu"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    total_contribution_after_multiplier = models.CurrencyField()


class Player(BasePlayer):
    contribution = models.IntegerField(
        choices=[[0, "Mfuko"], [10, "Chungu"]],
        label="",
        widget=widgets.RadioSelect,
    )
    contribution_received = models.CurrencyField()
    payoff_other_player = models.CurrencyField()
    reaktion = models.StringField(
        choices=['Mvuvi wa Omena', "Mvuvi wa Sangara (Mbuta)"],
        label="Ni nani uliyecheza naye?",
        widget=widgets.RadioSelect,
    )
    belief = models.IntegerField(
        choices=[[0, "Mfuko"], [10, "Chungu"]],
        label='',
        widget=widgets.RadioSelect,
    )
    beliefs_correctly_guessed_game1 = models.IntegerField()
    fish_of_other_player = models.StringField
    fish_of_player = models.StringField

    payoff_game1 = models.CurrencyField()
# FUNCTIONS


def fish_of_player(player: Player):
    if player.session.config['test_mode']:
        fish_id = player.participant.id_in_session % 2
    else:
        fish_id = player.participant.fish
    return 'Omena' if fish_id == 0 else 'Sangara (Mbuta)'


def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


def session_id(group: Group):
    print('SESSION ID')
    print(group.session.code)


# PAGES


class Reaktion(Page):
    form_model = 'player'
    form_fields = ['reaktion']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff_game1 = player.payoff
        player.participant.payoff_game1 = player.payoff


class WaitAndGroupPage(WaitPage):

    body_text = "Tafadhali subiri!"

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        if not subsession.session.config['test_mode']:
            print('grouping people')
            print(subsession.session.groups_per_round[subsession.round_number])
            subsession.set_group_matrix(subsession.session.groups_per_round[0])
            print('Session Code')
            print(subsession.session.code)


class WaitPage1(WaitPage):

    body_text = "Tafadhali subiri!"

    @staticmethod
    def after_all_players_arrive(group: Group):
        players_in_group = group.get_players()
        group.total_contribution = 0
        for player in players_in_group:
            player.participant.pgg_contribution = player.contribution
            player.contribution_received = player.get_others_in_group()[0].contribution
            player.participant.pgg_contribution_received = player.get_others_in_group()[0].contribution
            group.total_contribution += player.field_maybe_none('contribution')
            if player.belief == player.contribution_received:
                if player.field_maybe_none('beliefs_correctly_guessed_game1') is not None:
                    player.beliefs_correctly_guessed_game1 = player.beliefs_correctly_guessed_game1 + 1
                else:
                    player.beliefs_correctly_guessed_game1 = 1

        group.total_contribution_after_multiplier = group.total_contribution * 1.2

        for player in players_in_group:
            player.payoff = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - player.contribution
            player.participant.pgg_payoff = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - \
                                            player.contribution
            player.payoff_other_player = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - \
                                         player.contribution_received
            player.participant.pgg_payoff_other_player = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - \
                                                         player.contribution_received


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief']


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(fish=player.participant.fish)

    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return dict(fish_of_other_player=fish_of_player(other_player))


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

    body_text = "Tafadhali subiri!"


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        player_share = player.group.field_maybe_none(
            'total_contribution_after_multiplier') / 2 if player.group.field_maybe_none(
            'total_contribution_after_multiplier') else 0
        other_player = player.get_others_in_group()[0]
        other_dagaa = fish_of_player(other_player) == 'Omena'
        fish_dagaa = fish_of_player(player) == 'Omena'
        return dict(
            player_share=player_share,
            fish_of_other_player=fish_of_player(other_player),
            other_dagaa=other_dagaa,
            fish_of_player=fish_of_player(player),
            fish_dagaa=fish_dagaa
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.punishment_pgg_payoff = player.payoff
        if player.field_maybe_none('beliefs_correctly_guessed_game1') is not None:
            player.payoff += player.session.config['belief_reward'] * player.beliefs_correctly_guessed_game1


class Info(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        other_dagaa = fish_of_player(other_player) == 'Omena'
        fish_dagaa = fish_of_player(player) == 'Omena'
        return dict(
            fish_of_other_player=fish_of_player(other_player),
            fish_of_player=fish_of_player(player),
            other_dagaa=other_dagaa,
            fish_dagaa=fish_dagaa
        )


class WaitAdvance(Page):
    pass


page_sequence = [WaitAndGroupPage, Info, Contribute, WaitAdvance, Belief, WaitPage1, Results, Reaktion, WaitAdvance]
