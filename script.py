from io import StringIO
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--import_from')
parser.add_argument('--export_to')
args = parser.parse_args()

memory_file = StringIO()
questions = {}


def write_log(string):
    memory_file.read()
    memory_file.write(string)


def print_log(string):
    print(string)
    write_log(string)


def create_card(no):
    print(f'The term for card #{no}:')
    while True:
        term = input()
        if term in questions:
            print(f'The term "{term}" already exists. Try again!')
        else:
            break
    print(f'The definition for card #{no}:')
    while True:
        definition = input()
        if definition in questions.values():
            print(f'The definition "{definition}" already exists. Try again!')
        else:
            break
    questions[term] = definition


def ask(question):
    print_log(f'Print the definition of "{question}":')
    answer = input()
    write_log(answer)
    if answer == questions[question][0]:
        print_log('Correct!')
    else:
        questions[question][1] += 1
        if answer in [val[0] for val in list(questions.values())]:
            key = list(questions.keys())[[val[0] for val in list(questions.values())].index(answer)]
            print_log(f'Wrong. The right answer is "{questions[question][0]}", '
                      f'but your definition is correct for "{key}".')
        else:
            print_log(f'Wrong. The right answer is "{questions[question][0]}".')


def add_card():
    print_log('The card:')
    while True:
        term = input()
        write_log(term)
        if term in questions:
            print_log(f'The card "{term}" already exists.')
        else:
            break
    print_log('The definition of the card:')
    while True:
        definition = input()
        write_log(definition)
        if definition in (questions[key][0] for key in questions):
            print_log(f'The definition "{definition}" already exists.')
        else:
            break
    questions[term] = [definition, 0]
    print_log(f'The pair ("{term}":"{definition}" has been added.')


def remove_card():
    print_log('Which card?')
    card = input()
    write_log(card)
    if card in questions:
        del questions[card]
        print_log('The card has been removed.')
    else:
        print_log(f'Can\'t remove "{card}": there is no such card.')


def import_cards(exp=None):
    if exp is None:
        print_log('File name:')
        filename = input()
        write_log(filename)
    else:
        filename = exp
    try:
        with open(filename) as file:
            lines = 0
            for line in file:
                term, definition, stats = line.split()
                questions[term] = [definition, int(stats)]
                lines += 1
            print_log(f'{lines} cards have been loaded.')
    except FileNotFoundError:
        print_log('File not found.')


def export_cards(exp=None):
    if exp is None:
        print_log('File name:')
        filename = input()
        write_log(filename)
    else:
        filename = exp
    with open(filename, 'w') as file:
        lines = 0
        for key, value in questions.items():
            file.write(f'{key} {value[0]} {value[1]}\n')
            lines += 1
        print_log(f'{lines} cards have been saved.')


def main():
    if args.import_from:
        import_cards(exp=args.import_from)
    while True:
        print_log('\nSelect the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
        entry = input()
        write_log(entry)
        if entry == 'add':
            add_card()
        elif entry == 'remove':
            remove_card()
        elif entry == 'import':
            import_cards()
        elif entry == 'export':
            export_cards()
        elif entry == 'ask':
            print_log('How many times to ask?')
            keys = tuple(questions.keys())
            times = int(input())
            write_log(str(times))
            for i in range(times):
                question = keys[i % len(keys)]
                ask(question)
        elif entry == 'exit':
            if args.export_to:
                export_cards(exp=args.export_to)
            print_log('Bye!')
            break
        elif entry == 'log':
            print_log('File name:')
            filename = input()
            write_log(filename)
            with open(filename, 'w') as log:
                for line in memory_file.getvalue():
                    log.write(line)
            print_log('The log has been saved.')
        elif entry == 'hardest card':
            try:
                maximum = max(questions[key][1] for key in questions)
            except ValueError:
                maximum = 0
            if maximum == 0:
                print_log('There are no cards with errors.')
            else:
                hardest = []
                for key, value in questions.items():
                    if value[1] == maximum:
                        hardest.append('"' + key + '"')
                if len(hardest) == 1:
                    print_log(f'The hardest card is {hardest[0]}. You have {maximum} errors answering it.')
                else:
                    print_log(f'The hardest cards are {", ".join(hardest)}. You have {maximum} errors answering it.')
        elif entry == 'reset stats':
            for key in questions:
                questions[key][1] = 0
            print_log('Card statistics have been reset.')
        else:
            print_log('Invalid entry.')


main()
