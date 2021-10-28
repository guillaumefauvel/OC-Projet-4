import collections
from tinydb import TinyDB, Query
from code.controllers.controller_tournament import player_researcher

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
        self.scoreboard = ""
        self.nested_list = [] #
        self.ranked_dict = {}

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
        self.scoreboard = TinyDB('scoreboard.json')
        if (len(self.scoreboard)) < 1: ## BETA ONLY
            def add_to_database(rank,ref,ID):
                self.scoreboard.insert({'Classement':rank,'Reference': ref, 'ID':ID, "Score": 0,
                                        "Classement-Score": 0, "Association(s)":[]})
            for index in self.ranked_dict:
                add_to_database(index,self.ranked_dict[index][0],index)


    def sort_score_rank(self):
        """Sort the json file based on his 'Classement-Score' key"""
        pass

    def first_draw(self):
        """ Generate the first list of duel """

        self.NUM_OF_DUEL = int(len(self.scoreboard)/2)
        self.duel_list = []

        for index in range(self.NUM_OF_DUEL):

            results = []
            player_1 = self.scoreboard.search(Query().Classement == index+1)
            player_2 = self.scoreboard.search(Query().Classement == index+1+self.NUM_OF_DUEL)

            results.append(player_1[0]['Reference'])
            results.append(player_2[0]['Reference'])
            self.duel_list.append(results)

            # Write the duel associations into the scoreboard
            self.scoreboard.update({'Association(s)': player_2[0]['ID']},
                                   Query().Reference == player_1[0]['Reference'])
            self.scoreboard.update({'Association(s)': player_1[0]['ID']},
                                   Query().Reference == player_2[0]['Reference'])

        # -DEVonly
        for value in self.scoreboard:
            print(value)

        return




    def duel_generator(self):
        NUM_OF_DUEL = len(self.scoreboard)/2


        # User = Query()
        # def search():
        #     results = self.scoreboard.search(User.Classement == 1)
        #     print("")
        #     print(results)
        #     return


        # search()

        #
        # def update():
        #     scoreboard.update({'age': 26}, User.name == 'Max')
        #
        #     results = scoreboard.search(User.name == 'Max')
        #     for res in results:
        #         res['age'] = 27
        #     scoreboard.write_back(results)
        #
        # self.scoreboard.purge()
        pass

    def launch(self):

        # Sort the player by making an ordered dict
        self.return_ranking()
        # Use the ordered dict in order to create the scoreboard
        self.scoreboard_maker()
        self.scoreboard.purge() # -DEVonly
        self.scoreboard_maker() # -DEVonly
        # Generate the first series of duel thanks to the scoreboard
        self.first_draw()
        # Write the duel association into the scoreboard

        # Generate the next series of duel thanks to the scoreboard

        pass



