import pygame


def init_pygame() -> None:
    """
    Helper to initialize pygame.
    """
    pygame.init()
    pygame.font.init()


def handle_quit_events() -> None:
    """
    Handle quit.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
