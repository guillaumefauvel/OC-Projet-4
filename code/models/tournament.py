import collections
from tinydb import TinyDB, Query
from code.models.round import Round
import json

class Tournament:

    _registry = []

    def __init__(self, name, location, start_date, end_date, num_of_round, selected_players, game_type, notes):

        self._registry.append(self)
        self.reference = self
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.num_of_round = num_of_round
        self.selected_players = selected_players
        self.game_type = game_type
        self.notes = notes
        self.num_of_duel = int(len(self.selected_players)/2)
        self.scoreboard = ""
        self.ranked_dict = {}
        self.object_dict = {}


    def return_ranking(self):
        """ Return a ordered dictionnary that contains participants informations
        key=index, value1 = player.reference """

        raw_rank = {}

        for player in self.selected_players:
            raw_rank[player.ranking] = player.reference
        ordered_dict = collections.OrderedDict(sorted(raw_rank.items()))

        for player, index, in zip(ordered_dict, range(1, len(self.selected_players) + 1)):
            self.ranked_dict[index] = ordered_dict[player],

        return

    def scoreboard_maker(self):
        self.scoreboard = TinyDB('scoreboard.json', indent=1)
        if (len(self.scoreboard)) < 1: ## -DEVonly
            def add_to_database(rank,ref,ID):
                self.scoreboard.insert({'Classement':rank,'Reference': ref, 'ID':ID, "Score": 0,
                                        "Classement-Score": 0, "Association(s)":[]})
            for index in self.ranked_dict:
                add_to_database(index,self.ranked_dict[index][0],index)

    def sort_score_rank(self):
        """Sort the json file based on his 'Classement-Score' key"""
        for line, rank in zip(sorted(self.scoreboard, key=lambda k: k['Score'],
                                     reverse=True),range(1,len(self.selected_players)+1)):
            self.scoreboard.update({'Classement-Score': rank},
                                   Query().Reference == line['Reference'])

        return

    def first_draw(self):
        """ Generate the first list of duel """

        self.duel_list = []

        for index in range(self.num_of_duel):

            results = []
            player_1 = self.scoreboard.search(Query().Classement == index+1)
            player_2 = self.scoreboard.search(Query().Classement == index+1+self.num_of_duel)

            results.append(player_1[0]['Reference'])
            results.append(player_2[0]['Reference'])
            self.duel_list.append(results)

            # Write the duel associations into the scoreboard
            self.scoreboard.update({'Association(s)': player_2[0]['ID']},
                                   Query().Reference == player_1[0]['Reference'])
            self.scoreboard.update({'Association(s)': player_1[0]['ID']},
                                   Query().Reference == player_2[0]['Reference'])


        # Create the round
        self.object_dict[1] = Round(self.duel_list,self)
        # Create the match attached to this round
        self.object_dict[1].make_match()

        return self.duel_list

    def updating_scoreboard_score(self, round):
        """ Update the score of the scoreboard
        Arg : the round index
        Return : nothing, modification of the scoreboard file
        """
        for match in self.object_dict[round].attached_match:
            if match.winner == "1":
                old_score = self.scoreboard.search(Query().Reference == match.player_1)[0]['Score']
                self.scoreboard.update({'Score':old_score + 1}, Query().Reference == match.player_1)
            elif match.winner == "2":
                old_score = self.scoreboard.search(Query().Reference == match.player_2)[0]['Score']
                self.scoreboard.update({'Score': old_score + 1}, Query().Reference == match.player_2)
                pass
            else:
                old_score_p1 = self.scoreboard.search(Query().Reference == match.player_1)[0]['Score']
                old_score_p2 = self.scoreboard.search(Query().Reference == match.player_2)[0]['Score']
                self.scoreboard.update({'Score':old_score_p1 + 0.5}, Query().Reference == match.player_1)
                self.scoreboard.update({'Score':old_score_p2 + 0.5}, Query().Reference == match.player_2)
                pass

    def duel_generator(self):
        pass

