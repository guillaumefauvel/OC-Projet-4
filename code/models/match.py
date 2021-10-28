
class Match:

    _registry = []

    def __init__(self, player_1, player_2,parent_reference):
        self._registry.append(self)
        self.player_1 = player_1
        self.player_2 = player_2
        self.parent = parent_reference
        self.winner = ""
        self.scoreboard = self.parent.scoreboard
        return

