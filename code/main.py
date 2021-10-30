from code.controllers import datas_management
from code.controllers.controller_menu import menu_attribution
from code.views.view_menu import menu_proposition
from code.models.player import Player

def main():
    # Load the data
    datas_management.load_sample_datas()
    # datas_management.load_from_save()
    # for value in Player._serialized_registry:
    #     print(value)
    # Launch the menu
    menu_attribution(menu_proposition())


    # from code.controllers.controller_menu import tournament_beta_purposes
    # tournament_beta_purposes()

    # -DEVonly
    # from code.controllers.controller_tournament import launch_from_controller
    # launch_from_controller(Tournament._registry[-1])

    datas_management.save_data()
    datas_management.save_date_tournament()

if __name__ == "__main__":
    main()

