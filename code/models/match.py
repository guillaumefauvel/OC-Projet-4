""" Match object """


class Match:
    """The Match object is created by the Round object """
    _registry = []

    def __init__(self, player_1, player_2):
        self._registry.append(self)
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = ""
        self.start_time = ""
        self.end_time = ""

        return
