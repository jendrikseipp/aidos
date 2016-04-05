# -*- coding: utf-8 -*-

OPTIMAL = True

CONFIGS = [
    #Execute rcp_tpp_m05_config_3 for 8,
    (8, [
        "--heuristic",
        "h_blind=blind(cache_estimates=false, cost_type=one)",
        "--heuristic",
        "h_cegar=cegar(subtasks=[original(copies=1)], max_states=10, use_general_costs=true, cost_type=one, max_time=relative time 50, pick=min_unwanted, cache_estimates=false)",
        "--heuristic",
        "h_deadpdbs=deadpdbs(patterns=combo(max_states=1), cost_type=one, max_dead_ends=290355, max_time=relative time 99, cache_estimates=false)",
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(patterns=combo(max_states=1), cost_type=one, cache_estimates=false)",
        "--heuristic",
        "h_hm=hm(cache_estimates=false, cost_type=one, m=1)",
        "--heuristic",
        "h_hmax=hmax(cache_estimates=false, cost_type=one)",
        "--heuristic",
        "h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=3), lmcut_constraints(), pho_constraints(patterns=combo(max_states=1)), state_equation_constraints()], cost_type=one)",
        "--heuristic",
        "h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)",
        "--search",
        "unsolvable_search(heuristics=[h_blind, h_cegar, h_deadpdbs, h_deadpdbs_simple, h_hm, h_hmax, h_operatorcounting, h_unsolvable_all_states_potential], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.9887183754249436))"]),

    #Execute resources_rcp_rovers_m05_m06_config_4 for 6,
    (6, [
        "--heuristic",
        "h_deadpdbs=deadpdbs(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2), cost_type=normal, max_dead_ends=36389913, max_time=relative time 52, cache_estimates=false)",
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2), cost_type=normal, cache_estimates=false)",
        "--heuristic",
        "h_lmcut=lmcut(cache_estimates=true, cost_type=normal)",
        "--heuristic",
        "h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=2), lmcut_constraints(), pho_constraints(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2)), state_equation_constraints()], cost_type=normal)",
        "--heuristic",
        "h_zopdbs=zopdbs(patterns=genetic(disjoint=false, mutation_probability=0.2794745683909153, pdb_max_size=1, num_collections=40, num_episodes=2), cost_type=normal, cache_estimates=true)",
        "--search",
        "astar(f_bound=compute, mpd=false, pruning=stubborn_sets_ec(min_pruning_ratio=0.2444996579070121), eval=max([h_deadpdbs, h_deadpdbs_simple, h_lmcut, h_operatorcounting, h_zopdbs]))"]),

    #Execute unsolvable_no_mystery_config_3 for 2,
    (2, [
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=true, pattern_max_size=3), cost_type=one, cache_estimates=false)",
        "--search",
        "unsolvable_search(heuristics=[h_deadpdbs_simple], cost_type=one, pruning=null())"]),

    #Execute unsat_mystery_config_6 for 2,
    (2, [
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(patterns=genetic(disjoint=true, mutation_probability=0.32087500872172836, num_collections=30, num_episodes=7, pdb_max_size=1908896), cost_type=one, cache_estimates=false)",
        "--heuristic",
        "h_hm=hm(cache_estimates=false, cost_type=one, m=3)",
        "--heuristic",
        "h_pdb=pdb(pattern=greedy(max_states=18052), cost_type=one, cache_estimates=false)",
        "--search",
        "unsolvable_search(heuristics=[h_deadpdbs_simple, h_hm, h_pdb], cost_type=one, pruning=null())"]),

    #Execute unsolvable_parking_config_9 for 2,
    (2, [
        "--heuristic",
        "h_blind=blind(cache_estimates=false, cost_type=one)",
        "--heuristic",
        "h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=4, max_time=relative time 84, patterns=systematic(only_interesting_patterns=false, pattern_max_size=15))",
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(patterns=systematic(only_interesting_patterns=false, pattern_max_size=15), cost_type=one, cache_estimates=false)",
        "--heuristic",
        "h_merge_and_shrink=merge_and_shrink(cache_estimates=false, label_reduction=exact(before_shrinking=true, system_order=random, method=all_transition_systems, before_merging=false), cost_type=one, shrink_strategy=shrink_bisimulation(threshold=115, max_states_before_merge=56521, max_states=228893, greedy=true, at_limit=use_up), merge_strategy=merge_dfp(atomic_before_product=false, atomic_ts_order=regular, product_ts_order=random, randomized_order=true))",
        "--search",
        "unsolvable_search(heuristics=[h_blind, h_deadpdbs, h_deadpdbs_simple, h_merge_and_shrink], cost_type=one, pruning=null())"]),

    #Execute resources_rcp_rovers_m08_m09_config_10 for 4,
    (4, [
        "--heuristic",
        "h_cegar=cegar(subtasks=[original(copies=1)], max_states=114, use_general_costs=false, cost_type=normal, max_time=relative time 1, pick=max_hadd, cache_estimates=false)",
        "--heuristic",
        "h_cpdbs=cpdbs(patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, num_collections=4, num_episodes=170, pdb_max_size=1), cost_type=normal, dominance_pruning=true, cache_estimates=false)",
        "--heuristic",
        "h_deadpdbs=deadpdbs(cache_estimates=true, cost_type=normal, max_dead_ends=12006, max_time=relative time 21, patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, num_collections=4, num_episodes=170, pdb_max_size=1))",
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(cache_estimates=false, cost_type=normal, patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, num_collections=4, num_episodes=170, pdb_max_size=1))",
        "--heuristic",
        "h_lmcut=lmcut(cache_estimates=true, cost_type=normal)",
        "--heuristic",
        "h_operatorcounting=operatorcounting(cache_estimates=false, cost_type=normal, constraint_generators=[feature_constraints(max_size=2), lmcut_constraints(), pho_constraints(patterns=genetic(disjoint=true, mutation_probability=0.7174375735405052, num_collections=4, num_episodes=170, pdb_max_size=1)), state_equation_constraints()])",
        "--heuristic",
        "h_pdb=pdb(pattern=greedy(max_states=250), cost_type=normal, cache_estimates=false)",
        "--search",
        "astar(f_bound=compute, mpd=true, pruning=null(), eval=max([h_cegar, h_cpdbs, h_deadpdbs, h_deadpdbs_simple, h_lmcut, h_operatorcounting, h_pdb]))"]),

    #Execute rcp_rovers_m05_config_7 for 7,
    (7, [
        "--heuristic",
        "h_blind=blind(cache_estimates=false, cost_type=one)",
        "--heuristic",
        "h_cegar=cegar(subtasks=[original(copies=1)], max_states=5151, use_general_costs=false, cost_type=one, max_time=relative time 44, pick=max_hadd, cache_estimates=false)",
        "--heuristic",
        "h_hmax=hmax(cache_estimates=false, cost_type=one)",
        "--heuristic",
        "h_merge_and_shrink=merge_and_shrink(cache_estimates=false, label_reduction=exact(before_shrinking=true, system_order=random, method=all_transition_systems_with_fixpoint, before_merging=false), cost_type=one, shrink_strategy=shrink_bisimulation(threshold=1, max_states_before_merge=12088, max_states=100000, greedy=false, at_limit=return), merge_strategy=merge_linear(variable_order=cg_goal_random))",
        "--heuristic",
        "h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=2), lmcut_constraints(), state_equation_constraints()], cost_type=one)",
        "--heuristic",
        "h_unsolvable_all_states_potential=unsolvable_all_states_potential(cache_estimates=false, cost_type=one)",
        "--search",
        "unsolvable_search(heuristics=[h_blind, h_cegar, h_hmax, h_merge_and_shrink, h_operatorcounting, h_unsolvable_all_states_potential], cost_type=one, pruning=null())"]),

    #Execute 3unsat_config_2 for 37,
    (37, [
        "--heuristic",
        "h_hmax=hmax(cache_estimates=false, cost_type=one)",
        "--heuristic",
        "h_operatorcounting=operatorcounting(cache_estimates=false, constraint_generators=[feature_constraints(max_size=10), state_equation_constraints()], cost_type=zero)",
        "--search",
        "unsolvable_search(heuristics=[h_hmax, h_operatorcounting], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.4567602354825518))"]),

    #Execute resources_rcp_tpp_m08_m09_config_7 for 33,
    (33, [
        "--heuristic",
        "h_all_states_potential=all_states_potential(max_potential=1e8, cache_estimates=true, cost_type=normal)",
        "--heuristic",
        "h_blind=blind(cache_estimates=false, cost_type=normal)",
        "--heuristic",
        "h_cegar=cegar(subtasks=[goals(order=hadd_down), landmarks(order=original, combine_facts=true), original(copies=1)], max_states=601, use_general_costs=false, cost_type=normal, max_time=relative time 88, pick=min_unwanted, cache_estimates=true)",
        "--heuristic",
        "h_deadpdbs_simple=deadpdbs_simple(cache_estimates=true, cost_type=normal, patterns=hillclimbing(min_improvement=2, pdb_max_size=7349527, collection_max_size=233, max_time=relative time 32, num_samples=28))",
        "--heuristic",
        "h_initial_state_potential=initial_state_potential(max_potential=1e8, cache_estimates=false, cost_type=normal)",
        "--heuristic",
        "h_operatorcounting=operatorcounting(cache_estimates=false, cost_type=normal, constraint_generators=[feature_constraints(max_size=10), lmcut_constraints(), pho_constraints(patterns=hillclimbing(min_improvement=2, pdb_max_size=7349527, collection_max_size=233, max_time=relative time 32, num_samples=28)), state_equation_constraints()])",
        "--heuristic",
        "h_pdb=pdb(pattern=greedy(max_states=6), cost_type=normal, cache_estimates=true)",
        "--heuristic",
        "h_zopdbs=zopdbs(patterns=hillclimbing(min_improvement=2, pdb_max_size=7349527, collection_max_size=233, max_time=relative time 32, num_samples=28), cost_type=normal, cache_estimates=false)",
        "--search",
        "astar(f_bound=compute, mpd=true, pruning=stubborn_sets_ec(min_pruning_ratio=0.0927145675045078), eval=max([h_all_states_potential, h_blind, h_cegar, h_deadpdbs_simple, h_initial_state_potential, h_operatorcounting, h_pdb, h_zopdbs]))"]),

    #Execute unsolvable_cavediving_strips_config_10 for 150,
    (150, [
        "--heuristic",
        "h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=6, max_time=relative time 75, patterns=systematic(only_interesting_patterns=true, pattern_max_size=1))",
        "--search",
        "unsolvable_search(heuristics=[h_deadpdbs], cost_type=one, pruning=stubborn_sets_ec(min_pruning_ratio=0.3918701752094733))"]),

    #Execute rcp_nomystery_m09_config_9 for 1549
    (1549, [
        "--heuristic",
        "h_deadpdbs=deadpdbs(cache_estimates=false, cost_type=one, max_dead_ends=63156737, max_time=relative time 4, patterns=ordered_systematic(pattern_max_size=869))",
        "--heuristic",
        "h_merge_and_shrink=merge_and_shrink(cache_estimates=false, label_reduction=exact(before_shrinking=true, system_order=random, method=all_transition_systems_with_fixpoint, before_merging=false), cost_type=one, shrink_strategy=shrink_bisimulation(threshold=23, max_states_before_merge=29143, max_states=995640, greedy=false, at_limit=return), merge_strategy=merge_dfp(atomic_before_product=false, atomic_ts_order=regular, product_ts_order=new_to_old, randomized_order=false))",
        "--search",
        "unsolvable_search(heuristics=[h_deadpdbs, h_merge_and_shrink], cost_type=one, pruning=null())"]),

]

assert sum(t for t, _ in CONFIGS) == 1800
