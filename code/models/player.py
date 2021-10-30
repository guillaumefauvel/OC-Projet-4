"""Player object"""
import json


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
        serialized_version = {
            'name': self.name,
            'first_name': self.first_name,
            'birthday': self.birthday,
            'gender': self.gender,
            'ranking': self.ranking,
            'reference': self.reference
        }
        self._serialized_registry.append(serialized_version)