import sys
import re

keywords = [
    ('VAR', 'var'),
    ('FUNCTION', 'function'),
    ('RETURN', 'return'),
    ('PRINT', 'print')
]

tokenLexeme = [
    ('ASSIGN', r'='),
    ('ADD', r'[+]'),
    ('SUB', r'[-]'),
    ('MULT', r'[*]'),
    ('DIV', r'\/'),
    ('EXP', r'\^'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('COMMA', r','),
    ('COLON', r':'),
    ('NUMBER', r'((\d+(\.\d*)?)|(\.\d+))'),
    ('IDENT', r'[a-zA-Z]+[a-zA-Z0-9_]*')

]

def lex(stringToLex):
    lexedList = []
    currentIndex = 0

    myRegex = '|'.join('(?P<%s>%s)' % pair for pair in tokenLexeme)
    matchedToken = re.compile(myRegex).match

    current = matchedToken(stringToLex)
    while current is not None:
        typ = current.lastgroup
        if typ != 'SKIP':
            val = current.group(typ)
            if typ == 'IDENT':
                found = False
                for pair in keywords:
                    if pair[1] == val:
                        lexedList.append((pair[0]))
                        found = True
                        break
                if found==False:
                    lexedList.append((typ + ":" + val))
            elif typ == 'NUMBER':
                lexedList.append((typ + ":" + str(val)))
            else:
                lexedList.append((typ))
        currentIndex = current.end()
        current = matchedToken(stringToLex, currentIndex)
    if currentIndex != len(stringToLex):
        raise Exception('Unexpected char %c' %(stringToLex[currentIndex]))

    return lexedList

if __name__ == '__main__':
    lexerOutput = []
    tokenLexeme.append(('SKIP', r'[\s+]|\n'))
    for part in sys.stdin.readlines():
        lexerOutput.append(lex(part))

    for lexedList in lexerOutput:
        for lexedItem in lexedList:
            sys.stdout.write(" " + str(lexedItem) + " ")

    sys.stdout.write("EOF")
