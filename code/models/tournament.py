""" Tournament object """

import itertools
import collections
from models.round import Round
from controllers.controller_conversion import convert_to_player_object, round_conversion


class Tournament:
    """ A tournament object is initialised by the user """
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
        self.serialized_version = {}

    def return_ranking(self):
        """ Return a ordered dictionnary that contains participants informations
        key=index, value1 = player.reference """

        raw_rank = {}
        for player in self.players_object:
            raw_rank[player.ranking] = player.reference
        ordered_dict = collections.OrderedDict(sorted(raw_rank.items()))

        for player, index, in zip(ordered_dict, range(1, len(self.players_object) + 1)):
            self.scoreboard[index] = {"reference": ordered_dict[player], "id": index, "scorerank": 0,
                                      "score": 0, "associations": []}

    def sort_score_rank(self):
        # """Sort the json file based on his 'Classement-Score' key"""
        for line, rank in zip(sorted(self.scoreboard.values(), key=lambda k: k['score'],
                                     reverse=True), range(1, len(self.players_object)+1)):
            line['scorerank'] = rank
        return

    def first_draw(self):
        """ Generate the first list of duel by analysing the scoreboard database """

        duel_list = []

        for index in range(1, self.num_of_duel+1):
            results = []
            player_1 = self.scoreboard[index]
            player_2 = self.scoreboard[index + self.num_of_duel]

            results.append(player_1['reference'])
            results.append(player_2['reference'])
            duel_list.append(results)

            player_1['associations'].append(player_2['id'])
            player_2['associations'].append(player_1['id'])

        # Create the round
        self.object_dict[1] = Round(duel_list)
        # Create the match attached to this round
        self.object_dict[1].make_match()
        return duel_list

    def updating_scoreboard_score(self, round_obj_index):
        """ Update the score of the scoreboard
        Arg : the round index
        Return : nothing, modification of the scoreboard file
        """

        list_of_winner = []
        list_of_equality = []

        for match in self.object_dict[round_obj_index].attached_match:
            if match.winner == "1":
                list_of_winner.append(match.player_1)
            elif match.winner == "2":
                list_of_winner.append(match.player_2)
            else:
                list_of_equality.append(match.player_1)
                list_of_equality.append(match.player_2)

        for player in self.scoreboard.values():
            if player['reference'] in list_of_winner:
                player['score'] = player['score']+1
            if player['reference'] in list_of_equality:
                player['score'] = player['score']+0.5

    def generating_other_draw(self, round_index):
        """ Generate a list of duel by analysing the scoreboard database, it also make a round and some matchs
        Arg : The round index - in order to link the round to his tournament
        Return : The list of the next duels """

        short_term_dict = {}
        duel_list = []
        player_to_match = []

        for value, index in zip(sorted(self.scoreboard.values(), key=lambda k: k['score'], reverse=True),
                                range(1, len(self.scoreboard)+1)):
            short_term_dict[index] = value['id'], value['associations'], value['reference']

        for value in list(short_term_dict):
            if value not in list(short_term_dict):
                pass
            else:
                index = 0
                while True:
                    index += 1
                    try:
                        if index > len(self.scoreboard):
                            player_to_match.append(value)
                            break
                        if short_term_dict[value][0] not in short_term_dict[value + index][1]:
                            duel_list.append([short_term_dict[value][2], short_term_dict[value + index][2]])
                            short_term_dict.pop(value)
                            short_term_dict.pop(value + index)
                            break
                    except KeyError:
                        pass

        # If the fastest attribution method didn't work we use another method.
        if len(short_term_dict) > 0:
            duel_list = self.scoreboard_converter(self.swiss_pairing())

        self.object_dict[round_index] = Round(duel_list)
        self.object_dict[round_index].make_match()

        return duel_list

    def swiss_pairing(self):
        """ Only used if the first pairing method didn't find every matchs
        Return : A list of duel based on the sorted scoreboard index """

        scoreboard_dict = {}

        for value, index in zip(sorted(self.scoreboard.values(), key=lambda k: k['score'], reverse=True),
                                range(1, len(self.scoreboard)+1)):
            scoreboard_dict[index] = value['id'], value['associations'], value['reference'], value['score']

        general_list = []
        general_score = []

        for index in range(1, len(self.scoreboard)+1):
            for index2 in range(1, len(self.scoreboard) + 1):
                general_list.append([index, index2])

        for value in general_list:
            player_1 = scoreboard_dict[value[0]]
            player_2 = scoreboard_dict[value[1]]
            player_1_id = player_1[0]
            player_2_id = player_2[0]
            player_1_score = player_1[3]
            player_2_score = player_2[3]

            player_2_association = player_2[1]
            if player_1_id in player_2_association:
                association_score = 100
                general_score.append(association_score)
            elif player_1_id == player_2_id:
                association_score = 200
                general_score.append(association_score)
            elif player_1_id not in player_2_association and player_1_id != player_2_id:
                association_score = player_1_score-player_2_score
                general_score.append(association_score)

        new_dict = {}
        for association, score, index in zip(general_list, general_score, range(1, len(general_list)+1)):
            new_dict[index] = association, score

        lowest_score = 200
        best_combination = []
        for i in itertools.permutations([v for v in range(1, len(self.selected_players)+1, 1)]):
            if i[0] == 1:
                score = 0
                output = [i[v:v + 2] for v in range(0, len(i), 2)]
                for value in output:
                    for combi in new_dict:
                        if new_dict[combi][0] == list(value):
                            score += (new_dict[combi][1])
                if 0 < score < lowest_score:
                    lowest_score = score
                    best_combination = output
            else:
                break

        return best_combination

    def scoreboard_converter(self, best_combination):
        """ Convert a list of duel logged as scoreboard_index into a list of player_reference
        Args : A list of scoreboard index generated by the swiss_pairing method
        Return : The list of the next duel, a list of list containing the player's reference."""
        duel_list = []
        scoreboard = sorted(self.scoreboard.values(), key=lambda k: k['score'], reverse=True)

        for value in best_combination:
            value_1 = value[0]
            value_2 = value[1]
            duel = []
            for player in scoreboard:
                if player['scorerank'] == value_1:
                    duel.append(player['reference'])
                if player['scorerank'] == value_2:
                    duel.append(player['reference'])
            duel_list.append(duel)

        return duel_list

    def updating_scoreboard_associations(self, list_of_duel):
        """ Add the new associations to the scoreboard in order to have a meetings history
        Arg = A list of duels
        """
        associations_list = []

        for duel in list_of_duel:
            for player in self.scoreboard:
                if duel[0] == self.scoreboard[player]['reference']:
                    player2_id = self.scoreboard[player]['id']
                    associations_list.append([duel[1], player2_id])

                if duel[1] == self.scoreboard[player]['reference']:
                    player1_id = self.scoreboard[player]['id']
                    associations_list.append([duel[0], player1_id])

        for duel in associations_list:
            for player in self.scoreboard:
                if duel[0] == self.scoreboard[player]['reference']:
                    self.scoreboard[player]['associations'].append(duel[1])

        return

    def serialized_the_object(self):
        """ Replace the former serialized tournament by an updated version """

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
            'serialized_object': self.serialized_object,
            'scoreboard': self.scoreboard
        }
        for value in self._serialized_registry:
            if value['name'] == self.name:
                self._serialized_registry.remove(value)

        self._serialized_registry.append(self.serialized_version)
