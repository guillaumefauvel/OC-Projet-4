from controllers import datas_management
from controllers.controller_menu import menu_attribution
from views.view_menu import menu_proposition
from models.tournament import Tournament

def main():
    # Load the data
    datas_management.load_from_save()

    # DEVonly
    from controllers.datas_management import serializing_tournament_player
    serializing_tournament_player()

    # Launch the menu
    # menu_attribution(menu_proposition())

    # -DEVonly
    from code.controllers.controller_tournament import launch_from_controller
    launch_from_controller(Tournament._registry[-1])

    # -DEVonly
    # from controllers.controller_report_manager import sort_by_rank, sort_by_age
    # sort_by_rank()
    # sort_by_age()
    # sort_by_age()

    datas_management.save_data()

if __name__ == "__main__":
    main()

