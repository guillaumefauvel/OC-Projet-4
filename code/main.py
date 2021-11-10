from controllers import datas_management
from controllers.controller_menu import menu_attribution
from views.view_menu import menu_proposition


def main():

    datas_management.load_from_save()
    datas_management.serializing_tournament_player()

    menu_attribution(menu_proposition())

    datas_management.serializing_tournament_player()
    datas_management.save_data()

if __name__ == "__main__":
    main()
