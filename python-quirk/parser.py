# Takes a sequence of tokens and produces a parse tree according to the
# language grammar. It is expected that this parser will be a recursive
# descent parser.

import sys
import pprint

pp = pprint.PrettyPrinter(indent=1, depth=20)
tokens = []


# begin utilities
def is_ident(tok):
    """
    Determine if the token is of type IDENT.

    tok - a token
    returns True if IDENT is in the token or False if not.
    """
    return -1 < tok.find("IDENT")


def is_number(tok):
    """
    Determine if the token is of type NUMBER.

    tok - a token
    returns True if NUMBER is in the token or False if not.
    """
    return -1 < tok.find("NUMBER")
# end utilities


def Program(tok_index):
    """
    Return (full program) tree if possible.

    <Program> ->
        <Statement> <Program>
        | <Statement>
    """
    # <Statement> <Program>
    (result, ret_index, ret_subtree) = Statement(tok_index)
    if result:
        subtree = ["Program0", ret_subtree]
        (result, ret_index, ret_subtree) = Program(ret_index)
        if result:
            subtree.append(ret_subtree)
            return [True, ret_index, subtree]

    # <Statement>
    (result, ret_index, ret_subtree) = Statement(tok_index)
    if result:
        return [True, ret_index, ["Program1", ret_subtree]]
    return [False, tok_index, []]


def Statement(tok_index):
    """
    Return statement subtree, if possible.

    <Statement> ->
        <FunctionDeclaration>
        | <Assignment>
        | <Print>
    """
    # <FunctionDeclaration>
    (result, ret_index, ret_subtree) = FunctionDeclaration(tok_index)
    if result:
        return [True, ret_index, ["Statement0", ret_subtree]]

    # <Assignment>
    (result, ret_index, ret_subtree) = Assignment(tok_index)
    if result:
        return [True, ret_index, ["Statement1", ret_subtree]]

    # <Print>
    (result, ret_index, ret_subtree) = Print(tok_index)
    if result:
        return [True, ret_index, ["Statement2", ret_subtree]]

    return [False, tok_index, []]


def FunctionDeclaration(tok_index):
    """
    Return FunctionDeclaration subtree, if possible.

    <FunctionDeclaration> ->
        FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
    """
    # FUNCTION <Name> LPAREN <FunctionParams> LBRACE <FunctionBody> RBRACE
    if "FUNCTION" == tokens[tok_index]:
        subtree = ["FunctionDeclaration0", tokens[tok_index]]
        (result, ret_index, ret_subtree) = Name(tok_index + 1)
        if result:
            subtree.append(ret_subtree)
            if "LPAREN" == tokens[ret_index]:
                subtree.append(tokens[ret_index])
                (result, ret_index, ret_subtree) = FunctionParams(ret_index +
                                                                  1)
                if result:
                    subtree.append(ret_subtree)
                    if "LBRACE" == tokens[ret_index]:
                        subtree.append(tokens[ret_index])
                        (result, ret_index,
                            ret_subtree) = FunctionBody(ret_index + 1)
                        if result:
                            subtree.append(ret_subtree)
                            if "RBRACE" == tokens[ret_index]:
                                subtree.append(tokens[ret_index])
                                return [True, ret_index + 1, subtree]
    return [False, tok_index, []]


def FunctionParams(tok_index):
    """
    Return FunctionParams subtree, if possible.

    <FunctionParams> ->
        <NameList> RPAREN
        | RPAREN
    """
    # <NameList> RPAREN
    (result, ret_index, ret_subtree) = NameList(tok_index)
    if result:
        subtree = ["FunctionParams0", ret_subtree]
        if "RPAREN" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            return [True, ret_index + 1, subtree]

    # RPAREN
    if "RPAREN" == tokens[tok_index]:
        subtree = ["FunctionParams1", tokens[tok_index]]
        return [True, tok_index + 1, []]
    return [False, tok_index, []]


def FunctionBody(tok_index):
    """
    Return FunctionBody subtree, if possible.

    <FunctionBody> ->
        <Program> <Return>
        | <Return>
    """
    # <Program> <Return>
    (result, ret_index, ret_subtree) = Program(tok_index)
    if result:
        subtree = ["FunctionBody0", ret_subtree]
        (result, ret_index, ret_subtree) = Return(ret_index)
        if result:
            subtree.append(ret_subtree)
            return [True, ret_index, subtree]

    # <Return>
    (result, ret_index, ret_subtree) = Return(tok_index)
    if result:
        return [True, ret_index, ["FunctionBody1", ret_subtree]]
    return [False, tok_index, []]


