from lib.deck import Deck 
from lib.grid import Grid


def main():
    deck = Deck()
    init_size = deck.remain

    first_card = deck.draw()
    second_card = deck.draw()
    next_five_cards = deck.draw_n(5) 

    final_size = deck.remain

    print(f"""
          

    nombre de carte: {init_size}

    premier tirage: {first_card}

    second tirage: {second_card}

    cinq prochains tirages: {next_five_cards}

    nombre de carte après les tirage: {final_size}


    """)

    board = Grid(5, 5)

    print(f"Only the First Tile:\n{board}")

    board._add_node(0, 1)    #Two Node = Two Tile = One Domino
    board._add_node(0, 2)

    print(f"With 1 domino:\n{board}")

    board._add_node(1, 2)
    board._add_node(2, 2)

    print(f"With 2 dominos:\n{board}")

    board._add_node(0, -1)
    board._add_node(-1, -1)

    print(f"With 3 dominos:\n{board}")

    

    print(" 'X' -> No Domino/Node Allowed")
    print(" '.' -> Domino/Node Allowed")
    print(" '#' -> A Domino/Node")
    print(" 'O' -> Initial Domino")


if __name__ == "__main__":
    main()

