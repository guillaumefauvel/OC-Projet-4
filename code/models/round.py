from code.models.match import Match

class Round:

    def __init__(self, duel_list, parent_reference):
        self.duel_conbinations = duel_list
        self.parent = parent_reference

    def make_match(self):

        for duel in self.duel_conbinations:
            player_1, player_2 = duel
            Match(player_1, player_2,self.parent)