#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        '3unsat_incumbent',
        ['--random-seed', ' 15659276',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.05132193143996114, num_collections=4, num_episodes=56, pdb_max_size=29), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[state_equation_constraints()], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_deadpdbs_simple, h_operatorcounting], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.3969771769844538))']),
    IssueConfig(
        'unsolvable_parking_incumbent',
        ['--random-seed', ' 6705316',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_hm=hm(cache_estimates=false, cost_type=one, m=2)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_hm, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.9884274253756492))']),
    IssueConfig(
        'unsolvable_no_mystery_incumbent',
        ['--random-seed', ' 5330197',
        '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
        '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=4824335, max_time=1638.16802355, patterns=systematic(only_interesting_patterns=false, pattern_max_size=3))',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_deadpdbs], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsolvable_cavediving_strips_incumbent',
        ['--random-seed', ' 11590901',
        '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=48379), cost_type=one, cache_estimates=false)',
         '--search', 'unsolvable_search(heuristics=[h_pdb], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.3439343933696375))']),
    IssueConfig(
        'rcp_tpp_m05_incumbent',
        ['--random-seed', ' 13861905',
        '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=734, use_general_costs=true, cost_type=one, max_time=200.167626959, pick=max_refined, cache_estimates=false)',
        '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=47828, max_time=172.073924751, patterns=genetic(disjoint=true, mutation_probability=0.5445622235458125, num_collections=2, num_episodes=250, pdb_max_size=33079))',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[lmcut_constraints(), state_equation_constraints()], cost_type=zero)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_cegar, h_deadpdbs, h_operatorcounting, h_unsolvable_all_states_potential], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_nomystery_m05_incumbent',
        ['--random-seed', ' 13293539',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_merge_and_shrink=merge_and_shrink(cache_estimates=false, label_reduction=exact(before_shrinking=true, system_order=regular, method=two_transition_systems, before_merging=false), cost_type=one, merge_strategy=merge_dfp(atomic_before_product=false, atomic_ts_order=regular, product_ts_order=new_to_old, randomized_order=false), shrink_strategy=shrink_bisimulation(threshold=746, max_states_before_merge=163793, max_states=992727, greedy=false, at_limit=return))',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[pho_constraints(patterns=systematic(only_interesting_patterns=false, pattern_max_size=1))], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_hmax, h_merge_and_shrink, h_operatorcounting], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_rovers_m09_incumbent',
        ['--random-seed', ' 9297943',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=38), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_hm=hm(cache_estimates=false, cost_type=one, m=3)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple, h_hm], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsat_mystery_incumbent',
        ['--random-seed', ' 10157681',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=2), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple, h_hmax, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.6670355678770702))']),
    IssueConfig(
        'unsolvable_sokoban_incumbent',
        ['--random-seed', ' 13441541',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind], cost_type=one, pruning=null())']),
    IssueConfig(
        'unsat_tiles_incumbent',
        ['--random-seed', ' 5328689',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.5606464868362103, num_collections=3, num_episodes=96, pdb_max_size=4), cost_type=one, cache_estimates=false)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs_simple], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_nomystery_m09_incumbent',
        ['--random-seed', ' 7960304',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.8956334014147692, num_collections=2, num_episodes=168, pdb_max_size=41), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_merge_and_shrink=merge_and_shrink(cache_estimates=false, label_reduction=exact(before_shrinking=false, system_order=random, method=all_transition_systems_with_fixpoint, before_merging=true), cost_type=one, shrink_strategy=shrink_random(threshold=311, max_states_before_merge=130846, max_states=466048), merge_strategy=merge_linear(variable_order=reverse_level))',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=infinity), state_equation_constraints()], cost_type=zero)',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=994), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_deadpdbs_simple, h_merge_and_shrink, h_operatorcounting, h_pdb, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.2846779479099395))']),
    IssueConfig(
        'unsat_pegsol_strips_incumbent',
        ['--random-seed', ' 6985924',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=62168016, max_time=187.095736772, patterns=genetic(disjoint=true, mutation_probability=0.13930739086837762, num_collections=23, num_episodes=2, pdb_max_size=1))',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_rovers_m05_incumbent',
        ['--random-seed', ' 10363085',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=one)',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=220510, use_general_costs=true, cost_type=one, max_time=114.424402986, pick=max_hadd, cache_estimates=false)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=false, mutation_probability=8.878739393457791E-4, num_collections=3, num_episodes=1, pdb_max_size=455), cost_type=one, cache_estimates=false)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=4), lmcut_constraints(), pho_constraints(patterns=genetic(disjoint=false, mutation_probability=8.878739393457791E-4, num_collections=3, num_episodes=1, pdb_max_size=455)), state_equation_constraints()], cost_type=one)',
         '--search', 'unsolvable_search(heuristics=[h_blind, h_cegar, h_deadpdbs_simple, h_operatorcounting], cost_type=one, pruning=null())']),
    IssueConfig(
        'rcp_tpp_m09_incumbent',
        ['--random-seed', ' 2537508',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=10000000, max_time=90.05, patterns=ordered_systematic(pattern_max_size=1000000000))',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search(heuristics=[h_deadpdbs, h_operatorcounting], cost_type=one, pruning=null())']),
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