def Return(tok_index):
    """
    Return Return subtree, if possible.

    <Return> ->
        RETURN <ParameterList>
    """
    # RETURN <ParameterList>
    if "RETURN" == tokens[tok_index]:
        subtree = ["Return0", tokens[tok_index]]
        (result, ret_index, ret_subtree) = ParameterList(tok_index + 1)
        if result:
            subtree.append(ret_subtree)
            return [True, ret_index, subtree]
    return [False, tok_index, []]


def Assignment(tok_index):
    """
    Return Assignment subtree, if possible.

    <Assignment> ->
        <SingleAssignment>
        | <MultipleAssignment>
    """
    # <SingleAssignment>
    (result, ret_index, ret_subtree) = SingleAssignment(tok_index)
    if result:
        return [True, ret_index, ["Assignment0", ret_subtree]]

    # <MultipleAssignment>
    (result, ret_index, ret_subtree) = MultipleAssignment(tok_index)
    if result:
        return [True, ret_index, ["Assignment1", ret_subtree]]
    return [False, tok_index, []]


def SingleAssignment(tok_index):
    """
    Return SingleAssignment subtree, if possible.

    <SingleAssignment> ->
        VAR <Name> ASSIGN <Expression>
    """
    # VAR <Name> ASSIGN <Expression>
    if "VAR" == tokens[tok_index]:
        subtree = ["SingleAssignment0", tokens[tok_index]]
        (result, ret_index, ret_subtree) = Name(tok_index + 1)
        if result:
            subtree.append(ret_subtree)
            if "ASSIGN" == tokens[ret_index]:
                subtree.append(tokens[ret_index])
                (result, ret_index, ret_subtree) = Expression(ret_index + 1)
                if result:
                    subtree.append(ret_subtree)
                    return [True, ret_index, subtree]
    return [False, tok_index, []]


def MultipleAssignment(tok_index):
    """
    Return MultipleAssignment subtree, if possible.

    <MultipleAssignment> ->
        VAR <NameList> ASSIGN <FunctionCall>
    """
    # VAR <NameList> ASSIGN <FunctionCall>
    if "VAR" == tokens[tok_index]:
        subtree = ["MultipleAssignment0", tokens[tok_index]]
        (result, ret_index, ret_subtree) = NameList(tok_index + 1)
        if result:
            subtree.append(ret_subtree)
            if "ASSIGN" == tokens[ret_index]:
                subtree.append(tokens[ret_index])
                (result, ret_index, ret_subtree) = FunctionCall(ret_index + 1)
                if result:
                    subtree.append(ret_subtree)
                    return [True, ret_index, subtree]
    return [False, tok_index, []]


def Print(tok_index):
    """
    Return Print subtree, if possible.

    <Print> ->
        PRINT <Expression>
    """
    # PRINT <Expression>
    if "PRINT" == tokens[tok_index]:
        subtree = ["Print0", tokens[tok_index]]
        (result, ret_index, ret_subtree) = Expression(tok_index + 1)
        if result:
            subtree.append(ret_subtree)
            return [True, ret_index, subtree]
    return [False, tok_index, []]


