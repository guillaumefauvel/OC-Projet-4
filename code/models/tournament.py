import collections
from tinydb import TinyDB, Query
from code.models.round import Round
from code.controllers.controller_tournament import convert_to_player_object, round_conversion

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
        self.scoreboard = ""
        self.ranked_dict = {}
        self.object_dict = {} # To translate in V2
        self.serialized_object = {}
        serialized_version = {
            'name': self.name,
            'location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'num_of_round': self.num_of_round,
            'selected_players': self.selected_players,
            'game_type':self.game_type,
            'notes':self.notes
        }
        self._serialized_registry.append(serialized_version)

    def return_ranking(self):
        """ Return a ordered dictionnary that contains participants informations
        key=index, value1 = player.reference """

        raw_rank = {}

        for player in self.players_object:
            raw_rank[player.ranking] = player.reference
        ordered_dict = collections.OrderedDict(sorted(raw_rank.items()))

        for player, index, in zip(ordered_dict, range(1, len(self.players_object) + 1)):
            self.ranked_dict[index] = ordered_dict[player],

        return

    def scoreboard_maker(self):
        """ Create the scoreboard by using a sorting dict """
        self.scoreboard = TinyDB('scoreboard.json', indent=1)
        if (len(self.scoreboard)) < 1: ## -DEVonly
            def add_to_database(rank,ref,ID):
                self.scoreboard.insert({'Classement':rank,'Reference': ref, 'ID':ID, "Score": 0,
                                        "ClassementScore": 0, "Association(s)":[]})
            for index in self.ranked_dict:
                add_to_database(index,self.ranked_dict[index][0],index)

    def sort_score_rank(self):
        """Sort the json file based on his 'Classement-Score' key"""
        for line, rank in zip(sorted(self.scoreboard, key=lambda k: k['Score'],
                                     reverse=True),range(1,len(self.players_object)+1)):
            self.scoreboard.update({'ClassementScore': rank},
                                   Query().Reference == line['Reference'])

        return

    def first_draw(self):
        """ Generate the first list of duel by analysing the scoreboard database """

        self.duel_list = []

        for index in range(self.num_of_duel):

            results = []
            player_1 = self.scoreboard.search(Query().Classement == index+1)
            player_2 = self.scoreboard.search(Query().Classement == index+1+self.num_of_duel)

            results.append(player_1[0]['Reference'])
            results.append(player_2[0]['Reference'])
            self.duel_list.append(results)

            # Write the duel associations into the scoreboard
            self.scoreboard.update({'Association(s)': [player_2[0]['ID']]},
                                   Query().Reference == player_1[0]['Reference'])
            self.scoreboard.update({'Association(s)': [player_1[0]['ID']]},
                                   Query().Reference == player_2[0]['Reference'])


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

    def generating_other_draw(self,round_index):
        """ Generate a list of duel by analysing the scoreboard database, it also make a round and some matchs
        Arg : The round index - in order to link the round to his tournament
        Return : The list of the duels """

        dict = {}
        duel_list = []

        for value, index in zip(sorted(self.scoreboard, key=lambda k: k['Score'],reverse=True),range(1,len(self.scoreboard)+1)):
            dict[index] = value['ID'],value['Association(s)'],value['Reference']

        for value in list(dict):
            if value not in list(dict):
                pass
            else:
                # print(f"Travaux sur la valeur : {dict[value][2]}")
                try:
                    condition = 0
                    try:
                        if dict[value][0] not in dict[value + 1][1]:
                            duel_list.append([dict[value][2], dict[value + 1][2]])
                            # print([dict[value][2], dict[value + 1][2]])
                            dict.pop(value)
                            dict.pop(value + 1)
                            condition = 1
                            # print("It's a match V1")
                    except:
                        # print("Erreur stade 1")
                        pass
                    if condition == 0:
                        try:
                            if dict[value][0] not in dict[value + 2][1]:
                                duel_list.append([dict[value][2], dict[value + 2][2]])
                                # print([dict[value][2], dict[value + 2][2]])
                                dict.pop(value)
                                dict.pop(value + 2)
                                condition = 2
                                # print("It's a match V2")
                        except:
                            # print("Erreur stade 2")
                            pass
                    if condition == 0:
                        try:
                            if dict[value][0] not in dict[value + 3][1]:
                                duel_list.append([dict[value][2], dict[value + 3][2]])
                                # print([dict[value][2], dict[value + 3][2]])
                                dict.pop(value)
                                dict.pop(value + 3)
                                # print("It's a match V3")
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

        list_of_duel_plus = []

        for value in list_of_duel:
            list_of_duel_plus.append([value[0], value[1]])
            list_of_duel_plus.append([value[1], value[0]])

        for player, pair in zip(sorted(self.scoreboard, key=lambda k: k['Score'],reverse=True),list_of_duel_plus):
            # Searching the old associations for the player
            associations_p1 = self.scoreboard.search(Query().Reference == pair[0])[0]['Association(s)']
            # finding the ID of the player2
            p2_id = self.scoreboard.search(Query().Reference == pair[1])[0]['ID']
            associations_p1.append(p2_id)
            # updating the new asssociations to the scoreboard
            self.scoreboard.update({'Association(s)': associations_p1}, Query().Reference == pair[0])

        return

    def serialized_the_object(self):
        self.serialized_object = round_conversion(self.object_dict)