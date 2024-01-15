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

if __name__ == "__main__":
    main()

