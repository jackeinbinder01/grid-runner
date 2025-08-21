from enum import Enum, auto


class RunState(Enum):
    """
    Play/Pause game state
    """
    GO = auto()
    PLAY = auto()
    PAUSE = auto()
    FINISHED = auto()
    HALTED = auto()

    def __str__(self):
        """
        Get enum name.
        """
        return self.name
