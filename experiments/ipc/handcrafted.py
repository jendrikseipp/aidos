#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'blind',
        ['--search', 'unsolvable_search([blind()])'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'deadpdbs_30',
        ['--search', 'unsolvable_search([deadpdbs(max_time=90)])'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'deadpdbs_60',
        ['--search', 'unsolvable_search([deadpdbs(max_time=60)])'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'deadpdbs_60_prune_050',
        ['--search', 'unsolvable_search([deadpdbs(max_time=60)], pruning=stubborn_sets_ec(min_pruning_ratio=0.50))'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'deadpdbs_120',
        ['--search', 'unsolvable_search([deadpdbs(max_time=120)])'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'seq',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq])'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'seq_prune_025',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.25))'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'seq_prune_050',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.50))'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'seq_prune_075',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints()], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.75))'],
        driver_options=["--search-time-limit", "10m"]),
    IssueConfig(
        'seq_features_prune_050',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=infinity)], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.50))'],
        driver_options=["--search-time-limit", "10m"]),
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

exp.add_absolute_report_step(attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
