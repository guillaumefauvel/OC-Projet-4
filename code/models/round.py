""" Round object"""

from models.match import Match
from datetime import datetime


class Round:
    """ A Round object is created by a tournament """
    _registry = []

    def __init__(self, duel_list):
        self._registry.append(self)
        self.duel_list = duel_list
        self.attached_match = []
        self.start_time = datetime.now()
        self.end_time = ""
        return

    def make_match(self):
        """ The Round object uses his own list in order to create Matchs objects """

        for duel in self.duel_list:
            player_1, player_2 = duel
            self.attached_match.append(Match(player_1, player_2))
