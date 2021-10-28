"""Player object"""

class Player:

    _registry = []

    def __init__(self, name, first_name, birthday, gender, ranking ):

        self._registry.append(self)
        self.name = name
        self.first_name = first_name
        self.birthday = birthday
        self.gender = gender
        self.ranking = ranking
        # self.reference = (self.name+"."+self.first_name).replace(" ","").lower()
        self.reference = (f"{first_name} {name}")