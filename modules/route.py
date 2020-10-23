


class Route:
    def __init__(self, path, parent, *args, **kwargs) -> None:

        self.parent = parent

        self.Path = path.copy()