#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'aidos-1',
        [],
        build_options=["aidos_ipc"],
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos-1", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'aidos-2',
        [],
        build_options=["aidos_ipc"],
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos-2", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'aidos-3',
        [],
        build_options=["aidos_ipc"],
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos-3", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'seq_features_prune_020',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=2)], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'deadpdbs_1_prune_080',
        ['--search', 'unsolvable_search([deadpdbs(max_time=1)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'deadpdbs_300_prune_080',
        ['--search', 'unsolvable_search([deadpdbs(max_time=300)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'resources_cegar_max_hadd_lmcut_seq_pruning_050',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), lmcut_constraints()])',
         '--heuristic', 'h_cegar=cegar(subtasks=[original()], pick=max_hadd, max_time=300)',
         '--search', 'astar(f_bound=compute, eval=max([h_cegar, h_seq]), pruning=stubborn_sets_ec(min_pruning_ratio=0.50))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
]
revisions = ["unsolvable"]

def get_domain_dir():
    return "/infai/pommeren/projects/downward/unsolve-ipc-2016/domains/FINAL"

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
    "bag-barman",
    "bag-gripper",
    "bag-transport",
    "bottleneck",
    "cave-diving",
    "chessboard-pebbling",
    "diagnosis",
    "document-transfer",
    "over-nomystery",
    "over-rovers",
    "over-tpp",
    "pegsol",
    "pegsol-row5",
    "sliding-tiles",
    "tetris",
])

def add_unsolvable(run):
    if run.get("error") == "incomplete-search-found-no-plan":
        run["unsolvable"] = 1
    return run

exp.add_absolute_report_step(
    filter=add_unsolvable,
    attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
