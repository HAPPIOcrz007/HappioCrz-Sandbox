# [X] 1  -- list all order
# [ ] 2  -- complete affirmative orders --------------------------------- remove them from list ----
# [ ] 3  -- announce completions for each player ------------------------ in chat ----
# [ ] 4  -- change net movements while doing orders --------------------- update share property in and out ---
# [ ] 5  -- convert possible conditional orders to affirmative ---------- do-able orders to confirm ---
# [ ] 6  -- update prices ----------------------------------------------- update prices on current moves ---
# [ ] 7  -- check conditional chances, if possible to confirm ----------- do as step 5 again for new prices ---
# [ ] 8  -- deliver new calls and puts ---------------------------------- assign new calls and puts at the premium ---
# [ ] 9  -- update all calls and puts , ready for next round ------------ get calls and puts ready for next round ---
# [ ] 10 -- update prices ----------------------------------------------- update prices on current moves ---
# [ ] 11 -- announce all completed processes and announce them ---------- all logged and ready ---
# [ ] 12 -- ready for new round / check if completed --> announce winner  check completion (yes or now) or next round

import uuid
from typing import List, Dict
from typing_extensions import override  # Use this if Python <3.12
from datetime import datetime

is_completed = False


# ------------------ Core Classes ------------------


class Person:
    """
    Represents a player in the game.

    Attributes:
        name (str): The player's name.
        stocks (List[str]): A list of the player's stock holdings, formatted as "stockName_lowerDstock_volumeDstock_price".
        amount (float): The player's current cash amount.
        net_worth (float): The player's net worth (cash + stock value).
        order (List[Dict[str, str | float | int]]): A list of the player's orders.
        id (str): The player's unique ID.
    """

    name: str
    stocks: List[str]  # <stockName_lower>D<stock_volume>D<stock_price>
    amount: float
    net_worth: float
    order: List[Dict[str, str | float | int]]
    id: str

    def __init__(self, entryName: str, entryAmount: float, player_id: str) -> None:
        """
        Initializes a Person object.

        Args:
            entryName (str): The player's name.
            entryAmount (float): The player's starting cash amount.
            player_id (str): The player's unique ID.
        """
        self.name = entryName
        self.stocks = []
        self.amount = entryAmount
        self.net_worth = entryAmount
        self.order = []
        self.id = player_id

    @override
    def __str__(self) -> str:
        """
        Returns a string representation of the Person object.

        Returns:
            str: A string containing the player's name, cash, and net worth.
        """
        return f"Person(name={self.name}, cash={self.amount:.2f}, net_worth={self.net_worth:.2f})"


class Stock:
    """
    Represents a stock in the game.

    Attributes:
        name (str): The stock's name.
        id (str): The stock's unique ID.
        volume (int): The total number of shares available.
        capital (float): The total capital of the stock.
        price (float): The current price per share.
        movement (Dict[str, float]): A dictionary tracking buy and sell movements.
        current_market (int): The current available volume in the market.
    """

    name: str
    id: str
    volume: int
    capital: float
    price: float
    movement: Dict[str, float]
    current_market: int

    def __init__(
        self,
        listingName: str,
        listingId: str,
        listingVolume: int,
        listingCapital: float,
    ) -> None:
        """
        Initializes a Stock object.

        Args:
            listingName (str): The stock's name.
            listingId (str): The stock's unique ID.
            listingVolume (int): The total number of shares.
            listingCapital (float): The total capital of the stock.
        """
        self.name = listingName
        self.id = listingId
        self.volume = listingVolume
        self.capital = listingCapital
        self.price = listingCapital / listingVolume if listingVolume > 0 else 0
        self.movement = {"buys": 0.0, "sells": 0.0}
        self.current_market = self.volume

    @override
    def __str__(self) -> str:
        """
        Returns a string representation of the Stock object.

        Returns:
            str: A string containing the stock's name, ID, price, volume, and capital.
        """
        return f"Stock(name={self.name}, id={self.id}, price={self.price:.2f}, volume={self.volume}, capital={self.capital})"


