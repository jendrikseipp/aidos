#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'seq_features_prune_020',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=infinity)], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "10m"]),
    IssueConfig(
        'deadpdbs_300_prune_080',
        ['--search', 'unsolvable_search([deadpdbs(max_time=300)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "10m"]),
    IssueConfig(
        'resources_cegar_max_hadd_pruning_050',
        ['--search', 'astar(cegar(subtasks=[original()], pick=max_hadd, max_time=300), f_bound=compute)'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "10m"]),
    IssueConfig(
        'resources_cegar_max_hadd_lmcut_seq_pruning_050',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), lmcut_constraints()], cost_type=zero)',
         '--heuristic', 'h_cegar=cegar(subtasks=[original()], pick=max_hadd, max_time=300)',
         '--search', 'astar(f_bound=compute, eval=max([h_cegar, h_seq]), pruning=stubborn_sets_ec(min_pruning_ratio=0.50))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "10m"]),
]
revisions = ["unsolvable"]

def get_domain_dir():
    path = os.path.abspath(common_setup.get_repo_base())
    path = os.path.dirname(path)
    return os.path.join(path, "unsolvable-pddl-tasks")

cores = 2
exp = IssueExperiment(
    revisions=revisions,
    configs=configs,
    suite=[],
    test_suite=[],
    email="florian.pommerening@unibas.ch",
    extra_environment_options='#$ -pe smp %d' % cores,
)

exp.add_suite(get_domain_dir(), [
    "3unsat",
    "bottleneck",
    "rcp-nomystery-m05",
    "rcp-nomystery-m06",
    "rcp-nomystery-m07",
    "rcp-nomystery-m08",
    "rcp-nomystery-m09",
    "rcp-nomystery-m10",
    "rcp-rovers-m05",
    "rcp-rovers-m06",
    "rcp-rovers-m07",
    "rcp-rovers-m08",
    "rcp-rovers-m09",
    "rcp-rovers-m10",
    "rcp-tpp-m05",
    "rcp-tpp-m06",
    "rcp-tpp-m07",
    "rcp-tpp-m08",
    "rcp-tpp-m09",
    "rcp-tpp-m10",
    "unsat-mystery",
    "unsat-nomystery",
    "unsat-pegsol-strips",
    "unsat-rovers",
    "unsat-tiles",
    "unsat-tpp",
    "unsolvable-cavediving-strips",
    "unsolvable-childsnack",
    "unsolvable-maintenance-strips",
    "unsolvable-no-mystery",
    "unsolvable-parking",
    "unsolvable-pebbling",
    "unsolvable-pegsol-invasion",
    "unsolvable-sokoban",
    "unsolvable-spanner",
    "unsolvable-tetris",
])

def add_unsolvable(run):
    if run.get("error") == "incomplete-search-found-no-plan":
        run["unsolvable"] = 1
    return run

exp.add_absolute_report_step(
    filter=add_unsolvable,
    attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
