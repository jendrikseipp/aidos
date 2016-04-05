# -*- coding: utf-8 -*-

OPTIMAL = True

CONFIGS = [
    (1, [
        "--heuristic",
        "h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=2)], cost_type=zero)",
        "--search",
        "unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))"]),
    (4, [
        "--search",
        "unsolvable_search([deadpdbs(max_time=1)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))"]),
    (420, [
        "--heuristic",
        "h_seq=operatorcounting([state_equation_constraints(), lmcut_constraints()])",
        "--heuristic",
        "h_cegar=cegar(subtasks=[original()], pick=max_hadd, max_time=relative time 75, f_bound=compute)",
        "--search",
        "astar(f_bound=compute, eval=max([h_cegar, h_seq]), pruning=stubborn_sets_ec(min_pruning_ratio=0.50))"]),
    (1275, [
        "--search",
        "unsolvable_search([deadpdbs(max_time=relative time 50)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))"]),
    (100, [
        "--heuristic",
        "h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=infinity)], cost_type=zero)",
        "--search",
        "unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))"]),
]

assert sum(t for t, _ in CONFIGS) == 1800
