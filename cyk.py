#!/usr/bin/python
import sys

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

def make_chart(_size):
    chart = [[] for _ in range(_size)]
    for n in range(_size):
        chart[_size-1-n] = [[] for _ in range(n+1)]

    return chart

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
    tree = make_chart(strlen)
    rule = make_chart(strlen)
    back = make_chart(strlen)

    # basis: fill bottom layer of tree
    for n_word in range(strlen):
        tree[0][n_word], rule[0][n_word], back[0][n_word] = search_gram(_grammar, _string[n_word], _back1=[_string[n_word]], _back3=[0, n_word])

    for n_depth in range(1, len(tree)):
        for n_node in range(len(tree[n_depth])):
            for s1, s2 in [[[n_s, n_node], [n_depth-n_s-1, n_node+n_s+1]] for n_s in range(n_depth)]:
                for t1, t2 in [[t1, t2] for t1 in tree[s1[0]][s1[1]] for t2 in tree[s2[0]][s2[1]]]:
                    t, r, b = search_gram(_grammar, t1, t2, s1, s2, [n_depth, n_node])
                    tree[n_depth][n_node].extend(t)
                    rule[n_depth][n_node].extend(r)
                    back[n_depth][n_node].extend(b)

    return tree, rule, back

"""
Recursive search subroutine to find rules in grammar.
Receives the used grammar and the term(s) to search for. After
a rule (left side) is found, recursively searches for the found
non-terminal on the right side of rules.
Returns all possible matches.
"""
def search_gram(_grammar, _term1, _term2=None, _back1=None, _back2=None, _back3=None):
    term_nt, rule_nt, prev_nt = [], [], []
    for nt, rules in _grammar.iteritems():
        for rule in rules:
            if (len(rule)==1 and _term1==rule[0] and not _term2) or (len(rule)==2 and _term1==rule[0] and _term2==rule[1]):
                tn, rn, pn = search_gram(_grammar, nt, _back1=_back3)
                term_nt.extend([nt] + tn)
                rule_nt.extend([rule] + rn)
                if not _back2: prev_nt.extend([[_back1]] + pn)
                else: prev_nt.extend([[_back1, _back2]] + pn)

    return term_nt, rule_nt, prev_nt

"""
Recursive reverse search that prints sentence parse tree(s).
Receives grammar and all charts as input. Looks up the back-
trace chart and the corresponding rules chart. Looks for the
rule in the tree chart cell pointed to by the backtrace chart
and recursively searches for the entires in that cell.

Prints all possible parse tree(s) to stdout with the follow-
ing components:
s = always left/upper-most, signifies beginning of tree
tag(s) at *indent* level [recursive] = children of [parent]
"""
def print_tree(_grammar, _t, _r, _b):

    def reverse_gram(_depth, _node, _n, _r_d):
        prev = _b[_depth][_node][_n]
        base = _r[_depth][_node][_n]

        while len(prev) == 1:
            # recursion basis: a terminal is found
            if prev[0] == base:
                for _ in range(_r_d): print('  '),
                print('"' + base[0] + '"')
                return

            _n -= 1
            prev = _b[_depth][_node][_n]
            base = _r[_depth][_node][_n]

        for n_t, t in enumerate(prev):
            for _ in range(_r_d): print('  '),
            p = base[n_t]
            print(p)
            idx = [i for i, j in enumerate(_t[t[0]][t[1]]) if j == p]
            reverse_gram(t[0], t[1], idx[0], _r_d+1)
            # after a duplicate is used, remove from charts
            if len(idx) > 1:
                _t[t[0]][t[1]].pop(i)
                _r[t[0]][t[1]].pop(i)
                _b[t[0]][t[1]].pop(i)

    no_match = True
    for n, t in enumerate(_t[-1][0]):
        if t == 's':
            print('s')
            depth, node = len(_t)-1, 0
            reverse_gram(depth, node, n, 1)
            no_match = False

    if no_match:
        print('no parsed sentences')

"""
Convenience function that combines some other functions.
Receives path to a grammar file and a string for evaluation.
Prints parse tree to stdout and returns grammar, rules found
(left side), rules used (right side), and backpointers.
"""
def main(_grammar_file='flight.gram', _string='book a flight from Houston to TWA'):
    print('grammar :')
    g = read_grammar(_grammar_file)
    for key, val in g.iteritems():
        print(key + ':'),
        for v in val:
            print(v),
        print('')

    print('')
    print('string : ' + _string)
    print('')

    t, r, b = search_tree(g, _string)

    print_tree(g, t, r, b)

if __name__ == "__main__":
    grammar_file = sys.argv[1]
    string = sys.argv[2]
    main(grammar_file, string)
