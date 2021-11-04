import collections
from tinydb import TinyDB, Query
from models.round import Round
from controllers.controller_tournament import convert_to_player_object, round_conversion

class Tournament:

    _registry = []
    _serialized_registry = []

    def __init__(self, name, location, start_date, end_date, num_of_round, selected_players, game_type, notes):

        self._registry.append(self)
        self.reference = self
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.num_of_round = num_of_round
        self.selected_players = selected_players
        self.players_object = convert_to_player_object(self.selected_players)
        self.game_type = game_type
        self.notes = notes
        self.num_of_duel = int(len(self.selected_players)/2)
        self.scoreboard = {}
        self.object_dict = {}
        self.serialized_object = {}

    def return_ranking(self):
        """ Return a ordered dictionnary that contains participants informations
        key=index, value1 = player.reference """

        raw_rank = {}
        for player in self.players_object:
            raw_rank[player.ranking] = player.reference
        ordered_dict = collections.OrderedDict(sorted(raw_rank.items()))

        for player, index, in zip(ordered_dict, range(1, len(self.players_object) + 1)):
            self.scoreboard[index] = { "reference" : ordered_dict[player], "id" : index,"scorerank" : 0,
                                            "score" : 0, "associations" : [] }

    def sort_score_rank(self):
        # """Sort the json file based on his 'Classement-Score' key"""
        for line, rank in zip(sorted(self.scoreboard.values(), key=lambda k: k['score'],
                                     reverse=True),range(1,len(self.players_object)+1)):
            line['scorerank'] = rank
        return

    def first_draw(self):
        """ Generate the first list of duel by analysing the scoreboard database """

        self.duel_list = []

        for index in range(1,self.num_of_duel+1):
            results = []
            player_1 = self.scoreboard[index]
            player_2 = self.scoreboard[index+self.num_of_duel]

            results.append(player_1['reference'])
            results.append(player_2['reference'])
            self.duel_list.append(results)

            player_1['associations'].append(player_2['id'])
            player_2['associations'].append(player_1['id'])

        # Create the round
        self.object_dict[1] = Round(self.duel_list)
        # Create the match attached to this round
        self.object_dict[1].make_match()

        return self.duel_list

    def updating_scoreboard_score(self, round):
        """ Update the score of the scoreboard
        Arg : the round index
        Return : nothing, modification of the scoreboard file
        """
        list_of_winner = []
        list_of_equality = []

        for match in self.object_dict[round].attached_match:
            if match.winner == "1" :
                list_of_winner.append(match.player_1)
            elif match.winner == "2" :
                list_of_winner.append(match.player_2)
            else:
                list_of_equality.append(match.player_1)
                list_of_equality.append(match.player_2)

        for player in self.scoreboard.values():
            if player['reference'] in list_of_winner:
                player['score'] = player['score']+1
            if player['reference'] in list_of_equality:
                player['score'] = player['score']+0.5

    def generating_other_draw(self,round_index):
        """ Generate a list of duel by analysing the scoreboard database, it also make a round and some matchs
        Arg : The round index - in order to link the round to his tournament
        Return : The list of the duels """

        dict = {}
        duel_list = []

        for value, index in zip(sorted(self.scoreboard.values(), key=lambda k: k['score'],reverse=True),range(1,len(self.scoreboard)+1)):
            dict[index] = value['id'],value['associations'],value['reference']

        for value in list(dict):
            if value not in list(dict):
                pass
            else:
                try:
                    condition = 0
                    try:
                        if dict[value][0] not in dict[value + 1][1]:
                            duel_list.append([dict[value][2], dict[value + 1][2]])
                            dict.pop(value)
                            dict.pop(value + 1)
                            condition = 1
                    except:
                        pass
                    if condition == 0:
                        try:
                            if dict[value][0] not in dict[value + 2][1]:
                                duel_list.append([dict[value][2], dict[value + 2][2]])
                                dict.pop(value)
                                dict.pop(value + 2)
                                condition = 2
                        except:
                            pass
                    if condition == 0:
                        try:
                            if dict[value][0] not in dict[value + 3][1]:
                                duel_list.append([dict[value][2], dict[value + 3][2]])
                                dict.pop(value)
                                dict.pop(value + 3)
                        except:
                            pass
                except:
                    print(f"--- {value} a rencontré un problème --- ") # -DEVonly

        # Create the round
        self.object_dict[round_index] = Round(duel_list)
        # Create the match attached to this round
        self.object_dict[round_index].make_match()

        return duel_list

    def updating_scoreboard_associations(self,list_of_duel):
        """ Add the new associations to the scoreboard in order to have a meetings history
        Arg = A list of duels
        """
        associations_list = []

        for duel in list_of_duel:
            for player in self.scoreboard:
                if duel[0] == self.scoreboard[player]['reference']:
                    player2_id = self.scoreboard[player]['id']
                    associations_list.append([duel[1],player2_id])

                if duel[1] == self.scoreboard[player]['reference']:
                    player1_id = self.scoreboard[player]['id']
                    associations_list.append([duel[0],player1_id])

        for duel in associations_list:
            for player in self.scoreboard:
                if duel[0] == self.scoreboard[player]['reference']:
                    self.scoreboard[player]['associations'].append(duel[1])

        return

    def serialized_the_object(self):

        self.serialized_object = round_conversion(self.object_dict)
        self.serialized_version = {
            'name': self.name,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'num_of_round': self.num_of_round,
            'selected_players': self.selected_players,
            'game_type': self.game_type,
            'notes': self.notes,
            'serialized_object': self.serialized_object
        }
        # Deleting the old version
        for value in self._serialized_registry:
            if value['name'] == self.name:
                self._serialized_registry.remove(value)
        self._serialized_registry.append(self.serialized_version)