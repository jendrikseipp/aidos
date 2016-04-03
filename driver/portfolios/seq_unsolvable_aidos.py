# -*- coding: utf-8 -*-

OPTIMAL = True

CONFIGS = [
    (600, ["--heuristic",
           "h_seq=operatorcounting([state_equation_constraints(), lmcut_constraints()], cost_type=zero)",
           "--heuristic",
           "h_cegar=cegar(subtasks=[original()], pick=max_hadd, max_time=300)",
           "--search",
           "astar(f_bound=compute, eval=max([h_cegar, h_seq]), pruning=stubborn_sets_ec(min_pruning_ratio=0.50))"]),
    (600, ["--search",
           "unsolvable_search([deadpdbs(max_time=300)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))"]),
    (600, ["--heuristic",
           "h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=infinity)], cost_type=zero)",
           "--search",
           "unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))"]),
     ]
