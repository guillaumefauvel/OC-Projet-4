"""Player object"""

class Player:

    _registry = []
    _serialized_registry = []

    def __init__(self, name, first_name, birthday, gender, ranking ):

        self._registry.append(self)
        self.name = name
        self.first_name = first_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking
        self.reference = (f"{first_name} {name}")
        self.num_of_wins = 0
        self.num_of_losses = 0
        self.num_of_draw = 0
        self.winloss_ratio = 0
        self.num_of_match = 0
        self.num_of_tournaments = 0

        self.serialized_version = {
            'name': self.name,
            'first_name': self.first_name,
            'birthday': self.birthday,
            'gender': self.gender,
            'ranking': self.ranking,
            'reference': self.reference,
            'num_of_wins': self.num_of_wins,
            'num_of_losses': self.num_of_losses,
            'num_of_draw': self.num_of_draw,
            'win_loss_ratio': self.winloss_ratio,
            'num_of_match': self.num_of_match,
            'num_of_tournaments': self.num_of_tournaments
        }
        self._serialized_registry.append(self.serialized_version)

    def update_player_datas(self):
        self.serialized_version = {
            'name': self.name,
            'first_name': self.first_name,
            'birthday': self.birthday,
            'gender': self.gender,
            'ranking': self.ranking,
            'reference': self.reference,
            'num_of_wins': self.num_of_wins,
            'num_of_losses': self.num_of_losses,
            'num_of_draw': self.num_of_draw,
            'win_loss_ratio': self.winloss_ratio,
            'num_of_match': self.num_of_match,
            'num_of_tournaments': self.num_of_tournaments
        }
        # Deleting the old version
        for value in self._serialized_registry:
            if value['reference'] == self.reference:
                self._serialized_registry.remove(value)

        self._serialized_registry.append(self.serialized_version)


