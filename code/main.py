from views.view_menu import menu_proposition
from controllers.controller_menu import menu_attribution
from models import datas_load


def main():
    # Load the data
    datas_load.load_sample_datas()

    # Launch the menu
    # menu_attribution(menu_proposition())


    from code.controllers.controller_menu import tournament_beta_purposes
    tournament_beta_purposes()

if __name__ == "__main__":
    main()