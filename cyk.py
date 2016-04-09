#!/usr/bin/python

"""
Reads grammar files.
Expects a list of non-terminals on the left separated by arrows
-> with terminal(s)/non-terminal(s) on the right. Production
rules are expected to be in chomksy normal form. Rules can be 
combined with an 'or' ('|') sign.
Returns a dictionary of grammars, with left side non-terminals
as keys and lists of right sides as values.
"""
def read_grammar(_grammar_file):
    gm = open(_grammar_file).read().split('\n')[:-1]
    grammar = {}
    for line in gm:
        terms = line.split('->')
        left = terms[0].strip()

        # separate rules with an '|'
        if len(terms[1].split('|')) > 1:
            right = [[t.strip()] for t in terms[1].split('|')]
        else:
            right = [[t.strip() for t in terms[1].split()]]

        if left in grammar:
            old_right = grammar[left]
            right += old_right
        grammar[left] = right

    return grammar

"""
CYK algorithm for CNF sentence parsing.
Receives as input a parsed grammar and a string of words.
Builds a chart of words and iterates through it in cubic time
while saving backpointers to applied rules.
Returns all possible parse trees of the given string.
"""
def search_tree(_grammar, _string):
    _string = _string.split()
    strlen = len(_string)

    # build tree data structure and backtrace data structure
    tree = [[] for _ in range(strlen)]
    back = [[] for _ in range(strlen)]
    for n in range(strlen):
        tree[strlen-1-n] = [[] for _ in range(n+1)]
        back[strlen-1-n] = [{} for _ in range(n+1)]

    # basis: fill first layer of tree
    for n_word in range(strlen):
        tree[0][n_word], back[0][n_word] = search_gram(_grammar, _string[n_word])

    print(back)

    for n_depth in range(1, len(tree)):
        for n_node in range(len(tree[n_depth])):
            for n_split in range(n_depth):
                [tree[n_depth][n_node].extend(search_gram(_grammar, t1, t2)) for t1 in tree[n_split][n_node] for t2 in tree[n_depth-n_split-1][n_node+n_split+1]]

    return tree

"""
Recursive search subroutine to find rules in grammar.
Receives the used grammar and the term(s) to search for. After
a rule (left side) is found, recursively searches for the found
non-terminal on the right side of rules.
Returns all possible matches.
"""
def search_gram(_grammar, _term1, _term2=None):
    term_nt = []
    prev_nt = {}
    for nt, rules in _grammar.iteritems():
        for rule in rules:
            if ((len(rule) == 1 and _term1 in rule and not _term2) or (len(rule) == 2 and _term1 in rule and _term2 in rule)):
                term_nt.append(nt)
                tn, pn = search_gram(_grammar, nt)
                term_nt.append(tn)
                for key, val in prev_nt:
                    if key in pn:
                        old_rule = pn[key]
                        val += old_rule
                    prev_nt[key] = val
                    if nt == key:
                        old_rule = prev_nt[nt]
                        rule += old_rule
                    prev_nt[nt] = rule

    return term_nt, prev_nt

def build_tree(_grammar, _tree):
    pass
