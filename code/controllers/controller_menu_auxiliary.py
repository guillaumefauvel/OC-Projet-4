
import views.view_menu
import controllers.controller_menu


def launch_the_menu():
    controllers.controller_menu.menu_attribution(views.view_menu.menu_proposition())

    return


def navigator(num_of_the_manager):

    user_input = input("")
    if len(user_input) > 0:
        controllers.controller_menu.menu_attribution(views.view_menu.menu_proposition())
    else:
        controllers.controller_menu.menu_attribution(num_of_the_manager)

    return


def menu_loop(function):
    while True:
        function()
        response = views.view_menu.ask_menu_return()

        if response is True:
            launch_the_menu()
            break
        elif response is False:
            continue
