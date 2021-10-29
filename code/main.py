from views.view_menu import menu_proposition
from controllers.controller_menu import menu_attribution
from models import datas_management
from code.models.tournament import Tournament


def main():
    # Load the data
    # datas_management.load_sample_datas()

    # Launch the menu
    # menu_attribution(menu_proposition())

    datas_management.load_from_save()

    # from code.controllers.controller_menu import tournament_beta_purposes
    # tournament_beta_purposes()

    # -DEVonly
    # from code.controllers.controller_tournament import launch_from_controller
    # launch_from_controller(Tournament._registry[-1])

    datas_management.save_data()

if __name__ == "__main__":
    main()

