from controllers import datas_management
from controllers.controller_menu import menu_attribution
from views.view_menu import menu_proposition
from models.tournament import Tournament


def main():

    datas_management.load_from_save()
    datas_management.serializing_tournament_player()

    # -DEVonly
    # datas_management.delete_duplicates()

    menu_attribution(menu_proposition())

    # -DEVonly
    # from code.controllers.controller_tournament_manager import launch_from_controller
    # launch_from_controller(Tournament._registry[-1])


    datas_management.serializing_tournament_player()
    datas_management.save_data()


if __name__ == "__main__":
    main()
