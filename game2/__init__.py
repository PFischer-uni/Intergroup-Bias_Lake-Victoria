from otree.api import *
from random import randrange
from time import sleep

doc = """
Public goods with punishment 
"""


class C(BaseConstants):
    NAME_IN_URL = 'game2'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(10)
    MULTIPLIER = 1.2
    MAX_PUNISHMENT = 12
    NEXT = "Ifuatayo"
    WAIT = "Tafadhali subiri!"
    STYLE = "<style> .otree-body {font-size: 1.5em;}</style>"
    POCKET = "Mfuko"
    POT = "Chungu"



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    total_contribution_after_multiplier = models.CurrencyField()
    individual_share = models.CurrencyField()
    implemented_punishment_player_id = models.IntegerField()


class Player(BasePlayer):
    contribution = models.IntegerField(
        choices=[[0, "Mfuko"], [10, "Chungu"]],
        label="",
        widget=widgets.RadioSelect,
    )
    contribution_received = models.CurrencyField()
    punishment = models.IntegerField(
        choices=[0, 3, 6, 9, 12],
        label="",
        widget=widgets.RadioSelect,
    )
    punishment_received = models.IntegerField()
    payoff_other_player = models.CurrencyField()
    fish_of_other_player = models.StringField
    fish_of_player = models.StringField
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
    beliefs_correctly_guessed_game2 = models.IntegerField()

    payoff_game2 = models.CurrencyField()


# FUNCTIONS


def fish_of_player(player: Player):
    if player.session.config['test_mode']:
        fish_id = player.participant.id_in_session % 2
    else:
        fish_id = player.participant.fish
    return 'Omena' if fish_id == 0 else 'Sangara (Mbuta)'


# PAGES
class WaitAndGroupPage(WaitPage):

    body_text = "Tafadhali subiri!"

    wait_for_all_groups = True

    @staticmethod
    def after_all_players_arrive(subsession: Subsession):
        if not subsession.session.config['test_mode']:
            print('grouping people')
            print(f'round number {subsession.round_number}')
            print(subsession.session.groups_per_round[subsession.round_number])
            subsession.set_group_matrix(subsession.session.groups_per_round[subsession.round_number])
            print('Session Code')
            print(subsession.session.code)


class Contribute1(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return dict(fish_of_other_player=fish_of_player(other_player))


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief']


class WaitPage1(WaitPage):
    body_text = "Tafadhali subiri!"
    @staticmethod
    def after_all_players_arrive(group: Group):
        players_in_group = group.get_players()
        group.total_contribution = 0
        for player in players_in_group:
            player.contribution_received = player.get_others_in_group()[0].contribution
            group.total_contribution += player.field_maybe_none('contribution')
            if player.belief == player.contribution_received:
                if player.field_maybe_none('beliefs_correctly_guessed_game2') is not None:
                    player.beliefs_correctly_guessed_game2 = player.beliefs_correctly_guessed_game2 + 1
                else:
                    player.beliefs_correctly_guessed_game2 = 1

        group.total_contribution_after_multiplier = group.total_contribution * 1.2

        for player in players_in_group:
            player.payoff = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - player.contribution
            player.payoff_other_player = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - player.contribution_received


class Results1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        player_share = player.group.field_maybe_none('total_contribution_after_multiplier') / 2 if player.group.field_maybe_none('total_contribution_after_multiplier') else 0
        other_dagaa = fish_of_player(other_player) == 'Omena'
        fish_dagaa = fish_of_player(player) == 'Omena'
        return dict(
            player_share=player_share,
            fish_of_other_player=fish_of_player(other_player),
            fish_of_player=fish_of_player(player),
            other_dagaa=other_dagaa,
            fish_dagaa=fish_dagaa
        )


class Punish(Page):
    form_model = 'player'
    form_fields = ['punishment']

    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        player_share = player.group.field_maybe_none(
            'total_contribution_after_multiplier') / 2 if player.group.field_maybe_none(
            'total_contribution_after_multiplier') else 0
        other_dagaa = fish_of_player(other_player) == 'Omena'
        fish_dagaa = fish_of_player(player) == 'Omena'
        return dict(
            player_share=player_share,
            fish_of_other_player=fish_of_player(other_player),
            fish_of_player=fish_of_player(player),
            other_dagaa=other_dagaa,
            fish_dagaa=fish_dagaa
        )


class Reaktion(Page):
    form_model = 'player'
    form_fields = ['reaktion']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff_game2 = player.payoff
        player.participant.payoff_game2 = player.payoff


class WaitPage2(WaitPage):
    body_text = "Tafadhali subiri!"
    @staticmethod
    def after_all_players_arrive(group: Group):
        implemented_punishment_player_id = randrange(2) + 1
        group.implemented_punishment_player_id = implemented_punishment_player_id

        players_in_group = group.get_players()

        for player in players_in_group:
            player.punishment_received = player.get_others_in_group()[0].punishment

        for player in players_in_group:
            player.payoff = (C.MAX_PUNISHMENT - player.punishment) / 3 + player.payoff - player.punishment_received
            player.payoff = player.payoff if player.payoff > 0 else 0


class Results2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        punishes = player.group.implemented_punishment_player_id == player.id_in_group
        other_player = player.get_others_in_group()[0]
        player_payoff_part1 = player.group.total_contribution_after_multiplier / 2 + (C.ENDOWMENT - player.contribution)
        other_player_payoff_part1 = other_player.group.total_contribution_after_multiplier / 2 + (C.ENDOWMENT - other_player.contribution)
        extra_token_received = (C.MAX_PUNISHMENT - player.punishment_received) / 3
        other_dagaa = fish_of_player(other_player) == 'Omena'
        fish_dagaa = fish_of_player(player) == 'Omena'
        return dict(
            punishes=punishes,
            fish_of_other_player=fish_of_player(other_player),
            fish_of_player=fish_of_player(player),
            punishment_received=player.punishment_received,
            punishment=player.punishment,
            extra_token=(C.MAX_PUNISHMENT - player.punishment)/3,
            extra_token_received=extra_token_received,
            player_payoff_part1=player_payoff_part1,
            other_player_payoff_part1=other_player_payoff_part1,
            other_player_payoff_part2=other_player.payoff,
            other_dagaa=other_dagaa,
            fish_dagaa=fish_dagaa
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.punishment_pgg_payoff = player.payoff
        if player.field_maybe_none('beliefs_correctly_guessed_game2') is not None:
            player.payoff += player.session.config['belief_reward'] * player.beliefs_correctly_guessed_game2


class Info(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        other_dagaa = fish_of_player(other_player) == 'Omena'
        return dict(
            fish_of_other_player=fish_of_player(other_player),
            fish_of_player=fish_of_player(player),
            other_dagaa=other_dagaa,
        )


class WaitPage(Page):
    pass


class WaitAdvance(Page):
    pass


page_sequence = [
    WaitAndGroupPage,
    Info,
    Contribute1,
    WaitAdvance,
    Belief,
    WaitPage1,
    Results1,
    WaitAdvance,
    Punish,
    WaitPage2,
    Results2,
    Reaktion,
    WaitAdvance
]