def NameList(tok_index):
    """
    Return NameList subtree, if possible.

    <NameList> ->
        <Name> COMMA <NameList>
        | <Name>
    """
    # <Name> COMMA <NameList>
    (result, ret_index, ret_subtree) = Name(tok_index)
    if result:
        subtree = ["NameList0", ret_subtree]
        if "COMMA" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = NameList(ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <Name>
    (result, ret_index, ret_subtree) = Name(tok_index)
    if result:
        return [True, ret_index, ["NameList1", ret_subtree]]
    return [False, tok_index, []]


def ParameterList(tok_index):
    """
    Return ParameterList subtree, if possible.

    <ParameterList> ->
        <Parameter> COMMA <ParameterList>
        | <Parameter>
    """
    # <Parameter> COMMA <ParameterList>
    (result, ret_index, ret_subtree) = Parameter(tok_index)
    if result:
        subtree = ["ParameterList0", ret_subtree]
        if "COMMA" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = ParameterList(ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <Parameter>
    (result, ret_index, ret_subtree) = Parameter(tok_index)
    if result:
        return [True, ret_index, ["ParameterList1", ret_subtree]]
    return [False, tok_index, []]


def Parameter(tok_index):
    """
    Return Parameter subtree, if possible.

    <Parameter> ->
        <Expression>
        | <Name>
    """
    # <Expression>
    (result, ret_index, ret_subtree) = Expression(tok_index)
    if result:
        return [True, ret_index, ["Parameter0", ret_subtree]]

    # <Name>
    (result, ret_index, ret_subtree) = Name(tok_index)
    if result:
        return [True, ret_index, ["Parameter1", ret_subtree]]
    return [False, tok_index, []]


def Expression(tok_index):
    """
    Return Expression subtree, if possible.

    <Expression> ->
        <Term> ADD <Expression>
        | <Term> SUB <Expression>
        | <Term>
    """
    # <Term> ADD <Expression>
    (result, ret_index, ret_subtree) = Term(tok_index)
    if result:
        subtree = ["Expression0", ret_subtree]
        if "ADD" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = Expression(
                ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <Term> SUB <Expression>
    (result, ret_index, ret_subtree) = Term(tok_index)
    if result:
        subtree = ["Expression1", ret_subtree]
        if "SUB" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = Expression(
                ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]
    # <Term>
    (result, ret_index, ret_subtree) = Term(tok_index)
    if result:
        return [True, ret_index, ["Expression2", ret_subtree]]
    return [False, tok_index, []]


def Term(tok_index):
    """
    Return Term subtree, if possible.

    <Term> ->
        <Factor> MULT <Term>
        | <Factor> DIV <Term>
        | <Factor>
    """
    # <Factor> MULT <Term>
    (result, ret_index, ret_subtree) = Factor(tok_index)
    if result:
        subtree = ["Term0", ret_subtree]
        if "MULT" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = Term(ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <Factor> DIV <Term>
    (result, ret_index, ret_subtree) = Factor(tok_index)
    if result:
        subtree = ["Term1", ret_subtree]
        if "DIV" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = Term(ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <Factor>
    (result, ret_index, ret_subtree) = Factor(tok_index)
    if result:
        return [True, ret_index, ["Term2", ret_subtree]]
    return [False, tok_index, []]


def Factor(tok_index):
    """
    Return Factor subtree, if possible.

    <Factor> ->
        <SubExpression>
        | <SubExpression> EXP <Factor>
        | <FunctionCall>
        | <Value> EXP <Factor>
        | <Value>
    """
    # <SubExpression> EXP <Factor>
    (result, ret_index, ret_subtree) = SubExpression(tok_index)
    if result:
        subtree = ["Factor0", ret_subtree]
        if "EXP" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = Factor(ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <SubExpression>
    (result, ret_index, ret_subtree) = SubExpression(tok_index)
    if result:
        subtree = ["Factor1", ret_subtree]
        return [True, ret_index, subtree]

    # <FunctionCall>
    (result, ret_index, ret_subtree) = FunctionCall(tok_index)
    if result:
        return [True, ret_index, ["Factor2", ret_subtree]]

    # <Value> EXP <Factor>
    (result, ret_index, ret_subtree) = Value(tok_index)
    if result:
        subtree = ["Factor3", ret_subtree]
        if "EXP" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = Factor(ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                return [True, ret_index, subtree]

    # <Value>
    (result, ret_index, ret_subtree) = Value(tok_index)
    if result:
        return [True, ret_index, ["Factor4", ret_subtree]]
    return [False, tok_index, []]


def FunctionCall(tok_index):
    """
    Return FunctionCall subtree, if possible.

    <FunctionCall> ->
        <Name> LPAREN <FunctionCallParams> COLON <Number>
        | <Name> LPAREN <FunctionCallParams>
    """
    # <Name> LPAREN <FunctionCallParams> COLON <Number>
    (result, ret_index, ret_subtree) = Name(tok_index)
    if result:
        subtree = ["FunctionCall0", ret_subtree]
        if "LPAREN" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            (result, ret_index, ret_subtree) = FunctionCallParams(
                ret_index + 1)
            if result:
                subtree.append(ret_subtree)
                if "COLON" == tokens[ret_index]:
                    subtree.append(tokens[ret_index])
                    (result, ret_index, ret_subtree) = Number(
                        ret_index + 1)
                    if result:
                        subtree.append(ret_subtree)
                        return [True, ret_index, subtree]

    # <Name> LPAREN <FunctionCallParams>
        (result, ret_index, ret_subtree) = Name(tok_index)
        if result:
            subtree = ["FunctionCall1", ret_subtree]
            if "LPAREN" == tokens[ret_index]:
                subtree.append(tokens[ret_index])
                (result, ret_index, ret_subtree) = FunctionCallParams(
                    ret_index + 1)
                if result:
                    subtree.append(ret_subtree)
                    return [True, ret_index, subtree]
    return [False, tok_index, []]


def FunctionCallParams(tok_index):
    """
    Return FunctionCallParams subtree, if possible.

    <FunctionCallParams> ->
        <ParameterList> RPAREN
        | RPAREN
    """
    # <ParameterList> RPAREN
    (result, ret_index, ret_subtree) = ParameterList(tok_index)
    if result:
        subtree = ["FunctionCallParams0", ret_subtree]
        if "RPAREN" == tokens[ret_index]:
            subtree.append(tokens[ret_index])
            return [True, ret_index + 1, subtree]

    # RPAREN
    if "RPAREN" == tokens[tok_index]:
        subtree = ["FunctionCallParams1", tokens[tok_index]]
        return [True, tok_index + 1, subtree]
    return [False, tok_index, []]


def SubExpression(tok_index):
    """
    Return SubExpression subtree, if possible.

    <SubExpression> ->
        LPAREN <Expression> RPAREN
    """
    # LPAREN <Expression> RPAREN
    if "LPAREN" == tokens[tok_index]:
        subtree = ["SubExpression0", tokens[tok_index]]
        (result, ret_index, ret_subtree) = Expression(tok_index + 1)
        if result:
            subtree.append(ret_subtree)
            if "RPAREN" == tokens[ret_index]:
                subtree.append(tokens[ret_index])
                return [True, ret_index + 1, subtree]
    return [False, tok_index, []]


def Value(tok_index):
    """
    Return Value subtree, if possible.

    <Value> ->
        <Name>
        | <Number>
    """
    # <name>
    (result, ret_index, ret_subtree) = Name(tok_index)
    if result:
        return [True, ret_index, ["Value0", ret_subtree]]

    # <number>
    (result, ret_index, ret_subtree) = Number(tok_index)
    if result:
        return [True, ret_index, ["Value1", ret_subtree]]
    return [False, tok_index, []]


def Name(tok_index):
    """
    Return Name subtree, if possible.

    <Name> ->
        IDENT
        | SUB IDENT
        | ADD IDENT
    """
    subtree = []
    # IDENT
    if is_ident(tokens[tok_index]):
        subtree = ["Name0", tokens[tok_index]]
        return [True, tok_index + 1, subtree]

    # SUB IDENT
    if "SUB" == tokens[tok_index]:
        if is_ident(tokens[tok_index + 1]):
            subtree = ["Name1", tokens[tok_index], tokens[tok_index + 1]]
            return [True, tok_index + 2, subtree]

    # ADD IDENT
    if "ADD" == tokens[tok_index]:
        if is_ident(tokens[tok_index + 1]):
            subtree = ["Name2", tokens[tok_index], tokens[tok_index + 1]]
            return [True, tok_index + 2, subtree]
    return [False, tok_index, subtree]


def Number(tok_index):
    """
    Return Number subtree, if possible.

    <Number> ->
        NUMBER
        | SUB NUMBER
        | ADD NUMBER
    """
    subtree = []
    # NUMBER
    if is_number(tokens[tok_index]):
        subtree = ["Number0", tokens[tok_index]]
        return [True, tok_index + 1, subtree]

    # SUB NUMBER
    if "SUB" == tokens[tok_index]:
        if is_number(tokens[tok_index + 1]):
            subtree = ["Number1", tokens[tok_index], tokens[tok_index + 1]]
            return [True, tok_index + 2, subtree]

    # ADD NUMBER
    if "ADD" == tokens[tok_index]:
        if is_number(tokens[tok_index + 1]):
            subtree = ["Number2", tokens[tok_index], tokens[tok_index + 1]]
            return [True, tok_index + 2, subtree]
    return [False, tok_index, subtree]


if __name__ == '__main__':
    for line in sys.stdin.readlines():
        for token in line.split():
            tokens.append(token)
    # print(tokens)
    pp.pprint(Program(0))
