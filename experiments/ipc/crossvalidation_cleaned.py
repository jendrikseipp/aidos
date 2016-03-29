#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

# Removed random seed
# Removed blind from configs with more than one config
# Removed cache_estimates=false
# Removed cost_type=one and pruning=null() from unsolvable_search
# Removed cost_type=one from deadpdbs_simple, hm, deadpdbs, pdb, hmax, blind
# Removed copies=1 from original (and some other parameters that had their default value)
# Removed only_interesting_patterns=false from deadpdbs, pho_constraints
# Rounded double params to two significant digits
# Smoothed int params

# Strange things:

# pho_constraints(patterns=systematic(pattern_max_size=1))
# deadpdbs_simple(patterns=systematic(pattern_max_size=38))
# genetic(..., pdb_max_size=1)
# genetic(..., pdb_max_size=4)
# genetic(..., pdb_max_size=50)
# genetic(..., mutation_probability=0.54)
# genetic(..., mutation_probability=0.56)
# genetic(..., mutation_probability=0.90)
# genetic(..., mutation_probability=0.000887)
# pdb(pattern=greedy(max_states=1000))


configs = [
    IssueConfig(
        '3unsat_incumbent',
        ['--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.051, num_collections=4, num_episodes=60, pdb_max_size=30))',
         '--heuristic', 'h_operatorcounting=operatorcounting(constraint_generators=[state_equation_constraints()], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple, h_operatorcounting], pruning=stubborn_sets_ec(min_pruning_ratio=0.4))']),
    IssueConfig(
        'unsolvable_parking_incumbent',
        ['--heuristic', 'h_hm=hm(m=2)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_hm, h_unsolvable_all_states_potential], pruning=stubborn_sets_ec(min_pruning_ratio=0.98))']),
    IssueConfig(
        'unsolvable_no_mystery_incumbent',
        ['--heuristic', 'h_deadpdbs=deadpdbs(max_dead_ends=5000000, max_time=1600, patterns=systematic(pattern_max_size=3))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs])']),
    IssueConfig(
        'unsolvable_cavediving_strips_incumbent',
        ['--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=50000))',
         '--search', 'unsolvable_search(heuristics=[h_pdb], pruning=stubborn_sets_ec(min_pruning_ratio=0.35))']),
    IssueConfig(
        'rcp_tpp_m05_incumbent',
        ['--heuristic', 'h_cegar=cegar(subtasks=[original()], max_states=750, use_general_costs=true, cost_type=one, max_time=200, pick=max_refined)',
         '--heuristic', 'h_deadpdbs=deadpdbs(max_dead_ends=50000, max_time=175, patterns=genetic(disjoint=true, mutation_probability=0.54, num_collections=2, num_episodes=250))',
         '--heuristic', 'h_operatorcounting=operatorcounting(constraint_generators=[lmcut_constraints(), state_equation_constraints()], cost_type=zero)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_cegar, h_deadpdbs, h_operatorcounting, h_unsolvable_all_states_potential])']),
    IssueConfig(
        'rcp_nomystery_m05_incumbent',
        ['--heuristic', 'h_hmax=hmax()',
         '--heuristic', 'h_merge_and_shrink=merge_and_shrink(label_reduction=exact(before_shrinking=true, system_order=regular, method=two_transition_systems, before_merging=false), cost_type=one, merge_strategy=merge_dfp(atomic_before_product=false, atomic_ts_order=regular, product_ts_order=new_to_old, randomized_order=false), shrink_strategy=shrink_bisimulation(threshold=750, max_states_before_merge=175000, max_states=1000000, greedy=false, at_limit=return))',
         '--heuristic', 'h_operatorcounting=operatorcounting(constraint_generators=[pho_constraints(patterns=systematic(pattern_max_size=1))], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_hmax, h_merge_and_shrink, h_operatorcounting])']),
    IssueConfig(
        'rcp_rovers_m09_incumbent',
        ['--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(pattern_max_size=38), cost_type=one)',
         '--heuristic', 'h_hm=hm(m=3)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple, h_hm])']),
    IssueConfig(
        'unsat_mystery_incumbent',
        ['--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(pattern_max_size=2))',
         '--heuristic', 'h_hmax=hmax()',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple, h_hmax, h_unsolvable_all_states_potential], pruning=stubborn_sets_ec(min_pruning_ratio=0.67))']),
    IssueConfig(
        'unsolvable_sokoban_incumbent',
        ['--search', 'unsolvable_search(heuristics=[blind()])']),
    IssueConfig(
        'unsat_tiles_incumbent',
        ['--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.56, num_collections=3, num_episodes=100, pdb_max_size=4))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple])']),
    IssueConfig(
        'rcp_nomystery_m09_incumbent',
        ['--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.90, num_collections=2, num_episodes=175, pdb_max_size=50))',
         '--heuristic', 'h_merge_and_shrink=merge_and_shrink(label_reduction=exact(before_shrinking=false, system_order=random, method=all_transition_systems_with_fixpoint, before_merging=true), cost_type=one, shrink_strategy=shrink_random(threshold=300, max_states_before_merge=150000, max_states=500000), merge_strategy=merge_linear(variable_order=reverse_level))',
         '--heuristic', 'h_operatorcounting=operatorcounting(constraint_generators=[feature_constraints(max_size=infinity), state_equation_constraints()], cost_type=zero)',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=1000))',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple, h_merge_and_shrink, h_operatorcounting, h_pdb, h_unsolvable_all_states_potential], pruning=stubborn_sets_ec(min_pruning_ratio=0.30))']),
    IssueConfig(
        'unsat_pegsol_strips_incumbent',
        ['--heuristic', 'h_deadpdbs=deadpdbs(max_dead_ends=65000000, max_time=190, patterns=genetic(disjoint=true, mutation_probability=0.14, num_collections=23, num_episodes=2, pdb_max_size=1))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs])']),
    IssueConfig(
        'rcp_rovers_m05_incumbent',
        ['--heuristic', 'h_cegar=cegar(subtasks=[original()], max_states=250000, use_general_costs=true, cost_type=one, max_time=125, pick=max_hadd)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(mutation_probability=0.000887, num_collections=3, num_episodes=1, pdb_max_size=500))',
         '--heuristic', 'h_operatorcounting=operatorcounting(constraint_generators=[feature_constraints(max_size=4), lmcut_constraints(), pho_constraints(patterns=genetic(mutation_probability=0.000887, num_collections=3, num_episodes=1, pdb_max_size=500)), state_equation_constraints()], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_cegar, h_deadpdbs_simple, h_operatorcounting])']),
    IssueConfig(
        'rcp_tpp_m09_incumbent',
        ['--heuristic', 'h_deadpdbs=deadpdbs(max_time=90)',
         '--heuristic', 'h_operatorcounting=operatorcounting(constraint_generators=[state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs, h_operatorcounting])']),
    IssueConfig(
        'seq',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search(heuristics=[h_seq])']),
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
