#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'rcp_nomystery_m07',
        ['--random-seed', '6753672',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=false, cost_type=normal, dominance_pruning=false, patterns=combo(max_states=1))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=combo(max_states=1), cost_type=normal, cache_estimates=false)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=2), lmcut_constraints(), state_equation_constraints()], cost_type=normal)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=true, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=null(), eval=max([h_cpdbs, h_deadpdbs_simple, h_operatorcounting, h_unsolvable_all_states_potential]))']),
    IssueConfig(
        'rcp_nomystery_m08_m09',
        ['--random-seed', '8529744',
         '--heuristic', 'h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_cegar=cegar(subtasks=[goals(order=hadd_down), landmarks(order=original, combine_facts=true)], max_states=32342, use_general_costs=true, cost_type=normal, max_time=758.699959258, pick=max_refined, cache_estimates=false)',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=true, cost_type=normal, dominance_pruning=true, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_deadpdbs=deadpdbs(patterns=systematic(only_interesting_patterns=true, pattern_max_size=1), cost_type=normal, max_dead_ends=9113366, max_time=1048.32484119, cache_estimates=false)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=1), cost_type=normal, cache_estimates=false)',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=3)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=true, constraint_generators=[feature_constraints(max_size=infinity), lmcut_constraints(), state_equation_constraints()], cost_type=normal)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=null(), eval=max([h_all_states_potential, h_cegar, h_cpdbs, h_deadpdbs, h_deadpdbs_simple, h_diverse_potentials, h_hmax, h_operatorcounting, h_unsolvable_all_states_potential]))']),
    IssueConfig(
        'rcp_rovers_m08_m09',
        ['--random-seed', '12444338',
         '--heuristic', 'h_cegar=cegar(subtasks=[goals(order=hadd_down), landmarks(order=hadd_up, combine_facts=true), original(copies=1)], max_states=1199, use_general_costs=false, cost_type=normal, max_time=604.305232558, pick=min_unwanted, cache_estimates=false)',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=362)',
         '--heuristic', 'h_initial_state_potential=initial_state_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_sample_based_potentials=sample_based_potentials(max_potential=1e8, cache_estimates=false, cost_type=normal, num_heuristics=1680, num_samples=918)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_zopdbs=zopdbs(patterns=genetic(disjoint=false, mutation_probability=0.24424371153435742, pdb_max_size=160, num_collections=92, num_episodes=2), cost_type=normal, cache_estimates=false)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=null(), eval=max([h_cegar, h_diverse_potentials, h_initial_state_potential, h_sample_based_potentials, h_unsolvable_all_states_potential, h_zopdbs]))']),
    IssueConfig(
        'rcp_rovers_m05_m06',
        ['--random-seed', '13167049',
         '--heuristic', 'h_blind=blind(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=true, cost_type=normal, max_dead_ends=28832, max_time=1074.07153225, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=1), cost_type=normal, cache_estimates=true)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_initial_state_potential=initial_state_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=true, cost_type=normal, constraint_generators=[lmcut_constraints(), pho_constraints(patterns=systematic(only_interesting_patterns=true, pattern_max_size=1)), state_equation_constraints()])',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=3290), cost_type=normal, cache_estimates=false)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_simple(min_pruning_ratio=0.788069573101691), eval=max([h_blind, h_deadpdbs, h_deadpdbs_simple, h_hmax, h_initial_state_potential, h_lmcut, h_operatorcounting, h_pdb, h_unsolvable_all_states_potential]))']),
    IssueConfig(
        'rcp_tpp_m05_m06',
        ['--random-seed', '6673498',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=null(), eval=max([h_hmax, h_lmcut]))']),
    IssueConfig(
        'rcp_tpp_m07',
        ['--random-seed', '9596183',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=normal, max_dead_ends=1326, max_time=1082.64300144, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=1), cost_type=normal, cache_estimates=true)',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=3)',
         '--heuristic', 'h_initial_state_potential=initial_state_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, cost_type=normal, constraint_generators=[lmcut_constraints(), state_equation_constraints()])',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=544), cost_type=normal, cache_estimates=true)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_zopdbs=zopdbs(patterns=systematic(only_interesting_patterns=true, pattern_max_size=1), cost_type=normal, cache_estimates=true)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=stubborn_sets_simple(min_pruning_ratio=0.1406851010605542), eval=max([h_deadpdbs, h_deadpdbs_simple, h_diverse_potentials, h_initial_state_potential, h_lmcut, h_operatorcounting, h_pdb, h_unsolvable_all_states_potential, h_zopdbs]))']),
    IssueConfig(
        'rcp_nomystery_m05_m06',
        ['--random-seed', '4876933',
         '--heuristic', 'h_initial_state_potential=initial_state_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, cost_type=normal, constraint_generators=[pho_constraints(patterns=genetic(disjoint=true, mutation_probability=0.6926711167943063, pdb_max_size=497605, num_collections=4, num_episodes=6))])',
         '--heuristic', 'h_sample_based_potentials=sample_based_potentials(max_potential=1e8, cache_estimates=false, cost_type=normal, num_heuristics=1, num_samples=258)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=true, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_simple(min_pruning_ratio=0.20943355142564968), eval=max([h_initial_state_potential, h_lmcut, h_operatorcounting, h_sample_based_potentials, h_unsolvable_all_states_potential]))']),
    IssueConfig(
        'rcp_rovers_m07',
        ['--random-seed', '1466751',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=91983, use_general_costs=false, cost_type=normal, max_time=911.55747802, pick=max_hadd, cache_estimates=true)',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=true, cost_type=normal, dominance_pruning=false, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=normal, max_dead_ends=51226440, max_time=1024.88413254, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=3)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=false, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_ec(min_pruning_ratio=0.6604351517386684), eval=max([h_blind, h_cegar, h_cpdbs, h_deadpdbs, h_diverse_potentials, h_lmcut]))']),
    IssueConfig(
        'rcp_tpp_m08_m09',
        ['--random-seed', '5335524',
         '--heuristic', 'h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_blind=blind(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_cegar=cegar(subtasks=[landmarks(order=random, combine_facts=true)], max_states=5096, use_general_costs=true, cost_type=normal, max_time=87.8020597541, pick=max_unwanted, cache_estimates=true)',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=true, cost_type=normal, max_dead_ends=979, max_time=463.946559822, patterns=genetic(disjoint=true, mutation_probability=0.4360353603499927, pdb_max_size=786, num_collections=3, num_episodes=1))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.4360353603499927, pdb_max_size=786, num_collections=3, num_episodes=1), cost_type=normal, cache_estimates=true)',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=13)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=false, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=false, eval=max([h_all_states_potential, h_blind, h_cegar, h_deadpdbs, h_deadpdbs_simple, h_diverse_potentials, h_hmax, h_lmcut]), pruning=stubborn_sets_simple(min_pruning_ratio=0.07214424310366341))']),
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
    'rcp-nomystery-m05',
    'rcp-nomystery-m06',
    'rcp-nomystery-m07',
    'rcp-nomystery-m08',
    'rcp-nomystery-m09',
    'rcp-nomystery-m10',
    'rcp-rovers-m05',
    'rcp-rovers-m06',
    'rcp-rovers-m07',
    'rcp-rovers-m08',
    'rcp-rovers-m09',
    'rcp-rovers-m10',
    'rcp-tpp-m05',
    'rcp-tpp-m06',
    'rcp-tpp-m07',
    'rcp-tpp-m08',
    'rcp-tpp-m09',
    'rcp-tpp-m10',
])

exp.add_absolute_report_step(attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
