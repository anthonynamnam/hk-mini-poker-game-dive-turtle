import os
import sys
import time
import random

from constant import *
import setting

import DisplayMode
import read
import helper
import Poker
import GameSet


class System:

    _available_option_list = [0, 1, 2, 3, 4, 5, 6]
    _play_next_game = True

    _system_ongoing = False

    _login_status = False
    _login_username = ""
    _login_score = 0
    _login_played_game = 0

    _num_of_option = 7

    _current_num_of_player = DEFAULT_NUM_PLAYER

    _default_display_mode = DisplayMode.DisplayMode.SIMPLY
    _current_display_mode = DisplayMode.DisplayMode.SIMPLY

    def __init__(self):
        self._num_of_option = len(self._available_option_list)
        self.check_data_file_exist()

    def start_system(self):
        self._system_ongoing = True
        while self._system_ongoing:
            self.print_screen()
            try:
                choice = int(
                    input(
                        f"Plese input your choice by {self.display_question_number()}: "
                    )
                )
            except:
                choice = -1
            while choice < 1 or choice > self._num_of_option:
                try:
                    print("")
                    print(f"Please input a number between 1 and {self._num_of_option}")
                    choice = int(
                        input(
                            f"Plese input your choice by {self.display_question_number()}:"
                        )
                    )
                except:
                    choice = -1

            action_choice = self._available_option_list[choice - 1]
            if action_choice == 0:
                back_to_menu = self.start_game()
                self._system_ongoing = back_to_menu
            elif action_choice == 1:
                back_to_menu = self.edit_setting()
                self._system_ongoing = back_to_menu
            elif action_choice == 2:
                back_to_menu = self.login()
                self._system_ongoing = back_to_menu
            elif action_choice == 3:
                back_to_menu = self.sign_up()
                self._system_ongoing = back_to_menu
            elif action_choice == 4:
                back_to_menu = self.logout()
                self._system_ongoing = back_to_menu
            elif action_choice == 5:
                back_to_menu = self.restart()
                self._system_ongoing = back_to_menu
            elif action_choice == 6:
                back_to_menu = self.quit()
                self._system_ongoing = back_to_menu
        sys.exit()

    def start_game(self):
        #   Initiate Game Object
        thisgame = GameSet.GameSet(login=self._login_status)
        self._system_ongoing = True

        #   Initiate Guest Player
        if self._login_status:
            thisgame.init_member_player(
                self._login_username,
                self._login_score,
                self._login_played_game,
                self._current_display_mode,
            )
        else:
            #   Ask for guest name and initiate player object for the guest
            guest_name = str(input("Please input your name:"))
            thisgame.init_guset_player(guest_name, self._current_display_mode)

        #   Initiate Other Players
        thisgame.init_other_player(self._current_num_of_player)

        #   Initiate Exchange Order
        thisgame.init_exchange_order()

        #   Display all players name
        thisgame.display_all_players_name()

        #   Initiate Game Procedure
        thisgame.init_mix_poker()
        thisgame.distribute_poker_card()

        #   Displaying guest's Cards
        print("+++++++++++++++++++++++++++++++++++++++++")
        print(
            f"Welcome {thisgame.current_player_list[0].username} ! You have {thisgame.current_player_list[0].get_current_num_of_card()} cards in your hand."
        )

        helper.display_heading("Your cards are below:", 1)
        Poker.print_lengthy_simply_hands(
            thisgame.current_player_list[0].current_lengthy_simply_hand
        )
        helper.print_text_with_time_interval(
            "Eliminating pairs in your hand...", 2, 0.8
        )
        thisgame.update_current_player()

        #   Start Exchange the Card
        helper.display_heading(
            "Card Exchange Procedure Start!!!     Card Exchange Procedure Start!!!", 0,
        )

        while not thisgame.game_ended:
            print(
                ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            )
            thisgame.turn = thisgame.turn + 1
            #   Display Turn Number
            if setting.Waiting:
                time.sleep(0.6)
            thisgame.display_turn_number()

            #   Displaying all players' cards
            thisgame.display_guest_player_cards()
            for x in range(1, len(thisgame.current_player_list)):
                if thisgame.current_player_list[x].in_game:
                    thisgame.display_number_of_card_by_index(x)
                else:
                    thisgame.display_card_of_player_by_index(x)

            #   Display Current Player List
            if setting.Waiting:
                time.sleep(0.7)
            thisgame.display_current_players_name()

            #   Exchange Card
            thisgame.exchange_card()

            #   Update the card in Players' hand
            thisgame.update_current_player()

            #   Check if anyone win
            thisgame.check_if_anyone_win()

            #   Check if the game ended
            if thisgame.check_if_game_ended():
                print("")
                textprint = "The game is ended!  The game is ended  The game is ended  The game is ended"
                helper.display_heading(textprint, 0)
                helper.display_heading(textprint, 0)
                print("")
                break
            else:
                print("")
        thisgame.show_win_lose()

        print("====================The Game is ended======================")
        thisgame.reset_game()
        return True

    def edit_setting(self):
        print("")
        print("1) Number of Player \t2) Display Mode")
        edit_choice = int(input("Which one to edit? Please select the options above."))
        while edit_choice != 1 and edit_choice != 2:
            print("")
            print(f"Please input the number 1 or 2!!!")
            print(f"1) Number of Player \t2) Display Mode")
            edit_choice = int(
                input(f"Which one to edit? Please select the options above.")
            )
        if edit_choice == 1:
            print("")
            updated_number_of_players = int(
                input(
                    f"How many player you want? (Min: {MIN_NUM_PLAYER} / Max: {MAX_NUM_PLAYER})"
                )
            )
            while (
                updated_number_of_players < MIN_NUM_PLAYER
                or updated_number_of_players > MAX_NUM_PLAYER
            ):
                print("")
                print(
                    f"We only allow to have {MIN_NUM_PLAYER}~{MAX_NUM_PLAYER} people."
                )
                updated_number_of_players = int(
                    input(
                        f"How many player you want? (Min: {MIN_NUM_PLAYER} / Max: {MAX_NUM_PLAYER})"
                    )
                )
            self._current_num_of_player = updated_number_of_players
        elif edit_choice == 2:
            print("")
            print("1) Simply Mode \t2) Lengthy Mode")
            updated_display_mode = int(input("Which mode do you want to play?"))
            while updated_display_mode != 1 and updated_display_mode != 2:
                print("")
                print("Please input the number 1 or 2!!!")
                print("1) Simply Mode \t2) Lengthy Mode")
                updated_display_mode = int(input("Which mode do you want to play?"))
            if updated_display_mode == 1:
                helper.print_text_with_time_interval(
                    "Switching to Simply Mode...",
                    random.randint(3, 5),
                    random.randint(30, 48) / 100,
                )
                self._current_display_mode = DisplayMode.DisplayMode.SIMPLY
                print("\t   Switched to Simply Mode!!!")
                print("")
            elif updated_display_mode == 2:
                helper.print_text_with_time_interval(
                    "Switching to Lengthy Mode...",
                    random.randint(3, 5),
                    random.randint(30, 48) / 100,
                )
                self._current_display_mode = DisplayMode.DisplayMode.LENGTHY
                print("\t   Switched to Lengthy Mode!!!")
                print("")

        return True

    def login(self):
        fail_time = 0
        if self._login_status == True:
            print("")
            helper.display_heading("You have logged in already!!!", 1)
            helper.display_heading("Please log out to switch to another account!!!", 0)
            print("")
        else:
            print("")
            print("=========================================")
            print("｜\t\t\t\t\t｜")
            print("｜   Welcome to our Membership System\t｜")
            print("｜    Please Login to your account\t｜")
            print("｜\t\t\t\t\t｜")
            print("=========================================")
            helper.display_heading("Please enter your username below.", 1)
            input_username = input("Username: ")
            while (not read.check_if_username_used(input_username)) and fail_time < 3:
                print("System Message: Username Not Found!!")
                fail_time += 1
                if fail_time < 3:
                    print("")
                    helper.display_heading("Please enter your username below.", 1)
                    input_username = input("Username: ")
            print("")
            if fail_time < 3:
                helper.display_heading("Please enter your password below.", 1)
                input_password = input("Password: ")

                helper.print_text_with_time_interval(
                    "logging in...", random.randint(2, 5), 0.35
                )

                if read.check_if_login_correct(input_username, input_password):
                    target_user_id = read.get_user_id_by_username(input_username)
                    helper.display_heading("Loged in Successfully!!", 1)
                    print("")
                    if setting.Waiting:
                        time.sleep(0.7)
                    self._login_status = True
                    self._login_username = input_username
                    self._login_score = read.get_score_by_username(input_username)
                    self._login_played_game = read.get_played_game_by_username(
                        input_username
                    )
                else:
                    helper.display_heading("Wrong Password!!", 1)
        return True

    def sign_up(self):
        if self._login_status:
            print("System Message: You have to sign out for register a new account")
        else:
            add_success = False
            while not add_success:
                #   Ask for new Username and Password
                print("")
                print("Please input the username: (4~16 characters)")
                username = input("")
                while (
                    len(username) < 4 or len(username) > 16
                ) or helper.check_if_any_space(username):
                    print("Please input the username: (4~16 characters)")
                    username = input("")
                print("Please input the password: (8~16 characters)")
                password = input("")
                while (
                    len(password) < 8 or len(password) > 16
                ) or helper.check_if_any_space(password):
                    print("Please input the password: (8~16 characters)")
                    password = input("")

                #   Add Account into file
                add_success = read.add_account(username, password)
            input("Please click enter to continue...")

        return True

    def logout(self):
        if not self._login_status:
            print("System Message: You have not logged in yet")
        else:
            if self._login_status:
                self._login_status = False
                helper.display_heading("Successfully Logged Out!!!", 1)
            self._login_username = ""
            self._login_score = 0
            self._login_played_game = 0

        return True

    def restart(self):
        if self._login_status:
            self._login_status = False
            self._login_username = ""
            self._login_score = 0
            self._login_played_game = 0
        self._current_num_of_player = DEFAULT_NUM_PLAYER
        self._current_display_mode = self._default_display_mode
        helper.print_text_with_time_interval(
            "Shuting Down...", random.randint(2, 4), random.randint(25, 40) / 100
        )
        helper.print_text_with_time_interval(
            "Restarting...", random.randint(3, 6), random.randint(28, 50) / 100
        )

        return True

    def quit(self):
        helper.print_text_with_time_interval(
            "Shuting Down...", random.randint(2, 4), random.randint(25, 40) / 100
        )
        helper.print_text_with_time_interval("System Shut Down!", 1, 0)
        return False

    def check_data_file_exist(self):
        if os.path.exists(setting.UserAccPath) and not os.path.exists(
            setting.UserInfoPath
        ):
            newfile2 = open(setting.UserInfoPath, "w")
            newfile2.write("UserID	LoginID		Score   PlayedGame\n")
            newfile2.close()
        elif not os.path.exists(setting.UserAccPath) and os.path.exists(
            setting.UserInfoPath
        ):
            newfile1 = open(setting.UserAccPath, "w")
            newfile1.write("UserID	LoginID		Password\n")
            newfile1.close()
        elif not os.path.exists(setting.UserAccPath) and not os.path.exists(
            setting.UserInfoPath
        ):
            newfile1 = open(setting.UserAccPath, "w")
            newfile1.write("UserID	LoginID		Password\n")
            newfile1.close()
            newfile2 = open(setting.UserInfoPath, "w")
            newfile2.write("UserID	LoginID		Score   PlayedGame\n")
            newfile2.close()

    def print_screen(self):
        if self._login_status:
            self._available_option_list = [0, 1, 4, 5, 6]
        else:
            self._available_option_list = [0, 1, 2, 3, 5, 6]
        self._num_of_option = len(self._available_option_list)
        print("")
        helper.print_border()
        helper.print_line("")
        helper.print_line("Welcome to our Poker Game")
        helper.print_line("「潛」烏龜", cut_space=5)
        helper.print_line("")
        if self._login_status:
            self._login_score = read.get_score_by_username(self._login_username)
            self._login_played_game = read.get_played_game_by_username(
                self._login_username
            )
            helper.print_line(
                f"Logged in as: {self._login_username}{' '*5}", left_more_right=8,
            )
            helper.print_line(
                f"Your Score: {self._login_score}{' '*10}Played Game: {self._login_played_game}"
            )
            helper.print_line("")
        helper.print_line("Game Setting:")
        helper.print_line(f"Number of Player: {self._current_num_of_player}")
        if self._current_display_mode == DisplayMode.DisplayMode.SIMPLY:
            helper.print_line(f" Display Mode: Simply")
        elif self._current_display_mode == DisplayMode.DisplayMode.LENGTHY:
            helper.print_line(f" Display Mode: Lengthy")
        helper.print_line("")
        helper.print_line(
            f"1. {OPTION_LIST[self._available_option_list[0]]}{' '*5}2. {OPTION_LIST[self._available_option_list[1]]}"
        )
        for i in range(2, len(self._available_option_list) - 2, 1):
            helper.print_line(f"{i+1}. {OPTION_LIST[self._available_option_list[i]]}")
        helper.print_line(
            f"{len(self._available_option_list)-1}. {OPTION_LIST[self._available_option_list[-2]]}{' '*5}{len(self._available_option_list)}. {OPTION_LIST[self._available_option_list[-1]]}"
        )
        helper.print_line("")
        helper.print_border()

    def display_question_number(self):
        string = ""
        for x in range(0, len(self._available_option_list)):
            string = string + str(x + 1)
            if x != (self._num_of_option - 1):
                string = string + "/"
        return string

