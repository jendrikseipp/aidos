#! /usr/bin/env python

from lab.parser import Parser

parser = Parser()

def check_proved_unsolvability(content, props):
    proved_unsolvability = False
    if props['coverage'] == 0:
        for line in content.splitlines():
            if line == 'Completely explored state space -- no solution!':
                proved_unsolvability = True
                break
    props['unsolvable'] = proved_unsolvability

parser.add_function(check_proved_unsolvability)

parser.parse()
