from models.match import Match

class Round:

    _registry = []

    def __init__(self, duel_list):
        self._registry.append(self)
        self.duel_list = duel_list
        self.attached_match = []
        return

    def make_match(self):

        for duel in self.duel_list:
            player_1, player_2 = duel
            self.attached_match.append(Match(player_1, player_2))