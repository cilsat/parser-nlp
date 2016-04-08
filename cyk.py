#!/usr/bin/python

from collections import OrderedDict
import itertools

def read_grammar(_grammar_file):
    gm = open(_grammar_file).read().split('\n')[:-1]
    grammar = {}
    for line in gm:
        terms = line.split('->')
        left = terms[0].strip()

        # rules should be a non-terminal followed by an arrow
        # catch if this is not the case
        try:
            len(terms) == 2
        except:
            print("error in input grammar file")
            raise SystemExit

        # separate rules with an '|'
        if len(terms[1].split('|')) > 1:
            right = [[t.strip()] for t in terms[1].split('|')]
        else:
            right = [[t.strip() for t in terms[1].split()]]

        try:
            old_right = grammar[left]
            right += old_right
        except:
            pass
        grammar[left] = right

    return grammar

def parse_tree(_grammar, _string):
    strlen = len(_string.split())

    try:
        strlen >= 2
    except:
        print("error: input string must be at least 2 words long")
        raise SystemExit

    back = [[[]*len(_grammar.keys())]*strlen]*strlen

    string_nt = OrderedDict()
    for word in _string.split():
        string_nt[word] = search_gram(_grammar, word)

    print(string_nt)

    for span in range(2, strlen):
        for begin in range(strlen - span):
            end = span + begin
            for split in range(begin+1, end-1):
                for nt, rules in _grammar.iteritems():
                    continue
                    
        word = _string[span]

def search_gram(_grammar, _term1, _term2=None):
    term_nt = []
    for nt, rules in _grammar.iteritems():
        for rule in rules:
            if nt not in term_nt and ((len(rule) == 1 and _term1 in rule and not _term2) or (len(rule) == 2 and _term1 in rule and _term2 in rule)):
                term_nt.append(nt)
                term_nt.extend(search_gram(_grammar, nt))

    return term_nt

