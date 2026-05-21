import automaton_parser as parser


# DFA stands for deterministic finite automaton M is a 5-tuple, (Q, Sigma, delta, q0, F).


def parseRules(rule_lines):
    rules = {}

    for line in rule_lines:
        source_state, symbol, destination_state = line.split(",")
        source_state = source_state.strip()
        symbol = symbol.strip()
        destination_state = destination_state.strip()

        if source_state not in rules:
            rules[source_state] = {}

        if symbol in rules[source_state]:
            if destination_state != rules[source_state][symbol]:
                raise Exception(
                    "We have 2 rules with same source state and symbols and different outcomes (destination states)"
                )
        else:
            rules[source_state][symbol] = destination_state

    return rules


def parseFile(inputDfaFile):
    sections = parser.parse_sections(inputDfaFile)

    states = sections.get("States", [])
    sigma = sections.get("Sigma", [])
    rules = parseRules(sections.get("Rules", []))

    start_section = sections.get("Start", [])
    if len(start_section) == 0:
        start = "None"
    elif len(start_section) == 1:
        start = start_section[0]
    else:
        raise Exception("A DFA can only have one start state")

    accept = sections.get("Accept", [])

    dfa = states, sigma, rules, start, accept
    if not isDfaValid(dfa):
        return False
    else:
        return dfa


def isDfaValid(DFA):
    states, sigma, rules, start, accept = DFA  # getting values from 5-tuple

    if len(states) == 0:
        raise Exception("States are not defined")
        return False

    if len(sigma) == 0:
        raise Exception("Alphabet is not defined")
        return False

    if start == "None":
        raise Exception("Start state is not defined")
        return False
    elif start not in states:
        raise Exception(f"Start state {start} is not defined")
        return False

    if accept == []:
        raise Exception("Accept state is not defined")
        return False
    else:
        for acceptState in accept:
            if acceptState not in states:
                raise Exception(f"Accept state {acceptState} is not defined")
                return False

    for sourceState in rules: # rules dict key is the source state of the rule
        if sourceState not in states:
            raise Exception(f"Source state {sourceState} is not defined in the states list for the DFA")
            return False

        for symbol in rules[sourceState]:
            if symbol not in sigma:
                raise Exception(f"Symbol {symbol} is not defined in the alphabet for the DFA")
                return False

            destinationState = rules[sourceState][symbol]
            if destinationState not in states:
                raise Exception(
                    f"Destination state {destinationState} is not defined in the states list for the DFA"
                )
                return False

    return True


def printDfaDataStructures(DFA):
    states, sigma, rules, start, accept = DFA # getting values from 5-tuple

    print(f"States : {states}")
    print(f"Alphabet : {sigma}")
    print(f"Rules : {rules}")
    print(f"Start state : {start}")

    if len(accept) != 1:
        print(f"Accept states : {accept}")
    else:
        print(f"Accept state: {accept[0]}")


def isStringValid(string, stringSeparator, sigma):
    for symbol in splitIncludingNoSeparator(string, stringSeparator):
        if symbol not in sigma:
            return False
    return True


'''
def searchRuleAndReturnState(currentState, currentSymbol, rules):
    # removes redudant code (would be used twice, depending if separator is "" or not)
    if currentState in rules:
        if currentSymbol in rules[currentState]:
            currentState = rules[currentState][currentSymbol] # destination state of the existing rule
            return currentState
        else:
            return currentState # considered by default for every state, 
                                # if not specified a rule for the current symbol
                                # 
    else:
        return currentState

    # if there isn't any rule with the source state we have, or with the source state and the symbol we got from the sequence
    raise UndefinedRuleError(f"Rule {currentState}, {currentSymbol}, destination state not existent")
'''

def getNextState(currentState, currentSymbol, rules):
    if currentState not in rules:
        return currentState
    elif currentSymbol not in rules[currentState]:
        return currentState
    else:
        return rules[currentState][currentSymbol]# the DFA goes to the state specified by the rule


def splitIncludingNoSeparator(string, separator):
    if separator == "":
        return string # would need an if-else statement within the runDfa function
    else:             # removes redudant code, by calling getNextState only once
        return string.split(separator)


def runDfa(DFA, inputString, stringSeparator, printDFASteps=True):
    states, sigma, rules, start, accept = DFA  # getting values from 5-tuple
    if not isDfaValid(DFA):
        raise Exception("DFA not valid")

    inputString = inputString.strip() # removes whitespace, \n, from left and right
    if not isStringValid(inputString, stringSeparator, sigma):
        raise Exception(
            "Input string contains symbols not in the given alphabet of the DFA. Possible problem: wrong string separator used when running the file."
        )

    currentState = start # first state is the start state of the DFA
    if printDFASteps is True:
        print(currentState)

    for currentSymbol in splitIncludingNoSeparator(inputString, stringSeparator):
        if printDFASteps is True:
            print(currentSymbol)

        currentState = getNextState(currentState, currentSymbol, rules)
        # function searches through the rules and finds the correct one
        # improved time efficiency wise by using two hashmaps - dictionaries, for O(1) search time

        if printDFASteps is True:
            print(currentState) # printing the new state of the DFA after every symbol

    if currentState in accept:  # after the for loop exits the currentState variable stores the last state
        return True             # of the DFA, if it is valid return true
    else:
        return False
