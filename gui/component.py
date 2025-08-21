from abc import ABC, abstractmethod
import pygame


class Component(ABC):
    """
    Component abstract class.
    """
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """
        Draw component.
        """
        pass

    @abstractmethod
    def update(self, event: pygame.event.Event):
        """
        Update component.
        """
        pass
