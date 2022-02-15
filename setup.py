import json
import os
import random


class Flashcards:
    def __init__(self, cards, template):
        self.cards = cards
        self.template = template


    def quiz(self):
        print('How many times to ask?')
        n = int(input())
        for _ in range(n):
            card = random.choice(list(self.cards.keys()))
            correct_definition = self.cards[card]
            print(f'Print the {self.template[1]} of "{card}":')
            trial = input()
            if trial == correct_definition:
                print('Correct!')
            elif trial not in self.cards.values():
                print(f'Wrong. The right answer is "{correct_definition}".')
            else:
                another_card = {v: k for k, v in self.cards.items()}[trial]
                print(f'Wrong. The right answer is "{correct_definition}", '
                      f'but your definition is correct for "{another_card}".')

    def menu(self):
        while 555 < 666:
            print('Input the action (add, remove, import, export, ask, exit):')
            inp = input()
            if inp != 'ask':
                card_manager = Card(inp)
                if inp == 'exit':
                    break
                card_manager.apply_action()
            else:
                self.quiz()
        print('bye bye')


class Card(Flashcards):
    def __init__(self, mode):
        super().__init__(my_cards, my_template)
        self.mode = mode
        self.user_manager = User(self.mode)

    def add(self):
        new_card = []
        for k_or_v in self.template:
            self.user_manager = User(self.mode, k_or_v)
            entry = self.user_manager.get_input()
            new_card.append(entry)
        self.cards |= {new_card[0]: new_card[1]}
        print(f'The pair ("{new_card[0]}":"{new_card[1]}") has been added.')

    def remove(self):
        if self.cards.items():
            entry = self.user_manager.get_input()
            if entry:
                del self.cards[entry]
                print('The card has been removed.')
        else:
            print('Nothing to remove')

    def load(self):
        entry = self.user_manager.get_input()
        if entry:
            with open(entry, 'r') as file:
                imported_cards = json.loads(file.read())
                self.cards |= imported_cards
            print(f'{len(imported_cards)} card{"s"[:len(imported_cards) ^ 1]} '
                  f'ha{"s" if len(imported_cards) == 1 else "ve"} been loaded.')

    def export(self):
        entry = self.user_manager.get_input()
        with open(entry, 'w') as file:
            file.write(json.dumps(self.cards, indent=4))
        print(f'{len(self.cards)} card{"s"[:len(self.cards) ^ 1]} '
              f'ha{"s" if len(self.cards) == 1 else "ve"} been saved.')


    def apply_action(self):
        if self.mode == 'add':
            self.add()
        if self.mode == 'remove':
            self.remove()
        if self.mode == 'import':
            self.load()
        if self.mode == 'export':
            self.export()


class User(Flashcards):
    def __init__(self, mode, k_or_v=''):
        super().__init__(my_cards, my_template)
        self.mode = mode
        self.k_or_v = k_or_v
        self.search_in = \
            self.cards.keys() if not self.k_or_v or not self.template.index(self.k_or_v) else \
                self.cards.values()

    def get_input(self):
        if self.mode == 'add':
            print(f'The {self.k_or_v}:')
            while 555 < 666:
                try:
                    entry = input()
                    err_message = f'The {self.k_or_v} "{entry}" already exists. Try again:'
                    assert entry not in self.search_in, err_message
                    return entry
                except AssertionError as err:
                    print(err)

        if self.mode == 'remove':
            print('Which card?')
            try:
                entry = input()
                err_message = f'Can\'t remove "{entry}": there is no such card.'
                assert entry in self.search_in, err_message
                return entry
            except AssertionError as err:
                print(err)

        if self.mode == 'export':
            print('File name:')
            return input()

        if self.mode == 'import':
            print('File name:')
            file_name = input()
            if os.path.exists(file_name):
                return file_name
            else:
                print('File not found.')

# cards start up db
my_cards = {}

# cards front/back definitions
my_template = [
    'card',
    'definition'
]

my_quiz = Flashcards(my_cards, my_template)
my_quiz.menu()
