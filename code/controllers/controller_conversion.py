from models.player import Player

def convert_to_player_object(list_of_player_reference):
    """ Convert a list of player reference into a list of player object """
    list_of_player_object = []
    for player_ref in list_of_player_reference:
        for player_object in Player._registry:
            if player_ref == player_object.reference:
                list_of_player_object.append(player_object)
    return list_of_player_object

def round_conversion(list_of_round):
    """ Convert a list of round object into a serialized dict
    arg : a list of round object
    return : a dict containing the duel list of a round and the result of those matchs
    These informations are in order to serialized the content of the tournament """
    serialized_dict = {}

    for value, index in zip(list_of_round, range(1, len(list_of_round) + 1)):
        serialized_dict[index] = [list_of_round[value].duel_list,
                                  [x.winner for x in list_of_round[value].attached_match]]

    return serialized_dict