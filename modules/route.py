


class Route:
    def __init__(self, path, parent, *args, **kwargs) -> None:

        self.parent = parent

        self.Path = path.copy()

    
    def getNumHops(self) -> int:
        return len(self.Path) - 1

    def getNode(self, pos:int) -> int:
        return self.Path[pos]