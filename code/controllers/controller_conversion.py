from models.player import Player

def convert_to_player_object(list_of_player_reference):
    """ Convert a list of player reference into a list of player object
    Arg : A list of player reference (ie: 'Garry Kasparov')
    Return : A list of player object for each player reference"""
    list_of_player_object = []
    for player_ref in list_of_player_reference:
        for player_object in Player._registry:
            if player_ref == player_object.reference:
                list_of_player_object.append(player_object)
    return list_of_player_object


def round_conversion(list_of_round):
    """ Convert a list of round object into a serialized dict
    arg : a list of round object
    return : a dict containing the duel list of a round and the atttributes of those matchs
    These informations are made in order to serialized the content of the tournament """
    serialized_dict = {}

    for value, index in zip(list_of_round, range(1, len(list_of_round) + 1)):

        round_start_time = list_of_round[value].start_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        round_end_time = list_of_round[value].end_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")

        serialized_dict[index] = [list_of_round[value].duel_list,
                                  [x.winner for x in list_of_round[value].attached_match],
                                  [x.start_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                                   for x in list_of_round[value].attached_match],
                                  [x.end_time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                                   for x in list_of_round[value].attached_match],[round_start_time,round_end_time]]

    return serialized_dict
