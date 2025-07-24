from otree.api import *
from random import randrange
from time import sleep

doc = """
Public goods with punishment, treatment where punishment table is first, then they are viewed, then
contribution is decided.
"""


class C(BaseConstants):
    NAME_IN_URL = 'game3'
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


def planned_punishment_field(contribution, contribution_received):
    return models.IntegerField(
        choices=[0, 3, 6, 9, 12],
        label="",
        widget=widgets.RadioSelect,
    )


class Player(BasePlayer):
    zz = planned_punishment_field(0, 0)
    zt = planned_punishment_field(0, 10)
    tz = planned_punishment_field(10, 0)
    tt = planned_punishment_field(10, 10)

    contribution = models.IntegerField(
        choices=[[0, "Mfuko"], [10, "Chungu"]],
        label="",
        widget=widgets.RadioSelect,
    )
    contribution_received = models.CurrencyField()
    punishment = models.IntegerField(
        choices=[0, 3, 6, 9, 12],
        label="Please choose between 0, 3, 6, 9 and tokens.",
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
    beliefs_correctly_guessed_game3 = models.IntegerField()

    payoff_game3 = models.CurrencyField()

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


class PunishmentMatrix(Page):
    form_model = 'player'
    form_fields = ['zz', 'zt', 'tz', 'tt']

    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        return dict(fish_of_other_player=fish_of_player(other_player))


class PunishmentMatrixWait(WaitPage):
    pass


class PunishmentMatrixReview(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player=player.get_others_in_group()[0])


class Contribute1(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player=player.get_others_in_group()[0])


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
                if player.field_maybe_none('beliefs_correctly_guessed_game3') is not None:
                    player.beliefs_correctly_guessed_game3 = player.beliefs_correctly_guessed_game3 + 1
                else:
                    player.beliefs_correctly_guessed_game3 = 1

        group.total_contribution_after_multiplier = group.total_contribution * 1.2

        for player in players_in_group:
            other_player = player.get_others_in_group()[0]
            player.payoff = group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - player.contribution
            player.payoff_other_player = \
                group.total_contribution_after_multiplier / 2 + C.ENDOWMENT - player.contribution_received

            contributions = (player.contribution, player.contribution_received)

            if contributions == (0, 0):
                player.punishment = player.zz
                player.punishment_received = other_player.zz
            elif contributions == (0, 10):
                player.punishment = player.zt
                player.punishment_received = other_player.tz
            elif contributions == (10, 0):
                player.punishment = player.tz
                player.punishment_received = other_player.zt
            elif contributions == (10, 10):
                player.punishment = player.tt
                player.punishment_received = other_player.tt

        players_in_group = group.get_players()

        for player in players_in_group:
            player.punishment_received = player.get_others_in_group()[0].punishment

        for player in players_in_group:
            player.payoff = (C.MAX_PUNISHMENT - player.punishment) / 3 + player.payoff - player.punishment_received
            player.payoff = player.payoff if player.payoff > 0 else 0


class Reaktion(Page):
    form_model = 'player'
    form_fields = ['reaktion']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff_game3 = player.payoff
        player.participant.payoff_game3 = player.payoff


class Results2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        player_payoff_part1 = player.group.total_contribution_after_multiplier / 2 + (C.ENDOWMENT - player.contribution)
        other_player_payoff_part1 = \
            other_player.group.total_contribution_after_multiplier / 2 + (C.ENDOWMENT - other_player.contribution)
        extra_token = (C.MAX_PUNISHMENT - player.punishment) / 3
        extra_token_received = (C.MAX_PUNISHMENT - player.punishment_received) / 3
        other_dagaa = fish_of_player(other_player) == 'Omena'
        fish_dagaa = fish_of_player(player) == 'Omena'
        return dict(
            fish_of_other_player=fish_of_player(other_player),
            fish_of_player=fish_of_player(player),
            punishment_received=player.punishment_received,
            punishment=player.punishment,
            extra_token=extra_token,
            extra_token_received=extra_token_received,
            player_payoff_part1=player_payoff_part1,
            other_player_payoff_part1=other_player_payoff_part1,
            other_player_payoff_part2=other_player.payoff,
            fish_dagaa=fish_dagaa,
            other_dagaa=other_dagaa
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.field_maybe_none('beliefs_correctly_guessed_game3') is not None:
            player.payoff += player.session.config['belief_reward'] * player.beliefs_correctly_guessed_game3


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


class WaitAdvance(Page):
    pass


page_sequence = [
    WaitAndGroupPage,
    Info,
    PunishmentMatrix,
    PunishmentMatrixWait,
    WaitAdvance,
    PunishmentMatrixReview,
    WaitAdvance,
    Contribute1,
    WaitAdvance,
    Belief,
    WaitPage1,
    Results2,
    Reaktion,
    WaitAdvance
    ]