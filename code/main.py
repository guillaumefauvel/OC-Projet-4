from controllers import datas_management
from controllers.controller_menu import menu_attribution
from views.view_menu import menu_proposition
from models.tournament import Tournament

def main():

    # Load the data
    datas_management.load_from_save()
    datas_management.serializing_tournament_player()

    # player_list = ["Garry Kasparov","Jean Godran","Bertrand Farse","Sven Gadzish","Arnold Noire","Martin Bernard",
    #                "Jacques Rousseau","François De Galice"]
    # def add_1_tournament():
    #     Tournament("TEST1", "PARIS", "20/10/2020", "20/10/2020",4,player_list,"Blitz","Une note")
    # add_1_tournament()

    # -DEVonly
    # datas_management.delete_duplicates()

    # Launch the menu
    menu_attribution(menu_proposition())

    # -DEVonly
    # from code.controllers.controller_tournament_manager import launch_from_controller
    # launch_from_controller(Tournament._registry[-1])

    datas_management.serializing_tournament_player()
    datas_management.save_data()


if __name__ == "__main__":
    main()

