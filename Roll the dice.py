import random


class DiceGame:
    def __init__(self):
        self.players = []
        self.computer_players = []
        self.current_bid = None
        self.current_bidder = None
        self.is_ace_wild = True

    def input_players(self):
        """Enter player information"""
        while True:
            try:
                num_players = int(input("Please enter the number of players at least 2: "))
                if num_players >= 2:
                    break
                else:
                    print("Insufficient players, you can try playing against the computer")
            except ValueError:
                print("Please enter a valid number")

        for i in range(num_players):
            while True:
                player_name = input(f"Please enter player {i + 1} name: ")
                if player_name:
                    self.players.append(
                        {"name": player_name, "dice": [random.randint(1, 6) for _ in range(5)], "status": "active"})
                    break
                else:
                    print("Player name cannot be empty, please re-enter!")

    def create_computer_player(self, computers):
        """create computer player"""
        for i in range(computers):
            computer_name = f"computer_{i+1}"
            self.computer_players.append({"name": computer_name, "dice": [random.randint(1, 6) for _ in range(5)], "status": "active"})

    def roll_dice(self, player):
        """Simulates a player rolling the dice"""
        player["dice"] = [random.randint(1, 6) for _ in range(5)]

    def show_dice_one_by_one(self):
        """Display the dice points of each player one by one"""
        print("\nPlease press Enter to see each player's points.")
        for player in self.players:
            input("Press Enter to continue...")
            print(f"{player['name']} the dice: {player['dice']}")

    def computer_action(self, computer):
        """computer action"""
        print(f"\n{computer['name']} Round")
        action = random.choice(['bid', 'challenge'])
        if action == 'bid':
            self.computer_bidder(computer)
        else:
            if self.current_bid is None:
                print("Computer selects bids")
                self.computer_bidder(computer)
            else:
                print(f"{computer['name']} challenge")
                self.challenge()
    def computer_bidder(self, computer):
        bid = False
        while not bid:
            quantity = random.randint(1, len(self.players) * 5)
            face = random.randint(1, 6)

            if self.current_bid is None:
                self.current_bid = (quantity, face)
                self.current_bidder = computer
                print(f"{computer['name']} bid: {quantity} {face}")
                if face == 1:
                    self.is_ace_wild = False
                bid = True
            else:
                previous_quantity, previous_face = self.current_bid
                if quantity > previous_quantity or (quantity == previous_quantity and face > previous_face):
                    self.current_bid = (quantity, face)
                    self.current_bidder = computer
                    print(f"{computer['name']} bid: {quantity} {face}")
                    if face == 1:
                        self.is_ace_wild = False
                    bid = True
                else:
                    continue

    def make_bid(self, player):
        """player bid"""
        while True:
            try:
                print(f"{player['name']}, please enter your bid (format: quantity points, for example: '3 4'): ")
                # 3 4 means three 4 point
                bid_str = input().strip()
                quantity_str, face_str = bid_str.split()
                quantity = int(quantity_str)
                face = int(face_str)

                # Verify That The Bid Is Valid
                if face < 1 or face > 6:
                    print("The Number Of Points Must Be Between 1 And 6")
                    continue

                if self.current_bid is None:
                    # initial bid
                    self.current_bid = (quantity, face)
                    self.current_bidder = player
                    print(f"{player['name']}bid: {quantity} {face}")
                    if face == 1:
                        self.is_ace_wild = False
                    return

                prev_quantity, prev_face = self.current_bid

                if quantity > prev_quantity:
                    # Number Increases
                    self.current_bid = (quantity, face)
                    self.current_bidder = player
                    print(f"{player['name']} bidding: {quantity} {face}")
                    if face == 1:
                        self.is_ace_wild = False
                    return
                elif quantity == prev_quantity and face > prev_face:
                    # increasing point
                    self.current_bid = (quantity, face)
                    self.current_bidder = player
                    print(f"{player['name']} bidding: {quantity} {face}")
                    if face == 1:
                        self.is_ace_wild = False
                    return
                else:
                    print("The bid must be higher than the previous bid (either by an increased amount or by an increased number of points and the same amount).")
                    continue

            except ValueError:
                print("The input format is incorrect, please enter the correct bid format (for example: '3 4').")

    def challenge(self):
        """Dealing with challenges"""
        total = 0
        bid_quantity, bid_face = self.current_bid

        print("\nShow the dice:")
        for player in self.players + self.computer_players:
            print(f"{player['name']}'s dice: {player['dice']}")
            if bid_face == 1:
                total += player["dice"].count(bid_face)
            else:
                if self.is_ace_wild:
                    total += player["dice"].count(bid_face) + player["dice"].count(1)
                else:
                    total += player["dice"].count(bid_face)
        print(f"\nStatistical results: The actual total {total} {bid_face} (Including universal dice 1)")
        if total >= bid_quantity:
            print("Challenge failed! The challenger loses and drink.")
        else:
            print(f"Challenge successful! {self.current_bidder['name']} loses and must drink.")


        # Reset game state
        self.current_bid = None
        self.current_bidder = None
        self.is_ace_wild = True

        # A new round starts with a random player
        self.new_round()
        # start_player = random.choice(self.players)
        # print(f"\nA new round begins, with {start_player['name']} bidding first.")
        # return start_player
    def new_round(self):
        """start a new round"""
        print("\nBegin new round!")
        for player in self.players:
            self.roll_dice(player)
        for computer in self.computer_players:
            self.roll_dice(computer)
        self.show_dice_one_by_one()
        all_players = self.players + self.computer_players


        current_player = random.choice(all_players)
        print(f"Started by player {current_player['name']}")


    def player_turn(self, player):
        """player round"""
        print(f"\n{player['name']}'s round")
        print("1. bid")
        print("2. challenge")
        print("3. end game")
        choice = input("Please choose to bid or challenge: ")

        if choice == "1":
            self.make_bid(player)
        elif choice == "2":
            if self.current_bid is None:
                print("No bid has been made yet, so cannot challenge.")
                return player  # Return the current player to continue bidding
            else:
                return self.challenge()
        elif choice == "3":
            print("end game!")
            exit()
        else:
            print("Invalid selection, please select again.")
            return player  # Return to current player and reselect

        return None  # Return None to continue the game

    def play_game(self):
        """start game"""
        print("Welcome to Roll the Dice!")
        print("Please select a game mode:")
        print("1. P v P")
        print("2. P v C")
        choice = input("Please enter your choice (1 or 2): ")

        if choice == "1":
            self.player_vs_player_mode()
        elif choice == "2":
            self.player_vs_computer_mode()
        else:
            print("Invalid choice!")

    def player_vs_computer_mode(self):
        """P V C"""
        self.input_players()
        computer_number = int(input("please enter computer_player number: "))
        self.create_computer_player(computer_number)

        for player in self.players:
            self.roll_dice(player)
        for computer in self.computer_players:
            self.roll_dice(computer)

        self.show_dice_one_by_one()
        all_players = self.players + self.computer_players
        current_player = random.choice(all_players)
        while True:
            if current_player in self.players:
                result = self.player_turn(current_player)
            else:
                result = self.computer_action(current_player)
                input("Press Enter to continue...")

            if isinstance(result, dict):
                current_player = result
            else:
                all_players = self.players + self.computer_players
                index = all_players.index(current_player)
                next_index = (index + 1) % len(all_players)
                current_player = all_players[next_index]



    def player_vs_player_mode(self):
        """P v P"""
        self.input_players()

        # Initial dice roll
        for player in self.players:
            self.roll_dice(player)

        # Display the dice points of each player one by one
        self.show_dice_one_by_one()

        # Randomly select a player to start the game
        current_player = random.choice(self.players)

        while True:
            # Player round
            result = self.player_turn(current_player)

            # If the result is a challenge, returns the starting player after the challenge
            if result is not None and isinstance(result, dict):
                current_player = result
            else:
                # Next player bids
                index = self.players.index(current_player)
                next_index = (index + 1) % len(self.players)
                current_player = self.players[next_index]


# start
if __name__ == "__main__":
    game = DiceGame()
    game.play_game()