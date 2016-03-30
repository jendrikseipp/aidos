#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'resources_rcp_nomystery_m05_m06_incumbent',
        ['--random-seed', '8578520',
         '--heuristic', 'h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=true, cost_type=normal, dominance_pruning=true, patterns=systematic(only_interesting_patterns=true, pattern_max_size=4))',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=stubborn_sets_ec(min_pruning_ratio=0.66261628704913), eval=max([h_all_states_potential, h_cpdbs, h_lmcut]))']),
    IssueConfig(
        'resources_rcp_nomystery_m07_incumbent',
        ['--random-seed', '12690727',
         '--heuristic', 'h_blind=blind(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_cegar=cegar(subtasks=[goals(order=hadd_down), landmarks(order=hadd_down, combine_facts=true)], max_states=416945, use_general_costs=false, cost_type=normal, max_time=64.1612700663, pick=min_hadd, cache_estimates=false)',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=false, cost_type=normal, dominance_pruning=false, patterns=systematic(only_interesting_patterns=true, pattern_max_size=3))',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=4), lmcut_constraints(), state_equation_constraints()], cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_simple(min_pruning_ratio=0.9106278996048794), eval=max([h_blind, h_cegar, h_cpdbs, h_operatorcounting]))']),
    IssueConfig(
        'resources_rcp_nomystery_m08_m09_incumbent',
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
        'resources_rcp_rovers_m05_m06_incumbent',
        ['--random-seed', '3787992',
         '--heuristic', 'h_deadpdbs=deadpdbs(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2), cost_type=normal, max_dead_ends=36389913, max_time=947.343297923, cache_estimates=false)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2), cost_type=normal, cache_estimates=false)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=2), lmcut_constraints(), pho_constraints(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2)), state_equation_constraints()], cost_type=normal)',
         '--heuristic', 'h_zopdbs=zopdbs(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2), cost_type=normal, cache_estimates=true)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=stubborn_sets_ec(min_pruning_ratio=0.2444996579070121), eval=max([h_deadpdbs, h_deadpdbs_simple, h_lmcut, h_operatorcounting, h_zopdbs]))']),
    IssueConfig(
        'resources_rcp_rovers_m07_incumbent',
        ['--random-seed', '1466751',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=91983, use_general_costs=false, cost_type=normal, max_time=911.55747802, pick=max_hadd, cache_estimates=true)',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=true, cost_type=normal, dominance_pruning=false, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=normal, max_dead_ends=51226440, max_time=1024.88413254, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=3)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=false, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_ec(min_pruning_ratio=0.6604351517386684), eval=max([h_blind, h_cegar, h_cpdbs, h_deadpdbs, h_diverse_potentials, h_lmcut]))']),
    IssueConfig(
        'resources_rcp_rovers_m08_m09_incumbent',
        ['--random-seed', '4522340',
         '--heuristic', 'h_cegar=cegar(subtasks=[original(copies=1)], max_states=114, use_general_costs=false, cost_type=normal, max_time=31.4194389849, pick=max_hadd, cache_estimates=false)',
         '--heuristic', 'h_cpdbs=cpdbs(cache_estimates=false, cost_type=normal, dominance_pruning=true, patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, pdb_max_size=1, num_collections=4, num_episodes=170))',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=true, cost_type=normal, max_dead_ends=12006, max_time=380.229024557, patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, pdb_max_size=1, num_collections=4, num_episodes=170))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, pdb_max_size=1, num_collections=4, num_episodes=170), cost_type=normal, cache_estimates=false)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[lmcut_constraints(), pho_constraints(patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, pdb_max_size=1, num_collections=4, num_episodes=170)), state_equation_constraints()], cost_type=normal)',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=250), cost_type=normal, cache_estimates=false)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=null(), eval=max([h_cegar, h_cpdbs, h_deadpdbs, h_deadpdbs_simple, h_lmcut, h_operatorcounting, h_pdb]))']),
    IssueConfig(
        'resources_rcp_tpp_m05_m06_incumbent',
        ['--random-seed', '13134690',
         '--heuristic', 'h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_cegar=cegar(subtasks=[landmarks(order=original, combine_facts=false)], max_states=161, use_general_costs=true, cost_type=normal, max_time=1.74901510861, pick=min_unwanted, cache_estimates=false)',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=true, cost_type=normal, max_dead_ends=345595, max_time=1766.28429666, patterns=genetic(disjoint=false, mutation_probability=0.1546088956131102, num_collections=1, num_episodes=1, pdb_max_size=1))',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(cache_estimates=false, cost_type=normal, patterns=genetic(disjoint=false, mutation_probability=0.1546088956131102, num_collections=1, num_episodes=1, pdb_max_size=1))',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=true, cost_type=normal, num_samples=1)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=2), state_equation_constraints()], cost_type=normal)',
         '--heuristic', 'h_sample_based_potentials=sample_based_potentials(max_potential=1e8, cache_estimates=false, cost_type=normal, num_heuristics=2, num_samples=1)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_simple(min_pruning_ratio=0.31327744487104425), eval=max([h_all_states_potential, h_cegar, h_deadpdbs, h_deadpdbs_simple, h_diverse_potentials, h_lmcut, h_operatorcounting, h_sample_based_potentials, h_unsolvable_all_states_potential]))']),
    IssueConfig(
        'resources_rcp_tpp_m07_incumbent',
        ['--random-seed', '3212469',
         '--heuristic', 'h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=normal, max_dead_ends=37075, max_time=1794.548256, patterns=genetic(disjoint=true, mutation_probability=0.6165588866117894, pdb_max_size=18209, num_collections=2, num_episodes=132))',
         '--heuristic', 'h_diverse_potentials=diverse_potentials(max_potential=1e8, cache_estimates=false, cost_type=normal, num_samples=4518)',
         '--heuristic', 'h_hm=hm(cache_estimates=true, cost_type=normal, m=1)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[lmcut_constraints(), state_equation_constraints()], cost_type=normal)',
         '--heuristic', 'h_pdb=pdb(pattern=greedy(max_states=10), cost_type=normal, cache_estimates=true)',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=true, cost_type=normal)',
         '--search', 'astar(f_bound=compute, mpd=true, pruning=stubborn_sets_ec(min_pruning_ratio=0.6645183316299098), eval=max([h_all_states_potential, h_blind, h_deadpdbs, h_diverse_potentials, h_hm, h_hmax, h_lmcut, h_operatorcounting, h_pdb, h_unsolvable_all_states_potential]))']),
    IssueConfig(
        'resources_rcp_tpp_m08_m09_incumbent',
        ['--random-seed', '11119560',
         '--heuristic', 'h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_blind=blind(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=false, mutation_probability=0.056415829877983104, pdb_max_size=78, num_collections=5, num_episodes=63), cost_type=normal, cache_estimates=true)',
         '--heuristic', 'h_hmax=hmax(cache_estimates=false, cost_type=normal)',
         '--heuristic', 'h_initial_state_potential=initial_state_potential(max_potential=1e8, cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_lmcut=lmcut(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_operatorcounting=operatorcounting(cache_estimates=false, cost_type=normal, constraint_generators=[feature_constraints(max_size=infinity), state_equation_constraints()])',
         '--heuristic', 'h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=true, cost_type=normal)',
         '--heuristic', 'h_zopdbs=zopdbs(patterns=genetic(disjoint=false, mutation_probability=0.056415829877983104, pdb_max_size=78, num_collections=5, num_episodes=63), cost_type=normal, cache_estimates=true)',
         '--search', 'astar(f_bound=compute, mpd=false, pruning=stubborn_sets_ec(min_pruning_ratio=0.5812385663973145), eval=max([h_all_states_potential, h_blind, h_deadpdbs_simple, h_hmax, h_initial_state_potential, h_lmcut, h_operatorcounting, h_unsolvable_all_states_potential, h_zopdbs]))']),
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

def add_unsolvable(run):
    if run.get("error") == "incomplete-search-found-no-plan":
        run["unsolvable"] = 1
    return run

exp.add_absolute_report_step(
    filter=add_unsolvable,
    attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