class Chat:
    """
    Represents a chat message in the game.

    Attributes:
        chat_counter (int): A class-level counter for chat message IDs.
        chat_data (str): The content of the chat message.
        chat_time (str): The timestamp of the chat message.
        id (int): The unique ID of the chat message.
        writer (str): The author of the chat message.
    """

    chat_counter: int = 1

    chat_data: str
    chat_time: str
    id: int
    writer: str

    def __init__(self, context: str, timeStamp: str, writer: str) -> None:
        """
        Initializes a Chat object.

        Args:
            context (str): The content of the chat message.
            timeStamp (str): The timestamp of the chat message.
            writer (str): The author of the chat message.
        """
        self.chat_data = context
        self.chat_time = timeStamp
        self.id = Chat.chat_counter
        Chat.chat_counter += 1
        self.writer = writer


class GameState:
    """
    Represents the state of the game.

    Attributes:
        people (List[Person]): A list of players in the game.
        market (List[Stock]): A list of stocks in the game.
        rounds (int): The total number of rounds in the game.
        orderList (List[str]): A list of all current orders.
        current_round (int): The current round number.
        logs (List[Dict[str, str | int]]): A list of game logs.
        chats (List[Chat]): A list of chat messages.
    """

    people: List[Person]
    market: List[Stock]
    rounds: int
    orderList: List[str]
    current_round: int
    logs: List[Dict[str, str | int]]
    chats: List[Chat]

    def __init__(self) -> None:
        """
        Initializes a GameState object.
        """
        self.people = []
        self.market = []
        self.rounds = 0
        self.current_round = 0
        self.logs = []
        self.orderList = []
        self.chats = []

    def add_player(self, name: str, starting_cash: float) -> None:
        """
        Adds a player to the game.

        Args:
            name (str): The player's name.
            starting_cash (float): The player's starting cash amount.
        """
        player_id = uuid.uuid4().hex[:8]
        player = Person(name, starting_cash, player_id)
        self.people.append(player)
        self.log_action("Player Registered", name, f"Starting cash: {starting_cash}")

    def add_stock(self, name: str, volume: int, capital: float) -> None:
        """
        Adds a stock to the game.

        Args:
            name (str): The stock's name.
            volume (int): The total number of shares.
            capital (float): The total capital of the stock.
        """
        stock_id = uuid.uuid4().hex[:8]
        stock = Stock(name, stock_id, volume, capital)
        self.market.append(stock)
        self.log_action(
            "Stock Registered", name, f"Volume: {volume}, Capital: {capital}"
        )

    def log_action(self, action_type: str, actor: str, details: str) -> None:
        """
        Logs an action in the game.

        Args:
            action_type (str): The type of action.
            actor (str): The actor who performed the action.
            details (str): Details about the action.
        """
        entry: Dict[str, str | int] = {
            "round": self.current_round,
            "type": action_type,
            "actor": actor,
            "details": details,
        }
        self.logs.append(entry)
        print(f"[LOG] Round {self.current_round} | {action_type} by {actor}: {details}")


# ------------------ Input Helpers ------------------


def get_int(
    prompt: str, error_msg: str = "Invalid entry --> must be an integer"
) -> int | None:
    """
    Gets an integer input from the user.

    Args:
        prompt (str): The prompt to display to the user.
        error_msg (str): The error message to display if the input is invalid.

    Returns:
        int | None: The integer entered by the user, or None if the input is invalid.
    """
    try:
        return int(input(prompt))
    except ValueError:
        print(error_msg)
        return None


