import json
import os
import random
import sys
from logger import LoggerIn, LoggerOut, log_methods, my_log
from setup import *


class Flashcards:
    def __init__(self, cards, template, log_method):
        self.cards = cards
        self.template = template
        self.log_file = log_method

    def quiz(self):
        print('How many times to ask?')
        n = int(input())
        for _ in range(n):
            card = random.choice(list(self.cards.keys()))
            answer = self.cards[card][0]
            definitions = [def_ for def_, _ in self.cards.values()]
            print(f'Print the {self.template[1].split(" ", 1)[0]} of "{card}":')
            trial = input()
            if trial == answer:
                print('Correct!')
            elif trial not in definitions:
                print(f'Wrong. The right answer is "{answer}".')
                self.cards[card][1] += 1
            else:
                for card, def_err in self.cards.items():
                    if def_err[0] == trial:
                        print(f'Wrong. The right answer is "{answer}", but your definition is correct for "{card}".')
                        self.cards[card][1] += 1

    def menu(self):
        while 555 < 666:
            print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
            inp = input()
            if inp != 'ask':
                card_manager = Card(inp)
                if inp == 'exit':
                    break
                card_manager.apply_action()
            else:
                self.quiz()
        print('bye bye')
        try:
            os.remove(log_methods[1])
        except:
            pass


class Card(Flashcards):
    def __init__(self, mode):
        super().__init__(my_cards, my_template, my_log)
        self.mode = mode
        self.user_manager = User(self.mode)
        self.errs = [err for _, err in self.cards.values()]
        self.hard = [card for card, v in my_cards.items() if v[1] == max(self.errs)]

    def add(self, err=0):
        new_card = []
        for k_or_v in self.template:
            self.user_manager = User(self.mode, k_or_v)
            entry = self.user_manager.get_input()
            new_card.append(entry)
        self.cards |= {new_card[0]: [new_card[1], err]}
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

    def log(self):
        user_log = self.user_manager.get_input()
        if self.log_file == log_methods[0]:
            with open(user_log, 'w') as file:
                file.write(self.log_file.getvalue())
        else:
            os.system(f'attrib -h {log_methods[1]}')  # unhide default log file
            os.rename(self.log_file, user_log)
            sys.stdout = LoggerOut(user_log)
            sys.stdin = LoggerIn(user_log)
        print('The log has been saved.')

    def hardest(self):
        if self.cards and max(self.errs) > 0:
            print(f'The hardest card{"s"[:len(self.hard)^1]} {"is" if len(self.hard) == 1 else "are"} '
                  f'{", ".join(self.hard)}. '
                  f'You have {max(self.errs)} error{"s"[:max(self.errs)^1]} answering '
                  f'{"it" if len(self.hard) == 1 else "them"}.')
        else:
            print('There are no cards with errors.')

    def reset_stats(self):
        for _, def_err in self.cards.items():
            def_err[1] = 0
        print('Card statistics have been reset.')

    def apply_action(self):
        if self.mode == 'add':
            self.add()
        if self.mode == 'remove':
            self.remove()
        if self.mode == 'import':
            self.load()
        if self.mode == 'export':
            self.export()
        if self.mode == 'log':
            self.log()
        if self.mode == 'hardest card':
            self.hardest()
        if self.mode == 'reset stats':
            self.reset_stats()


class User(Flashcards):
    def __init__(self, mode, k_or_v=''):
        super().__init__(my_cards, my_template, my_log)
        self.mode = mode
        self.k_or_v = k_or_v
        self.definitions = [def_ for def_, _ in self.cards.values()]
        self.search_in = \
            self.cards.keys() if not self.k_or_v or not self.template.index(self.k_or_v) else self.definitions

    def get_input(self):
        if self.mode == 'add':
            print(f'The {self.k_or_v}:')
            while 555 < 666:
                try:
                    entry = input()
                    err_message = f'The {self.k_or_v.split(" ", 1)[0]} "{entry}" already exists. Try again:'
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

        if self.mode == 'export' or self.mode == 'log':
            print('File name:')
            return input()

        if self.mode == 'import':
            print('File name:')
            file_name = input()
            if os.path.exists(file_name):
                return file_name
            else:
                print('File not found.')


sys.stdout = LoggerOut(my_log)
sys.stdin = LoggerIn(my_log)

my_quiz = Flashcards(my_cards, my_template, my_log)
my_quiz.menu()
