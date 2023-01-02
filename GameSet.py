import time
import random

from constant import *
import setting

import helper
import Poker
import read
import Player


class GameSet:
    poker_set = []
    start_player_list = []
    current_player_list = []
    win_player_list = []
    lose_player_list = []
    exchange_order = []
    current_draw_index = 0
    turtle_card = 0
    system_login_index = False
    turn = 0

    #   Initiate Game Set
    def __init__(self, login=False):
        self.game_ended = False
        self.system_login_index = login

    #   Reset the game
    def reset_game(self):
        self.poker_set.clear()
        self.start_player_list.clear()
        self.current_player_list.clear()
        self.win_player_list.clear()
        self.lose_player_list.clear()
        self.exchange_order.clear()
        self.current_draw_index = 0
        self.turn = 0
        self.turtle_card = 0
        self.game_ended = False

    #   Reset the game for next game
    def reset_game_to_next_game(self):
        self.poker_set = []
        self.current_player_list.clear()
        #   Reset the Player Status
        for x in range(len(self.start_player_list)):
            self.start_player_list[x].insert_hands([],)
            self.start_player_list[x].previousscore = self.start_player_list[x].score
            self.start_player_list[x].in_game = True
            self.current_player_list.append(self.start_player_list[x])
        self.win_player_list.clear()
        self.lose_player_list.clear()
        self.exchange_order.clear()
        self.current_draw_index = 0
        self.turn = 0
        self.turtle_card = 0
        self.game_ended = False

    #   Initiate the guest player
    def init_guset_player(self, guest_player_name, display_mode):
        new_player = Player.Player(guest_player_name, display_mode)
        self.start_player_list.append(new_player)
        self.current_player_list.append(new_player)

    #   Initiate member player
    def init_member_player(self, player_name, score, played_game, display_mode):
        new_player = Player.Player(player_name, score, played_game, display_mode)
        self.start_player_list.append(new_player)
        self.current_player_list.append(new_player)

    #   Initiate all the other player
    def init_other_player(self, num_of_player):
        already_used = []
        for s in range(len(COMPUTER_PLAYER_LIST)):
            already_used.append(False)

        while len(self.start_player_list) != num_of_player:
            pc_index = int(random.randint(0, len(COMPUTER_PLAYER_LIST) - 1))
            if not already_used[pc_index]:
                pc_player = Player.Player(COMPUTER_PLAYER_LIST[pc_index])
                already_used[pc_index] = True
                self.start_player_list.append(pc_player)
                self.current_player_list.append(pc_player)

    #   Starting Mixing Poker
    def init_mix_poker(self):
        self.poker_set = Poker.Poker()
        return

    def distribute_poker_card(self):
        self.turtle_card = self.poker_set.get_turtle_card()

        players_cards = self.poker_set.distribute_poker(len(self.current_player_list))
        for player, cards in zip(self.current_player_list, players_cards):
            player.insert_hands(cards, eliminate=False)

        #   Select the starting draw index, player with the least card start first
        minCard = self.current_player_list[
            self.exchange_order[self.current_draw_index] - 1
        ].get_current_num_of_card()
        for x in range(1, len(self.current_player_list)):
            if (
                self.current_player_list[
                    self.exchange_order[x] - 1
                ].get_current_num_of_card()
                < minCard
            ):
                self.current_draw_index = x

    #   Generate the exchange order
    def init_exchange_order(self):
        num_of_player = len(self.start_player_list)
        while len(self.exchange_order) != num_of_player:
            randnum = random.randint(1, num_of_player)
            if randnum not in self.exchange_order:
                self.exchange_order.append(randnum)
        self.current_draw_index = 0

    #   Count the total number of card
    def get_total_card_in_game(self):
        total = 0
        for x in range(len(self.current_player_list)):
            total = total + self.current_player_list[x].get_current_num_of_card()
        return total

    #   Count the total number of player in game
    def get_total_player_in_game(self):
        return len(self.current_player_list)

    #   Get the current player index by inputting the origianal player index
    def get_current_index_by_start_index(self, start_index):
        target_player = self.start_player_list[start_index].username
        for y in range(0, len(self.current_player_list)):
            if self.current_player_list[y].username == target_player:
                return y
        return -1

    #   Update the current players' hand
    def update_current_player(self):
        for x in range(0, len(self.current_player_list)):
            self.current_player_list[x].update_all_hands()

    #   Set the player to win
    def set_player_win(self, player_index):
        index_in_current = self.get_current_index_by_start_index(player_index)
        if index_in_current == -1:
            print(f"The player is not in the current game.")
        else:
            helper.display_heading(
                f"Player {player_index + 1} ({self.start_player_list[player_index].username}) wins the game.",
                1,
            )
            self.start_player_list[player_index].in_game = False
            self.current_player_list[index_in_current].in_game = False
            num_of_player = len(self.current_player_list)
            # self.start_player_list[PlayerIndex].add_score(num_of_player - 1)
            self.start_player_list[player_index].add_score(1)
            if player_index == 0:
                self.start_player_list[0].played_game = (
                    self.start_player_list[0].played_game + 1
                )
            self.current_draw_index = self.current_draw_index - 1
            winplayerincurrent = self.current_player_list.pop(index_in_current)
            self.win_player_list.append(winplayerincurrent)
            if setting.Waiting:
                time.sleep(1.5)
            if self.system_login_index == True:
                updated_score = self.start_player_list[0].score
                updated_played_game = self.start_player_list[0].played_game
                login_Username = self.start_player_list[0]
                read.update_score_by_name(
                    login_Username, updated_score, updated_played_game
                )

    #   Set the player to lose
    def set_player_lose(self, player_index):
        index_in_current = self.get_current_index_by_start_index(player_index)
        if index_in_current == -1:
            print(f"The player is not in the current game.")
        else:
            self.start_player_list[player_index].in_game = False
            self.current_player_list[index_in_current].in_game = False
            self.start_player_list[player_index].minus_score(1)
            if player_index == 0:
                self.start_player_list[0].played_game = (
                    self.start_player_list[0].played_game + 1
                )
            loseplayerincurrent = self.current_player_list.pop(index_in_current)
            self.lose_player_list.append(loseplayerincurrent)
            if self.system_login_index == True:
                updated_score = self.start_player_list[0].score
                updated_played_game = self.start_player_list[0].played_game
                login_Username = self.start_player_list[0]
                read.update_score_by_name(
                    login_Username, updated_score, updated_played_game
                )

    #   Display all players name
    def display_all_players_name(self):
        print("")
        print(f"There are {len(self.start_player_list)} players in the game now.")
        print(f"All Player Name List:")
        for i in range(0, len(self.start_player_list)):
            print(str(i + 1) + ") ", end="")
            print(self.start_player_list[i].username)

    #   Displayer all Current Player name
    def display_current_players_name(self):
        print("")
        print(f"There are {len(self.current_player_list)} players in the game now.")
        print(f"Current Player Name List:")
        for i in range(0, len(self.start_player_list)):
            if self.start_player_list[i].in_game:
                print(str(i + 1) + ") ", end="")
                print(self.start_player_list[i].username)

    #   Display number of card of the player
    def display_number_of_card_by_index(self, player_index):
        if self.start_player_list[player_index].in_game:
            currentindex = self.get_current_index_by_start_index(player_index)
            helper.display_heading(
                f"Player {player_index + 1}: {self.start_player_list[player_index].username} has {self.current_player_list[currentindex].get_current_num_of_card()}  Cards in total",
                1,
            )
            print("")
        else:
            helper.display_heading(
                f"Player {player_index + 1}: {self.start_player_list[player_index].username} has no cards.",
                1,
            )
            print("")

    #   Display the card of the player
    def display_card_of_player_by_index(self, player_index):
        if self.start_player_list[player_index].in_game:
            current_index = self.get_current_index_by_start_index(player_index)
            Poker.print_lengthy_simply_hands(
                self.current_player_list[current_index].current_lengthy_simply_hand
            )
            print("")
        else:
            helper.display_heading(
                f"Player {player_index + 1}: {self.start_player_list[player_index].username} has won the game.",
                1,
            )
            print("")

    #   Display the number of card and display the card of the player
    def display_num_of_card_and_card_by_index(self, player_index):
        currentindex = self.get_current_index_by_start_index(player_index)
        if self.current_player_list[currentindex].in_game:
            self.display_number_of_card_by_index(player_index)
            self.display_card_of_player_by_index(player_index)
        else:
            helper.display_heading(
                f"Player  {player_index + 1}: {self.start_player_list[player_index].username} has won the game.",
                1,
            )

    #   Display all players' cards
    def display_all_player_cards(self):
        self.display_guest_player_cards()
        self.display_other_player_cards()

    #   Display the guest player card
    def display_guest_player_cards(self):
        if self.start_player_list[0].in_game:
            current_index = self.get_current_index_by_start_index(0)
            helper.display_heading(
                f"You (Player 1: {self.start_player_list[0].username}) has {self.current_player_list[current_index].get_current_num_of_card()} Cards in total",
                1,
            )
            self.display_card_of_player_by_index(0)
            print("")
        else:
            helper.display_heading(f"Player 1: You has won the game already.", 1)

    #   Display all other player card
    def display_other_player_cards(self):
        for x in range(1, len(self.start_player_list)):
            if self.start_player_list[x].in_game:
                self.display_num_of_card_and_card_by_index(x)
            else:
                self.display_card_of_player_by_index(x)

    #   Display Turn Number of the game
    def display_turn_number(self):
        print("")
        helper.display_heading(f"| Turn {self.turn} Start Now!!! |", 2)
        print("")

    #   Card Exchange Procedure
    def exchange_card(self):
        #   Get the index of two players according to the drawing order
        who_draw_index = self.exchange_order[self.current_draw_index] - 1
        if self.current_draw_index == len(self.current_player_list) - 1:
            who_being_drawn_index = self.exchange_order[0] - 1
        else:
            who_being_drawn_index = self.exchange_order[self.current_draw_index + 1] - 1

        current_who_draw_index = self.get_current_index_by_start_index(who_draw_index)
        current_who_being_drawn_index = self.get_current_index_by_start_index(
            who_being_drawn_index
        )

        #   Print out the Trun Number and who draw who
        print("")
        helper.display_heading(
            f"|Turn {self.turn}: Player {who_draw_index + 1}({self.start_player_list[who_draw_index].username}) draws Player {who_being_drawn_index + 1}({self.start_player_list[who_being_drawn_index].username})|",
            1,
        )
        print("")

        if setting.Waiting:
            time.sleep(1.2)
        print(
            f"Which cards?\t {self.start_player_list[who_being_drawn_index].username} has {self.current_player_list[current_who_being_drawn_index].get_current_num_of_card()} cards"
        )
        print(
            f"Please input the __th cards (e.g. 1st card, input '1'/ 3rd card, input '3')"
        )
        if who_draw_index == 0:  # Need to change later, now automated all process
            index_of_card = int(input(""))
        else:
            index_of_card = random.randint(
                1,
                self.current_player_list[
                    current_who_being_drawn_index
                ].get_current_num_of_card(),
            )
            if setting.Waiting:
                time.sleep(1)
            print(index_of_card)
            if setting.Waiting:
                time.sleep(1.4)
        while (
            index_of_card
            > self.current_player_list[
                current_who_being_drawn_index
            ].get_current_num_of_card()
            or index_of_card < 1
        ):
            print("")
            print(
                f"Please input a number between 1 to {self.current_player_list[current_who_being_drawn_index].get_current_num_of_card()}!!!"
            )
            print(
                f"Which cards? {self.start_player_list[who_being_drawn_index].username} has {self.current_player_list[current_who_being_drawn_index].get_current_num_of_card()} cards"
            )
            index_of_card = int(
                input(
                    f"Please input the __th cards (e.g. 1st card, input '1'/ 3rd card, input '3')"
                )
            )

        #   Using the user input card index to rand another card index
        drawnindex = random.randint(
            index_of_card * 9,
            (
                len(
                    self.current_player_list[
                        current_who_being_drawn_index
                    ].current_index_hand
                )
                + index_of_card
            )
            * 10,
        ) % (
            len(
                self.current_player_list[
                    current_who_being_drawn_index
                ].current_index_hand
            )
        )

        #   Pick out a card(index) from Player who being drawn
        cardindex = self.current_player_list[
            current_who_being_drawn_index
        ].current_index_hand.pop(drawnindex)

        #   Displaying that card if the turn related to the Guest Player
        target_card = Poker.convert_index_to_card(cardindex)
        if who_being_drawn_index == 0 or who_draw_index == 0:
            print("")
            helper.display_heading(
                f"The card being drawn is {TYPE_DICT[target_card[0]]} {NUM_SHORT_DICT[target_card[1]]}",
                1,
            )
            print("")
            if setting.Waiting:
                time.sleep(1.4)

        #   Put the card in drawer's hand
        self.current_player_list[current_who_draw_index].current_index_hand.append(
            cardindex
        )

        #   Update both players hand
        self.current_player_list[current_who_draw_index].update_all_hands()
        self.current_player_list[current_who_being_drawn_index].update_all_hands()

        #   Update the Draw Card Order Index
        if self.current_draw_index == len(self.current_player_list) - 1:
            self.current_draw_index = 0
        else:
            self.current_draw_index = self.current_draw_index + 1

    #   Check if anyone win after every turn
    def check_if_anyone_win(self):
        for x in range(len(self.start_player_list)):
            y = self.get_current_index_by_start_index(x)
            if (
                y >= 0
                and self.current_player_list[y].current_index_hand == []
                and self.current_player_list[y].in_game
            ):
                self.set_player_win(x)
                self.exchange_order.remove(x + 1)

    #   Check if the game is endded
    #   Game will end when the total number of player equals to 1
    def check_if_game_ended(self):
        if self.get_total_card_in_game() == 1 or len(self.current_player_list) == 1:
            for x in range(len(self.start_player_list)):
                y = self.get_current_index_by_start_index(x)
                if (
                    y >= 0
                    and len(self.current_player_list[y].current_index_hand) != 0
                    and self.current_player_list[y].in_game
                ):
                    self.set_player_lose(x)
            self.end_game()
            return True
        else:
            return False

    #   End Game Procedure
    def end_game(self):
        if len(self.current_player_list) != 0:
            return
        self.poker_set = []
        self.game_ended = True

    #   Show the Win and Lose Player Lisy
    def show_win_lose(self):
        print("=========================Win Player=========================")
        for x in range(0, len(self.win_player_list)):
            print(f"---------Next Player----------")
            print(f" Username: \t{self.win_player_list[x].username}")
            print(f" Original Score: \t{self.win_player_list[x].get_previous_score()}")
            print(
                f" Rewards of this game: \t{self.win_player_list[x].get_reward_score()}"
            )
            print(f" Current Score: \t{self.win_player_list[x].get_score()}")

        print("")
        print("=========================Lose Player=========================")
        for x in range(0, len(self.lose_player_list)):
            print(f" Username: \t{self.lose_player_list[x].username}")
            print(f" Original Score: \t{self.lose_player_list[x].get_previous_score()}")
            print(
                f" Penalty of this game: \t{self.lose_player_list[x].get_reward_score()}"
            )
            print(f" Current Score: \t{self.lose_player_list[x].get_score()}")
        print("")
