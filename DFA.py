# DFA stands for deterministic finite automaton M is a 5-tuple, (Q, Σ, δ, q0, F), consisting of

def isComment(string):
    return string.startswith("#")
    # return string[0] == "#" would raise an IndexError for an empty string ""

def isEmptyLine(string):
    return string == ""

def parseFile(inputDfaFile):
    lines = inputDfaFile.readlines()
    currentSection = "None"
    states = []
    sigma = []
    rules = {}
    start = "None" # a dfa can only have one start state
    accept = [] # a dfa can have multiple accept states
    inMultipleLineComment = False
    for line in lines:
        line = line.strip() # eliminating whitespace
        if line[0] == "[": # new section starts here, filtering opening and closing pharantesis
            currentSection = line[1:-1]
            continue
        if line == "End":
            currentSection = "None" # searching for new section tag ([SectionName])
            continue

        if currentSection == "None":
            continue # skipping line, still searching for section tags ([SectionName])
        if currentSection == "States":
            states.append(line)
            continue
        if currentSection == "Sigma":
            sigma.append(line)
            continue
        if currentSection == "Rules":
            sourceState, symbol, destinationState = line.split(",")
            sourceState = sourceState.strip()
            symbol = symbol.strip()
            destinationState = destinationState.strip()
            if sourceState in rules:
                if symbol in rules[sourceState]:
                    if destinationState != rules[sourceState][symbol]:
                        raise   Exception("We have 2 rules with same source state and symbols and different outcomes (destination states)")
                        return False # DFA is not valid; it would not know which of the two rules to follow for the specific input state and symbol
                else:
                    rules[sourceState][symbol] = destinationState
            else: # we don't have any rules with this source state yet, so we initialise the dictionary with this first rule
                rules[sourceState] = {symbol : destinationState}
        if currentSection == "Start":
            start = line
            continue
        if currentSection == "Accept":
            accept.append(line)
            continue

    inputDfaFile.close()

    DFA = states, sigma, rules, start, accept
    if not isDfaValid(DFA):
        return False
    else:
        # returning 5-tuple of lists
        return DFA


def isDfaValid(DFA):

    states, sigma, rules, start, accept = DFA # getting values from 5-tuple
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
                raise Exception(f"Destination state {destinationState} is not defined in the states list for the DFA")
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
        print(f"Accept state: {accept[0]}") # to show singular form if needed and not a list with only one element


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
        return rules[currentState][currentSymbol] # the DFA goes to the state specified by the rule

def splitIncludingNoSeparator(string, separator):
    if separator == "" :
        return string  # would need an if-else statement within the runDfa function
    else:                # removes redudant code, by calling getNextState only once
        return string.split(separator)

def runDfa(DFA, inputString, stringSeparator, printDFASteps = True):

    states, sigma, rules, start, accept = DFA # getting values from 5-tuple
    if not isDfaValid(DFA):
        raise Exception("DFA not valid")

    inputString = inputString.strip() # removes whitespace, \n, from left and right
    if not isStringValid(inputString, stringSeparator, sigma):
        raise Exception("Input string contains symbols not in the given alphabet of the DFA. Possible problem: wrong string separator used when running the file.")


    currentState = start # first state is the start state of the DFA
    if printDFASteps == True:
        print(currentState) # printing starting state

    for currentSymbol in splitIncludingNoSeparator(inputString, stringSeparator):
            if printDFASteps == True:
                print(currentSymbol) # printing every symbol in the string

            currentState = getNextState(currentState, currentSymbol, rules)
            # function searches through the rules and finds the correct one
            # improved time efficiency wise by using two hashmaps - dictionaries, for O(1) search time

            if printDFASteps == True:
                print(currentState)  # printing the new state of the DFA after every symbol

    if currentState in accept: # after the for loop exits the currentState variable stores the last state
        return True            # of the DFA, if it is valid return true
    else:
        return False


