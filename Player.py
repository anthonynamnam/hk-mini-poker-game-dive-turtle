import Poker
import DisplayMode


class Player:
    #   Every Player has initial score of 5
    in_game = False
    hand_inserted = False
    original_index_hand = []
    current_index_hand = []
    current_converted_hands = []
    current_lengthy_simply_hand = []
    played_game = 0

    #   Initiate Player
    def __init__(
        self,
        username,
        score=3,
        played_game=0,
        displayMode=DisplayMode.DisplayMode.SIMPLY,
    ):
        self.username = username
        self.score = score
        self.previous_score = score
        self.played_game = played_game
        self.in_game = True
        self.displayMode = displayMode

    #   Reset the Player's Hand
    def resetHands(self):
        self.original_index_hand.clear()
        self.current_index_hand.clear()
        self.current_converted_hands.clear()
        self.current_lengthy_simply_hand.clear()
        self.in_game = True

    #   Get Score of the player
    def get_score(self):
        return self.score

    #   Get Previous Score of the player
    def get_previous_score(self):
        return self.previous_score

    #   Get the reward of this game of the player
    def get_reward_score(self):
        return self.score - self.previous_score

    #   Get the status of the player
    def get_in_game(self):
        return self.in_game

    #   Get number of card of the simplified hands
    def get_original_num_of_card(self):
        return len(self.original_index_hand)

    #   Get number of card of the origianl hands
    def get_current_num_of_card(self):
        return len(self.current_index_hand)

    #   Add the player score
    def add_score(self, add):
        self.score = self.get_score() + add

    #   Minus the player score
    def minus_score(self, minus):
        self.score = max(0, self.get_score() - minus)

    #   Get the converted hands of of the player
    def update_index_hand_to_converted_hand(self):
        return Poker.convert_indices_to_hands(self.current_index_hand)

    #   Get the converted detailed hands of of the player
    def update_converted_hand_to_lengthy_simply_hand(self):
        return Poker.convert_hands_to_lengthy_simply_hands(
            self.current_converted_hands, self.displayMode
        )

    #   Get the simplified detailed hands of of the player
    def update_lengthy_simply_hand_to_eliminated_hand(self):
        return Poker.eliminate_pair_with_lengthy_simply_hands(
            self.current_lengthy_simply_hand, self.displayMode
        )

    #   Sort all the hands
    def get_all_hands_sorted(self):
        self.current_index_hand.sort(reverse=False)
        self.current_converted_hands.sort(
            key=Poker.convert_card_to_index, reverse=False
        )
        self.current_lengthy_simply_hand.sort(
            key=Poker.convert_lengthy_simply_hand_to_index, reverse=False
        )

    #   Input new hand, sort it and updated it
    def insert_hands(self, input_hands, eliminate=True):
        if not self.hand_inserted:
            self.original_index_hand = input_hands.copy()
            self.hand_inserted = True

        self.current_index_hand = input_hands.copy()
        self.update_all_hands(eliminate=eliminate)
        self.get_all_hands_sorted()

    #   Updated other hands when new hands is inputted
    def update_all_hands(self, eliminate=True):
        if eliminate:
            self.current_index_hand = Poker.eliminate_pair_by_indice(
                self.current_index_hand
            )
        self.current_converted_hands = self.update_index_hand_to_converted_hand().copy()
        self.current_lengthy_simply_hand = (
            self.update_converted_hand_to_lengthy_simply_hand().copy()
        )
        self.get_all_hands_sorted()

