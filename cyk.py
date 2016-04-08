#!/usr/bin/python

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
        tree[0][n_word] = search_gram(_grammar, _string[n_word])

    for n_depth in range(1, len(tree)):
        for n_node in range(len(tree[n_depth])):
            for n_split in range(n_depth):
                [tree[n_depth][n_node].extend(search_gram(_grammar, t1, t2)) for t1 in tree[n_split][n_node] for t2 in tree[n_depth-n_split-1][n_node+n_split+1]]

    return tree

def search_gram(_grammar, _term1, _term2=None):
    term_nt = []
    prev_nt = {}
    for nt, rules in _grammar.iteritems():
        for rule in rules:
            if ((len(rule) == 1 and _term1 in rule and not _term2) or (len(rule) == 2 and _term1 in rule and _term2 in rule)):
                term_nt.append(nt)
                try:
                    prev_prev_nt = prev_nt[nt]

                term_nt.extend(search_gram(_grammar, nt))

    return term_nt

def build_tree(_grammar, _tree):
    pass
