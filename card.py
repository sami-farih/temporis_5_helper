from globalvars import img_path


class Card:
    def __init__(self, id_: int, name_: str):
        self.id = id_
        self.name = name_
        self.img_path = f"{img_path}{id_}.png"
        self.drop = "-"
