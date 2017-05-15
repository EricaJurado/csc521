import sys
import re

# Quirk keywords
keywords = [
    ('VAR', 'var'),
    ('FUNCTION', 'function'),
    ('RETURN', 'return'),
    ('PRINT', 'print')
]

# Quirk token lexeme pairs
tokenLexeme = [
    ('ASSIGN', r'='),
    ('ADD', r'[+]'),
    ('SUB', r'[-]'),
    ('MULT', r'[*]'),
    ('DIV', r'\/'),
    ('EXP', r'\^'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA', r','),
    ('COLON', r':'),

    ('NUMBER', r'((\d+(\.\d*)?)|(\.\d+))'),
    ('IDENT', r'[a-zA-Z]+[a-zA-Z0-9_]*')
]


def lex(stringToLex):
    """
    Lex uses regex functionality to create token and token lexeme pairs.

    Returns list of token and token lexeme pairs that will be passed to the
    parser.
    """
    # will hold lexed items
    lexedList = []
    currentIndex = 0

    # regex joins all pairs in tokenLexeme list to be used to see if
    # any token is within the string passed in
    myRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenLexeme)
    matchedToken = re.compile(myRegex).match

    current = matchedToken(stringToLex)
    # while there's still more of the string to search through...
    while current is not None:
        # get the current group to check
        typ = current.lastgroup
        # if the current group isn't 'SKIP' token (it's a something we care
        # about) ...
        if typ != 'SKIP':
            val = current.group(typ)
            if typ == 'IDENT':
                found = False
                for pair in keywords:
                    if pair[1] == val:
                        # If this condition is met, it's not actually an ident!
                        # It's a keyword. Therefore we should add the keywords
                        # to our lexedList directly.
                        lexedList.append((pair[0]))
                        found = True
                        break
                if found is False:
                    # If this condition is met, we know for sure it's an IDENT.
                    # We append the ident token lexeme pair to our lexedList.
                    lexedList.append(("IDENT" + ":" + val))
            elif typ == 'NUMBER':
                # If this condition is met, we know that it's a NUMBER and
                # can directionly append it to our lexedList.
                lexedList.append(("NUMBER" + ":" + str(val)))
            else:
                # Since it's a mached token and isn't a keyword, ident, or
                # or number, we know it must be another token. We can add this
                # directly to our lexedList.
                lexedList.append((typ))

        # updates our currentIndex
        currentIndex = current.end()
        # updates our current matchedToken based off our new index
        current = matchedToken(stringToLex, currentIndex)

    if currentIndex != len(stringToLex):
        raise Exception('Unexpected char %s' % (stringToLex[currentIndex]))

    return lexedList


if __name__ == '__main__':
    lexerOutput = ""
    # So we don't confuse a skip sequence as a true tokenLexeme pair...
    # we're going to add it here for clarity.
    tokenLexeme.append(('SKIP', r'[\s+]|\n'))

    # Reads all input from cmd line, lexes it, and adds it to lexerOutput string
    for part in sys.stdin.readlines():
        lexerOutput += ' '.join(lex(part))

    # Parser requries EOF marker
    lexerOutput += " EOF"

    print(lexerOutput)
