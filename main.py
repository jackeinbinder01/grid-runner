from controller.controller import Controller


def main():

    controller = Controller()
    controller.set_scoring_rules(
        coin_reward=controller.window.coin_grp_display.value,
        trash_reward=controller.window.trash_grp_display.value
    )
    controller.run()


if __name__ == '__main__':
    main()
