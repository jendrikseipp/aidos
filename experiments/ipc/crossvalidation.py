#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        '3unsat_incumbent',
        ['--random-seed', '13485870',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=10), state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search(heuristics=[h_hmax, h_operatorcounting], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.4567602354825518))']),
    IssueConfig(
        'rcp_nomystery_m05_incumbent',
        ['--random-seed', '10248012',
         '--heuristic', 'h_hm=hm(cache_estimates=false, cost_type=one, m=1)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=5), lmcut_constraints(), state_equation_constraints()], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_hm, h_hmax, h_operatorcounting], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_nomystery_m09_incumbent',
        ['--random-seed', '7756908',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=239, use_general_costs=false, cost_type=one, max_time=118.069098369, pick=min_refined, cache_estimates=false)',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=2223694, max_time=740.277837628, patterns=systematic(only_interesting_patterns=true, pattern_max_size=61))',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_cegar, h_deadpdbs], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_rovers_m05_incumbent',
        ['--random-seed', '8337657',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=5027, use_general_costs=true, cost_type=one, max_time=797.408130433, pick=max_hadd, cache_estimates=false)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=2), lmcut_constraints(), state_equation_constraints()], cost_type=one)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_cegar, h_hmax, h_operatorcounting, h_unsolvable_all_states_potential], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_rovers_m09_incumbent',
        ['--random-seed', '3280155',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=6072, max_time=716.548499568, patterns=ordered_systematic(pattern_max_size=7))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=ordered_systematic(pattern_max_size=7), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_merge_and_shrink=merge_and_shrink(cache_estimates=false, label_reduction=exact(before_shrinking=false, system_order=regular, method=two_transition_systems, before_merging=true), cost_type=one, shrink_strategy=shrink_fh(threshold=2, max_states_before_merge=103, shrink_h=low, shrink_f=high, max_states=394), merge_strategy=merge_linear(variable_order=reverse_level))',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=2), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_deadpdbs, h_deadpdbs_simple, h_hmax, h_merge_and_shrink, h_pdb, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_simple(min_pruning_ratio=0.2517428666541712))']),
    IssueConfig(
        'rcp_tpp_m05_incumbent',
        ['--random-seed', '1551623',
         '--heuristic', 'h_deadpdbs=deadpdbs(patterns=genetic(disjoint=false, mutation_probability=0.17038147427036285, num_collections=1, num_episodes=495, pdb_max_size=1), cost_type=one, max_dead_ends=14776533, max_time=1479.05182101, cache_estimates=false)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=infinity), pho_constraints(patterns=genetic(disjoint=false, mutation_probability=0.17038147427036285, num_collections=1, num_episodes=495, pdb_max_size=1)), state_equation_constraints()], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs, h_hmax, h_operatorcounting], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.9716249209641807))']),
    IssueConfig(
        'rcp_tpp_m09_incumbent',
        ['--random-seed', '2537508',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=10000000, max_time=90.05, patterns=ordered_systematic(pattern_max_size=1000000000))',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs, h_operatorcounting], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsat_mystery_incumbent',
        ['--random-seed', '13721267',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_hm=hm(cache_estimates=false, cost_type=one, m=2)',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=144), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_hm, h_pdb, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.3595127221437011))']),
    IssueConfig(
        'unsat_pegsol_strips_incumbent',
        ['--random-seed', '2847783',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsat_tiles_incumbent',
        ['--random-seed', '5113347',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=19, max_time=182.944769355, patterns=genetic(disjoint=false, mutation_probability=0.5185313060921733, num_collections=4, num_episodes=1, pdb_max_size=1))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsolvable_cavediving_strips_incumbent',
        ['--random-seed', '5816452',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=3, max_time=605.93544671, patterns=combo(max_states=17))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.44448343973504517))']),
    IssueConfig(
        'unsolvable_no_mystery_incumbent',
        ['--random-seed', '11612062',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=3), cost_type=one, cache_estimates=false)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsolvable_parking_incumbent',
        ['--random-seed', '13250859',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=1, use_general_costs=true, cost_type=one, max_time=730.146688792, pick=max_hadd, cache_estimates=false)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[state_equation_constraints()], cost_type=one)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_cegar, h_hmax, h_operatorcounting, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.0029587459660708193))']),
    IssueConfig(
        'unsolvable_sokoban_incumbent',
        ['--random-seed', '246877',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=480377, max_time=182.862658505, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs], cost_type=one, pruning=null())']),
]
revisions = ["unsolvable"]

def get_domain_dir():
    path = os.path.abspath(common_setup.get_repo_base())
    path = os.path.dirname(path)
    return os.path.join(path, "unsolvable-pddl-tasks")

exp = IssueExperiment(
    revisions=revisions,
    configs=configs,
    suite=[],
    test_suite=[],
    email="florian.pommerening@unibas.ch",
)

exp.add_suite(get_domain_dir(), [
    "3unsat",
    "rcp-nomystery-m05",
    "rcp-nomystery-m09",
    "rcp-rovers-m05",
    "rcp-rovers-m09",
    "rcp-tpp-m05",
    "rcp-tpp-m09",
    "unsat-mystery",
    "unsat-pegsol-strips",
    "unsat-tiles",
    "unsolvable-cavediving-strips",
    "unsolvable-no-mystery",
    "unsolvable-parking",
    "unsolvable-sokoban",
])

exp.add_absolute_report_step(attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
