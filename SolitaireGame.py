import os
import random
import signal
import sys 

def signal_handler(sig, frame):
    sys.exit(0)
    
signal.signal(signal.SIGINT, signal_handler)

def initialize_deck():
    ranks = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']  # Use lowercase for all ranks
    suits = ['C', 'D', 'H', 'S']
    deck = [f"{suit.upper() if suit in ['H', 'D'] else suit.lower()}{rank.upper()}" for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def initialize_piles(deck):
    piles = [[] for _ in range(7)]
    for i in range(7):
        for j in range(i + 1):
            piles[i].append(deck.pop() if i == j else "[]")
    return piles

def print_board(last_action):
    os.system("clear" if os.name == "posix" else "cls")
    print("S  O  L  I  T  A  I  R  E\n")
    print(f"s: {display_stock(stock, last_action)} A: {display_pile(piles_dict['A'])} B: {display_pile(piles_dict['B'])} C: {display_pile(piles_dict['C'])} D: {display_pile(piles_dict['D'])}")
    print("         1:        2:        3:        4:        5:        6:        7:")
    for i in range(max(len(p) for p in piles)):
        print_board_row([p[i] if i < len(p) and p[i] != "[]" else "[]" for p in piles])

def display_pile(pile):
    return "XX" if not pile or pile == "[]" else pile[-1]

def display_stock(stock, last_action):
    if last_action == "DEAL":
        return "[Hidden]" if not stock else f"[{stock[-1]}]"
    else:
        return "[ ]"

def print_board_row(row):
    row_str = "         "
    for card in row:
        row_str += f"{card}        "
    print(row_str)

def move_card():
    global history_stack
    print_board("MOVE")

    card_to_move = input("Card to move: ").upper()

   
    if card_to_move in stock:
        target_pile_input = input("Target pile: ").upper()

        if target_pile_input == "S":
        
            stock.remove(card_to_move)
            piles_dict["S"].append(card_to_move)
            print(f"Moved {card_to_move} to s pile")
        elif target_pile_input in ["A", "B", "C", "D"]:
          
            rank_to_move = card_to_move[1:]
            if rank_to_move.isdigit():
                rank_to_move = int(rank_to_move)
            else:
                rank_to_move = 11 if rank_to_move.upper() == 'J' else 12 if rank_to_move.upper() == 'Q' else 13 if rank_to_move.upper() == 'K' else 0

            target_pile = piles_dict[target_pile_input]

            if target_pile and target_pile[-1] != "[]" and rank_to_move > int(target_pile[-1][1:]):
                print("Move Invalid!")
                return

            target_pile.append(card_to_move)
            print(f"Moved {card_to_move} to {target_pile_input}")
        elif target_pile_input in ["1", "2", "3", "4", "5", "6", "7"]:
            target_pile_index = int(target_pile_input) - 1
            target_pile = piles[target_pile_index]
            rank_to_move = int(card_to_move[1:]) if card_to_move[1:].isdigit() else 0

            if target_pile and target_pile[-1] != "[]" and rank_to_move > int(target_pile[-1][1:]):
                print("Move Invalid!")
                return

            target_pile.append(card_to_move)
            print(f"Moved {card_to_move} to pile {target_pile_input}")
        else:
            print("Error: Invalid target pile.")
    else:
       
        source_pile_index = -1
        source_card_index = -1

        for i, pile in enumerate(piles):
            for j, card in enumerate(pile):
                if card != "[]" and card_to_move[:-1].upper() == card[:-1].upper():
                    source_pile_index = i
                    source_card_index = j
                    break
            if source_pile_index != -1:
                break

        if source_pile_index == -1 or source_card_index == -1:
            print("Error: Card(s) not found in any source pile or stock.")
            return

        source_pile = piles[source_pile_index]

        target_pile_input = input("Enter target pile index (1-7 or A-D): ").upper()

        if target_pile_input in ["A", "B", "C", "D"]:
            target_pile = piles_dict[target_pile_input]
            rank_to_move = int(card_to_move[1:]) if card_to_move[1:].isdigit() else 0

            if target_pile and target_pile[-1] != "[]" and rank_to_move > int(target_pile[-1][1:]):
                print("Move Invalid!")
                return

            print(f"Moved {card_to_move} to {target_pile_input}")
        elif target_pile_input in ["1", "2", "3", "4", "5", "6", "7"]:
            target_pile_index = int(target_pile_input) - 1
            target_pile = piles[target_pile_index]
            rank_to_move = int(card_to_move[1:]) if card_to_move[1:].isdigit() else 0

            if target_pile and target_pile[-1] != "[]" and rank_to_move > int(target_pile[-1][1:]):
                print("Move Invalid!")
                return

            print(f"Moved {card_to_move} to pile {target_pile_input}")
        else:
            print("Error: Invalid target pile.")
            return
        moved_card = source_pile.pop(source_card_index)
        target_pile.append(moved_card)
  
        current_state = (stock.copy(), [pile[:] for pile in piles], last_action)
        history_stack.append(current_state)
        history_stack = history_stack[-max_undo_moves:]


    print_board("MOVE")

def deal_stock():
    global stock
    global last_action
    if stock:
        card_to_move = stock[-1]
        print_board("DEAL")
        print(f"Stock card: [Hidden]")

        while True:
            sub_choice = input("\n[ 1 ]   Move\n[ 2 ]   Deal \n[ 3 ]   Return to Main Menu \n[ CTRL - C ] Exit\nEnter your choice: ")

            if sub_choice == "1":
                move_card()
                break
            elif sub_choice == "2":
                target_pile_input = input("Target pile: ").upper()

                if target_pile_input in ["A", "B", "C", "D"]:
                    target_pile = piles_dict[target_pile_input]
                    
                    target_pile.append(card_to_move)
                    stock.pop()
                    last_action = "DEAL"
                    print_board(last_action)
                  
                elif target_pile_input in ["1", "2", "3", "4", "5", "6", "7"]:
                    target_pile_index = int(target_pile_input) - 1
                    target_pile = piles[target_pile_index]
                   
                    target_pile.append(card_to_move)
                    stock.pop()  
                    last_action = "DEAL"
                    print_board(last_action)
                   
                elif target_pile_input == "S":
                    print("Error: Cannot deal to stock.")
                else:
                    print("Error: Invalid target pile.")
                    continue
            elif sub_choice == "3":
                break
            elif sub_choice.upper() == "CTRL-C":
                exit()
            else:
                print("Error: Invalid choice.")
    else:
        print("Error: Stock is empty.")
    
def save_game(stock, foundations, piles, visible_counts, visible_stock_card, filename="save.txt"):
    with open(filename, 'w') as file:
       
        file.write(f"{len(stock)} {visible_stock_card}\n")
        if stock:
            file.write(" ".join(stock) + "\n")
        else:
            file.write("\n")

        file.write(" ".join(foundations) + "\n")

       
        for i, pile in enumerate(piles, start=1):
            visible_count = visible_counts[i - 1]
            file.write(f"{len(pile)} {' '.join(pile)} {visible_count}\n")

def load_game(filename="save.txt"):
    if not os.path.exists(filename):
        print("Error: Save file not found.")
        return None, None, None, None, None

    with open(filename, 'r') as file:
   
        stock_line = file.readline().split()
        n_stock = int(stock_line[0])
        visible_stock_card = stock_line[1]
        stock = file.readline().split() if n_stock > 0 else []

       
        foundations = file.readline().split()

        piles = []
        visible_counts = []
        for _ in range(7):
            pile_line = file.readline().split()
            n_pile = int(pile_line[0])
            pile = pile_line[1:-1] 
            visible_count = int(pile_line[-1])
            piles.append(pile)
            visible_counts.append(visible_count)
        
    return stock, foundations, piles, visible_counts, visible_stock_card

def undo_move():
    global history_stack
    global stock
    global piles
    global last_action
    

    if len(history_stack) > 1: 
        previous_state = history_stack.pop()

       
        stock, piles, last_action = previous_state

        print("Undo successful.")
        print_board(last_action)
    else:
        print("Cannot undo. No previous state or already at the initial state.")

max_undo_moves = 5
history_stack = []


deck = initialize_deck()
piles = initialize_piles(deck)
stock = deck[:24]
deck = deck[24:]
current_deck_index = 24  


pile_a = []
pile_b = []
pile_c = []
pile_d = []
pile_s = []
piles_dict = {"A": pile_a, "B": pile_b, "C": pile_c, "D": pile_d, "S": pile_s}

last_action = ""
print_board(last_action)

while True:
    print("\n[ 1 ]   Move\n[ 2 ]   Deal \n[ 3 ]   Save \n[ 4 ]   load\n[ 5 ]   Undo \n[ CTRL - C ] Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        move_card()
    elif choice == "2":
        deal_stock()
    elif choice == "3":
        save_filename = input("Enter the save file name: ")
        save_game(stock, [display_pile(piles_dict['A']), display_pile(piles_dict['B']), display_pile(piles_dict['C']), display_pile(piles_dict['D'])], piles, [len(p) - 1 for p in piles], display_stock(stock, last_action), filename=save_filename)
        print(f"Game saved to {save_filename}.")
    elif choice == "4":
        load_filename = input("Enter the load file name: ")
        loaded_stock, loaded_foundations, loaded_piles, loaded_visible_counts, loaded_visible_stock_card = load_game(filename=load_filename)
        if loaded_stock is not None:
            stock = loaded_stock
            piles = loaded_piles
            visible_counts = loaded_visible_counts
            last_action = "DEAL" if loaded_visible_stock_card == "[Hidden]" else ""
            print(f"Game loaded from {load_filename}.")
            print_board(last_action)
    elif choice == "5":
        undo_move()
    elif choice.upper() == "CTRL-C":
        break
    else:
        print("Error: Invalid choice.")