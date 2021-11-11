
import views.view_menu as vm
import controllers.controller_menu as cm

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

    cm.menu_attribution(vm.menu_proposition())

    return

def navigator(num_of_the_manager,mode):
    """ Provide a navigation solution by either going back to the
    menu or going back to the parent manager.
    Args : The index of the manager, the selected_mode """
    if mode == 1:
        user_input = input("")
        if len(user_input) > 0:
            cm.menu_attribution(vm.menu_proposition())
        else:
            cm.menu_attribution(num_of_the_manager)
    if mode == 2:
        cm.menu_attribution(num_of_the_manager)
    if mode == 3:
        cm.menu_attribution(vm.menu_proposition())

    return

def menu_loop(function):
    """ Ask the user if he want to go back to the menu. if he choose not to
    the function passed as an argument is called.
    Arg : a function"""
    while True:

        response = vm.ask_menu_return()

        if response is True:
            launch_the_menu()
            break
        elif response is False:
            return function()

