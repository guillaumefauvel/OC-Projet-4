
import views.view_menu
import controllers.controller_menu
from controllers.controller_tournament_manager import tournament_manager
from controllers.controller_reports_manager import reports_manager
from controllers.controller_players_manager import players_manager


def menu_attribution(response):
    """ Receive the user's choice and redirect the user towards the wanted manager
    Arg : A int number between 1 and 4 """
    if response == 1:
        tournament_manager()
    elif response == 2:
        players_manager()
    elif response == 3:
        reports_manager()
    elif response == 4:
        pass

def launch_the_menu():
    """ Show the menu proposition to the user and ask for their answer """

    controllers.controller_menu.menu_attribution(views.view_menu.menu_proposition())

    return


def navigator(num_of_the_manager):
    """ Provide a navigation solution by either going back to the
    menu or going back to the parent manager. The user need to press enter
    if he want to go back to the parent manager. However if he want to go
    to the menu he need to enter more than just nothing.
    Arg : The index of the manager """
    user_input = input("")
    if len(user_input) > 0:
        controllers.controller_menu.menu_attribution(views.view_menu.menu_proposition())
    else:
        controllers.controller_menu.menu_attribution(num_of_the_manager)

    return


def menu_loop(function):
    """ Ask the user if he want to go back to the menu. if he choose not to
    the function passed as an argument is called again.
    Arg : a function"""
    while True:
        function()
        response = views.view_menu.ask_menu_return()

        if response is True:
            launch_the_menu()
            break
        elif response is False:
            continue