def get_float(
    prompt: str, error_msg: str = "Invalid entry --> must be a float"
) -> float | None:
    """
    Gets a float input from the user.

    Args:
        prompt (str): The prompt to display to the user.
        error_msg (str): The error message to display if the input is invalid.

    Returns:
        float | None: The float entered by the user, or None if the input is invalid.
    """
    try:
        return float(input(prompt))
    except ValueError:
        print(error_msg)
        return None


# ------------------ Display ------------------


def display_game_state(game: GameState) -> None:
    print("\nCurrent Game State:")
    print("Players:")
    for p in game.people:
        print(p)
    print("\nStocks:")
    for s in game.market:
        print(
            f"{s.name} | Price: ₹{s.price:.2f} | Total Volume: {s.volume} | Available in Market: {s.current_market} | Capital: ₹{s.capital:.2f}"
        )


# ------------ Game Functioning ------------


def get_order(game: GameState, p: Person, choice: int, stock_name: str) -> str:
    """
    Gets an order from a player.

    Args:
        game (GameState): The current game state.
        p (Person): The player placing the order.
        choice (int): The type of order (1: buy, 2: sell, 3: call, 4: put, 5: conditional).
        stock_name (str): The name of the stock.

    Returns:
        str: A message indicating the status of the order.
    """
    for s in game.market:
        if s.name.lower() == stock_name.lower():
            match choice:
                case 1:
                    try:
                        buy_volume = int(
                            input(f"What volume of share:{s.name} you want : ")
                        )
                    except ValueError:
                        return "Value must be an integer. Order cancelled."

                    max_affordable = int(p.amount // s.price)
                    max_possible = min(s.current_market, max_affordable, buy_volume)

                    if max_possible == 0:
                        return f"Cannot place order: insufficient funds or no shares available in market."

                    print(
                        f"Trade possible for up to {max_possible} shares at current price ₹{s.price:.2f}"
                    )
                    if max_possible < buy_volume:
                        print(
                            f"Note: You requested {buy_volume}, but only {max_possible} can be fulfilled now."
                        )

                    ask = input(
                        f"Do you want to place a BUY order for {max_possible} shares at ₹{s.price:.2f}? [y/n]: "
                    )
                    if ask.lower() == "y":
                        game.orderList.append(
                            f"BUY {p.name} {s.name.upper()} {max_possible} {s.price}"
                        )
                        return f"Order for BUY {p.name} {s.name} {max_possible} at ₹{s.price:.2f} placed."
                    elif ask.lower() == "n":
                        return f"Order for BUY {p.name} {s.name} cancelled."
                    else:
                        return f"Invalid response. Order cancelled."

                case 2:
                    holdings = []
                    for i, h in enumerate(p.stocks):
                        parts = h.split("D")
                        if len(parts) == 3 and parts[0] == stock_name.lower():
                            holdings.append((i + 1, parts))

                    if not holdings:
                        return f"No holdings found for {stock_name}. Cannot sell."

                    print("You hold:")
                    for idx, (name, vol, price) in holdings:
                        print(
                            f"Holding #{idx}: {name.upper()} | Volume: {vol} | Price:"
                            f" {price}"
                        )

                    try:
                        selected = int(input("Enter holding number to sell from: "))
                    except ValueError:
                        return "Invalid input. Order cancelled."

                    if selected < 1 or selected > len(holdings):
                        return "Invalid selection. Order cancelled."

                    _, (name, vol, price) = holdings[selected - 1]
                    try:
                        sell_volume = int(
                            input(
                                f"How much of {name.upper()} would you like to sell? "
                            )
                        )
                    except ValueError:
                        return "Invalid volume. Order cancelled."

                    if sell_volume > int(vol):
                        return "You don't have enough volume. Order cancelled."

                    confirm = input(
                        f"Confirm sale of {sell_volume} shares of {name.upper()} at"
                        f" price {price}? [y/n]: "
                    )
                    if confirm.lower() == "y":
                        game.orderList.append(
                            f"SELL {p.name} {name.upper()} {sell_volume} {price}"
                        )
                        return (
                            f"Order for SELL {p.name} {name.upper()} {sell_volume} {price}"
                            " placed."
                        )
                    else:
                        return "Sell order cancelled."

                case 3:
                    try:
                        strike_price = float(
                            input(f"Enter strike price for CALL on {s.name}: ")
                        )
                        premium = float(input("Enter premium for the CALL option: "))
                        expiry = int(input("Enter expiry rounds for this CALL: "))
                        if expiry <= 0:
                            return (
                                "Expiry must be a positive integer. Option cancelled."
                            )
                    except ValueError:
                        return "Invalid input. CALL option cancelled."

                    confirm = input(
                        f"Confirm CALL for {s.name} at strike {strike_price},"
                        f" premium {premium}, expiry {expiry}? [y/n]: "
                    )
                    if confirm.lower() == "y":
                        game.orderList.append(
                            f"CALL {p.name} {s.name} {strike_price} {premium} {expiry}"
                        )
                        return f"CALL option for {p.name} on {s.name} added."
                    else:
                        return "CALL option cancelled."

                case 4:
                    try:
                        strike_price = float(
                            input(f"Enter strike price for PUT on {s.name}: ")
                        )
                        premium = float(input("Enter premium for the PUT option: "))
                        expiry = int(input("Enter expiry rounds for this PUT: "))
                        if expiry <= 0:
                            return (
                                "Expiry must be a positive integer. Option cancelled."
                            )
                    except ValueError:
                        return "Invalid input. PUT option cancelled."

                    confirm = input(
                        f"Confirm PUT for {s.name} at strike {strike_price},"
                        f" premium {premium}, expiry {expiry}? [y/n]: "
                    )
                    if confirm.lower() == "y":
                        game.orderList.append(
                            f"PUT {p.name} {s.name} {strike_price} {premium} {expiry}"
                        )
                        return f"PUT option for {p.name} on {s.name} added."
                    else:
                        return "PUT option cancelled."

                case 5:
                    try:
                        cond_type = (
                            input("Enter conditional type (BUY/SELL): ").strip().upper()
                        )
                        if cond_type not in ["BUY", "SELL"]:
                            return "Invalid type. Conditional order cancelled."

                        direction = "LESS" if cond_type == "BUY" else "GREATER"
                        print(
                            f"Note: This conditional will trigger when price is"
                            f" {direction} than your target."
                        )

                        volume = int(input("Enter volume for conditional order: "))
                        trigger_price = float(input("Enter trigger price: "))
                    except ValueError:
                        return "Invalid input. Conditional order cancelled."

                    confirm = input(
                        f"Confirm CONDITIONAL {cond_type} ({direction}) of {volume}"
                        f" shares of {s.name} at trigger {trigger_price}? [y/n]: "
                    )
                    if confirm.lower() == "y":
                        game.orderList.append(
                            f"COND {p.name} {s.name} {cond_type} {direction} {volume}"
                            f" {trigger_price}"
                        )
                        return f"Conditional {cond_type} order for {p.name} on {s.name} added."
                    else:
                        return "Conditional order cancelled."

                case _:
                    return "Invalid choice. Order cancelled."
    return f"Stock {stock_name} not found in market."


def announce_trade(game: GameState, actor: str, message: str) -> None:
    """
    Announces a trade in the chat.

    Args:
        game (GameState): The current game state.
        actor (str): The actor who made the trade.
        message (str): The message to announce.
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    chat = Chat(context=message, timeStamp=timestamp, writer=actor)
    print(f"[CHAT] Round {game.current_round} | {actor}: {message}")
    game.chats.append(chat)


def complete_order(game: GameState) -> None:
    """
    Completes the buy and sell orders.

    Args:
        game (GameState): The current game state.
    """
    completed_orders = []

    for order in game.orderList:
        parts = order.split()
        if not parts:
            continue

        order_type = parts[0]

        # Only handle BUY/SELL here
        if order_type in ["BUY", "SELL"]:
            if len(parts) < 5:
                continue

            player_name = parts[1]
            stock_name = parts[2]
            volume = int(parts[3])  # safe now
            price = float(parts[4])

            stock = next(
                (s for s in game.market if s.name.lower() == stock_name.lower()), None
            )
            person = next((p for p in game.people if p.name == player_name), None)

            if not stock or not person:
                continue

            if order_type == "BUY":
                total_cost = volume * price
                if person.amount >= total_cost and stock.current_market >= volume:
                    person.amount -= total_cost
                    stock.current_market -= volume
                    stock.movement["buys"] += total_cost
                    person.stocks.append(f"{stock.name.lower()}D{volume}D{price}")
                    game.log_action(
                        "BUY Executed",
                        person.name,
                        f"{volume} of {stock.name} at {price}",
                    )
                    announce_trade(
                        game, person.name, f"Bought {volume} of {stock.name} at {price}"
                    )
                    completed_orders.append(order)

            elif order_type == "SELL":
                for i, h in enumerate(person.stocks):
                    parts = h.split("D")
                    if len(parts) != 3:
                        continue
                    name, held_vol, held_price = parts
                    if name == stock.name.lower() and int(held_vol) >= volume:
                        revenue = volume * price
                        person.amount += revenue
                        stock.current_market += volume
                        stock.movement["sells"] += revenue

                        remaining = int(held_vol) - volume
                        if remaining > 0:
                            person.stocks[i] = f"{name}D{remaining}D{held_price}"
                        else:
                            person.stocks.pop(i)

                        game.log_action(
                            "SELL Executed",
                            person.name,
                            f"{volume} of {stock.name} at {price}",
                        )
                        announce_trade(
                            game,
                            person.name,
                            f"Sold {volume} of {stock.name} at {price}",
                        )
                        completed_orders.append(order)
                        break

        # Skip CALL/PUT here (they are handled in update_options)
        else:
            continue

    for order in completed_orders:
        game.orderList.remove(order)


def convert_orders(game: GameState) -> None:
    """
    Converts conditional orders to affirmative orders if the condition is met.

    Args:
        game (GameState): The current game state.
    """
    converted = []

    for order in game.orderList:
        parts = order.split()
        if len(parts) != 7 or parts[0] != "COND":
            continue  # skip non-conditional or malformed orders

        (
            _,
            player_name,
            stock_name,
            cond_type,
            direction,
            volume_str,
            trigger_price_str,
        ) = parts
        volume = int(volume_str)
        trigger_price = float(trigger_price_str)

        stock = next(
            (s for s in game.market if s.name.lower() == stock_name.lower()), None
        )
        if not stock:
            continue

        current_price = stock.price
        condition_met = (direction == "LESS" and current_price < trigger_price) or (
            direction == "GREATER" and current_price > trigger_price
        )

        if condition_met:
            new_order = (
                f"{cond_type} {player_name} {stock.name} {volume} {current_price}"
            )
            converted.append((order, new_order))
            game.log_action(
                "Conditional Triggered",
                player_name,
                f"{cond_type} {stock.name} at {current_price} (trigger:"
                f" {trigger_price})",
            )

    # Replace triggered conditionals with affirmative orders
    for old, new in converted:
        game.orderList.remove(old)
        game.orderList.append(new)


def update_stocks(game: GameState) -> None:
    """
    Updates the prices of the stocks based on buy and sell movements.

    Args:
        game (GameState): The current game state.
    """
    for stock in game.market:
        total_volume = stock.volume
        if total_volume <= 0:
            continue  # avoid division by zero

        net_movement = stock.movement["buys"] - stock.movement["sells"]
        delta = net_movement / total_volume
        old_price = stock.price
        stock.price = round(old_price + delta, 2)

        game.log_action(
            "Price Updated",
            stock.name,
            f"Old: {old_price:.2f}, New: {stock.price:.2f}, Δ: {delta:.4f}",
        )

        # Reset movement for next round
        stock.movement["buys"] = 0
        stock.movement["sells"] = 0


def update_options(game: GameState) -> None:
    """
    Updates the options (CALLs and PUTs) in the game.

    Args:
        game (GameState): The current game state.
    """
    expired = []

    for order in game.orderList:
        parts = order.split()
        if len(parts) != 6 or parts[0] not in ["CALL", "PUT"]:
            continue  # skip non-option orders

        order_type = parts[0]
        player_name = parts[1]
        stock_name = parts[2]
        strike_price = float(parts[3])
        premium = float(parts[4])
        expiry = int(parts[5])

        person = next((p for p in game.people if p.name == player_name), None)
        if not person:
            continue

        # Charge premium
        if person.amount >= premium:
            person.amount -= premium
            game.log_action(
                "Premium Charged",
                person.name,
                f"{order_type} {stock_name} | Premium: {premium}",
            )
        else:
            game.log_action(
                "Premium Skipped",
                person.name,
                f"Insufficient funds for {order_type} {stock_name}",
            )

        # Decrement expiry
        expiry -= 1
        if expiry <= 0:
            expired.append(order)
            game.log_action(
                "Option Expired",
                person.name,
                f"{order_type} {stock_name} at strike {strike_price}",
            )
        else:
            # Replace with updated expiry
            updated_order = (
                f"{order_type} {player_name} {stock_name} {strike_price} {premium}"
                f" {expiry}"
            )
            game.orderList[game.orderList.index(order)] = updated_order

    # Remove expired options
    for order in expired:
        game.orderList.remove(order)


def update_net_worths(game: GameState) -> None:
    """
    Updates the net worth of each player.

    Args:
        game (GameState): The current game state.
    """
    for p in game.people:
        stock_value = 0
        for h in p.stocks:
            try:
                name, vol, _ = h.split("D")
                stock = next((s for s in game.market if s.name.lower() == name), None)
                if stock:
                    stock_value += int(vol) * stock.price
            except:
                continue
        p.net_worth = p.amount + stock_value


def check_completion_or_advance(game: GameState) -> None:
    """
    Checks if the game is completed or advances to the next round.

    Args:
        game (GameState): The current game state.
    """
    if game.current_round >= game.rounds:
        print("\n🏁 Game Over! Calculating final standings...\n")
        update_net_worths(game)
        rankings = sorted(game.people, key=lambda p: p.net_worth, reverse=True)

        print("🏆 Final Rankings:")
        for i, p in enumerate(rankings, start=1):
            print(
                f"{i}. {p.name} — Net Worth: ₹{p.net_worth:.2f} (Cash: ₹{p.amount:.2f})"
            )

        winner = rankings[0]
        print(f"\n🎉 Winner: {winner.name} with ₹{winner.net_worth:.2f} net worth!")
        game.log_action(
            "Game Completed", winner.name, f"Won with ₹{winner.net_worth:.2f}"
        )
        global is_completed
        is_completed = True
    else:
        print(
            f"\n✅ Round {game.current_round} completed. Preparing for Round"
            f" {game.current_round + 1}...\n"
        )


def recalculate_market_volumes(game: GameState) -> None:
    """
    Recalculates current_market for each stock based on total volume minus player holdings.
    """
    for stock in game.market:
        held_volume = 0
        for p in game.people:
            for h in p.stocks:
                try:
                    name, vol, _ = h.split("D")
                    if name.lower() == stock.name.lower():
                        held_volume += int(vol)
                except:
                    continue
        stock.current_market = stock.volume - held_volume


# ------------------ Main ------------------


def main() -> None:
    """
    The main function to run the game.
    """
    global is_completed
    game = GameState()

    N = get_int("How many players do you want to add: ")
    if N is None or N <= 0:
        return

    starting_cash = get_float("How much should each player start with: ")
    if starting_cash is None or starting_cash <= 0:
        return

    print("\nRegistering players...")
    for i in range(N):
        name = input(f"Enter name for player {i + 1}: ")
        game.add_player(name, starting_cash)
    print("Player registration complete.\n")

    S = get_int("How many stocks do you want to add: ")
    if S is None or S <= 0:
        return

    print("\nRegistering stocks...")
    for i in range(S):
        name = input(f"Name of Stock {i + 1}: ")
        volume = get_int(
            "Number of shares for the stock: ",
            "Invalid entry --> Volume must be a positive integer",
        )
        capital = get_float(
            "Total capital for the stock: ",
            "Invalid entry --> Capital must be a positive float",
        )
        if volume is not None and capital is not None and volume > 0 and capital > 0:
            game.add_stock(name, volume, capital)
        else:
            print("Stock registration failed\n")

    rounds = get_int(
        "How many rounds should the game have: ", "Rounds should be greater than 1"
    )
    if rounds is None or rounds <= 0:
        return
    game.rounds = rounds

    print("\nAll initializations completed. Ready for simulation.")
    display_game_state(game)

    # lets strat the game
    print(" L-E-T-'S--S-T-A-R-T")
    print("ROUND - 0")
    while not is_completed:
        print("Game stats")
        display_game_state(game)
        print("\ngathering orders")
        for p in game.people:
            while True:
                print(f"getting order for {p.name}")
                print(
                    """1 -- buy
                    2 -- sell
                    3 -- get calls
                    4 -- get puts
                    5 -- condition"""
                )
                try:
                    choice = int(input("Enter choice :  "))
                except ValueError:
                    print("Please enter an integer")
                    print("order cancelled")
                    continue
                if choice < 1 or choice > 5:
                    print("Please enter an integer between 1 and 5")
                    print("order cancelled")
                    continue
                print("For which stock would you like the order :  ")
                for s in game.market:
                    print(s)
                name = input("Enter stock name , if failed order will be cancelled :  ")
                status = get_order(game, p, choice, name)
                print(status)
                try:
                    ask = int(
                        input(
                            "Press any number to end ordering, or any letter to"
                            " continue: "
                        )
                    )
                    print("\n\n\n\n")
                    break
                except ValueError:
                    continue

        print("\n\n-- order gathering completed --\n\n")
        # [X] 1  -- list all order
        for order in game.orderList:
            if order.split()[0] != "COND":
                print(order)
            else:
                print(f"COND for {order.split()[1]}")
        # [X] 2  -- complete affirmative orders --------------------------------- remove them from list ----
        complete_order(game)
        # [X] 3  -- announce completions for each player ------------------------ in chat ----
        # [X] 4  -- change net movements while doing orders --------------------- update share property in and out ---
        # [X] 5  -- convert possible conditional orders to affirmative ---------- do-able orders to confirm ---
        convert_orders(game)
        complete_order(game)
        # [X] 6  -- update prices ----------------------------------------------- update prices on current moves ---\
        update_stocks(game)
        # [X] 7  -- check conditional chances, if possible to confirm ----------- do as step 5 again for new prices ---\
        convert_orders(game)
        complete_order(game)
        # [X] 8  -- deliver new calls and puts ---------------------------------- assign new calls and puts at the premium ---\
        # [X] 9  -- update all calls and puts , ready for next round ------------ get calls and puts ready for next round ---\
        update_options(game)
        # [ ] 10 -- update prices ----------------------------------------------- update prices on current moves ---\
        update_stocks(game)
        recalculate_market_volumes(game)
        # [X] 11 -- announce all completed processes and announce them ---------- all logged and ready ---\
        # [ ] 12 -- ready for new round / check if completed --> announce winner  check completion (yes or now) or next round
        check_completion_or_advance(game)
        game.current_round += 1


if __name__ == "__main__":
    main()
