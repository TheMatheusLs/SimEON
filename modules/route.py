
class Route:
    def __init__(self, path: list = [], parent: object = None, *args, **kwargs) -> None:

        self.parent = parent

        self.Path = []

        for p in path:
            self.Path.append(p)

    def getOrN(self) -> int:
        assert(len(self.Path) > 0)
        return self.Path[0]

    def getDeN(self) -> int:
	    return self.Path[-1]

    def getNumHops(self) -> int:
        return len(self.Path) - 1

    def getNumNodes(self) -> int:
        return len(self.Path)

    def getNode(self, pos:int) -> int:
        assert((pos >= 0) and (pos < len(self.Path)))
        return self.Path[pos]

