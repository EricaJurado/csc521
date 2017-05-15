# csc521

Python Implementation of Quirk
    Implementation of Quirk programming language for CSC 521.

    lexer.py: Reads Quirk code and creates token:lexeme/tokens sequence from it.
    parser.py: Takes sequence of tokens produced by lexer and creates a parse
        tree based on Quirk grammar.
    interpreter.py: Takes parse tree from parser and executes program.

    In short, the lexer takes in Quirk language via standard input and sends a
    stream of tokens to standard output to be used by the parser. This stream of
    tokens is used by the parser to generate a serializable version of the parse
    tree. The interpreter then deserializes this and executes the code and outputs
    a line whenever there is a print statement. All 3 parts are built off the
    partials given in class.

    To use the lexer, parser, and interpreter, they must pass information to
    their relevant neighbors. To do so with the included examples you must enter
    in the following command:

    python lexer.py < exampleA.py | python parser.py | python interpreter.py > output


    The lexer uses a list of keywords and a list of Quirk token lexeme pairs to
    create the pairs based on the input. It uses regex functionality to join
    all pairs in these lists to see if there are tokens within the string that is
    passed in. If there is, it adds this to the string to be outputted. In addition
    to the keywords and token lexeme pairs, a skip token is added within main
    which is used to ignore spaces and newlines. It is added in main rather than
    in the initial lists to make it clear that it's *not* part of Quirk grammar -
    it's used to properly lex input.

    The parser takes the full set of tokens (including an EOF) and stores them in
    an array. Each of the grammar functions has a parameter, token_index which is
    the position in the token list where the grammar should start parsing from.
    Ultimately the grammar functions will return a boolean that indicates if a
    subtree that corresponds to the grammar is found or not, the index of the list
    of tokens where the function left off, and finally the parse tree. This parse
    tree is what will be passed to the interpreter to use.

    The interpreter takes this parse tree and uses a scope stack to navigate this
    tree structure. By doing this it is able to execute the code. 
