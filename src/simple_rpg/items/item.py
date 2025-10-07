class Item:
    def __init__(self, name, description, value):
        self._name = name
        self._description = description
        self._value = value

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def get_value(self):
        return self._value
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self._name,
            "description": self._description,
            "value" : self._value
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["description"], data["value"])
    
    def __str__(self):
        return (f"{self.get_name()}\n"
                f"Description: {self.get_description()}\n"
                f"Value: {self.get_value()} gold")

    def __repr__(self):
        return (f"Item(name={self.get_name()!r}, "
                f"description={self.get_description()!r}, "
                f"value={self.get_value()})")
    
    def __eq__(self, value):
        return (
            (self._name == value.get_name()) and
            (self._description == value.get_description()) and
            (self._value == value.get_value())
        )
    

