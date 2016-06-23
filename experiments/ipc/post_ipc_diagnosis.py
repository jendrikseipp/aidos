#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment
import cactus

import os

configs = [
    IssueConfig(
        'aidos-1',
        ["--translate-options", "--hacky-workaround-for-nasty-facts"],
        build_options=["release64"],
        driver_options=["--build", "release64", "--alias=seq-unsolvable-aidos-1", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'aidos-2',
        ["--translate-options", "--hacky-workaround-for-nasty-facts"],
        build_options=["release64"],
        driver_options=["--build", "release64", "--alias=seq-unsolvable-aidos-2", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'aidos-3',
        ["--translate-options", "--hacky-workaround-for-nasty-facts"],
        build_options=["release64"],
        driver_options=["--build", "release64", "--alias=seq-unsolvable-aidos-3", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'seq_features_prune_020',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=2)], cost_type=zero)',
         '--search', 'unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))',
         '--translate-options', '--hacky-workaround-for-nasty-facts'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'deadpdbs_1_prune_080',
        ['--search', 'unsolvable_search([deadpdbs(max_time=1)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))',
         '--translate-options', '--hacky-workaround-for-nasty-facts'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'deadpdbs_300_prune_080',
        ['--search', 'unsolvable_search([deadpdbs(max_time=300)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))',
         '--translate-options', '--hacky-workaround-for-nasty-facts'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'resources_cegar_max_hadd_lmcut_seq_pruning_050',
        ['--heuristic', 'h_seq=operatorcounting([state_equation_constraints(), lmcut_constraints()])',
         '--heuristic', 'h_cegar=cegar(subtasks=[original()], pick=max_hadd, max_time=300)',
         '--search', 'astar(f_bound=compute, eval=max([h_cegar, h_seq]), pruning=stubborn_sets_ec(min_pruning_ratio=0.50))',
         '--translate-options', '--hacky-workaround-for-nasty-facts'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'blind',
        ['--search', 'unsolvable_search([blind()], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))',
         '--translate-options', '--hacky-workaround-for-nasty-facts'],
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
    'diagnosis:prob01.pddl',
    'diagnosis:prob02.pddl',
    'diagnosis:prob03.pddl',
    'diagnosis:prob04.pddl',
    'diagnosis:prob05.pddl',
    'diagnosis:prob06.pddl',
    'diagnosis:prob07.pddl',
    'diagnosis:prob08.pddl',
    'diagnosis:prob09.pddl',
    'diagnosis:prob10.pddl',
    'diagnosis:prob11.pddl',
    'diagnosis:prob12.pddl',
    'diagnosis:prob13.pddl',
    'diagnosis:prob14.pddl',
    'diagnosis:prob15.pddl',
    'diagnosis:prob16.pddl',
    'diagnosis:prob17.pddl',
    'diagnosis:prob18.pddl',
    'diagnosis:prob19.pddl',
    'diagnosis:prob20.pddl',
    'diagnosis:unknownprob01.pddl',
    'diagnosis:unknownprob02.pddl',
    'diagnosis:unknownprob03.pddl',
    'diagnosis:satprob04.pddl',
    'diagnosis:satprob05.pddl',
    'diagnosis:satprob06.pddl',
    'diagnosis:satprob11.pddl',
    'diagnosis:satprob12.pddl',
    'diagnosis:satprob13.pddl',
    'diagnosis:satprob14.pddl',
    'diagnosis:satprob121.pddl',
    'diagnosis:satprob122.pddl',
])

def add_unsolvable(run):
    if run.get("error") == "incomplete-search-found-no-plan":
        run["unsolvable"] = 1
    return run

exp.add_absolute_report_step(
    filter=add_unsolvable,
    attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

for attribute in ["memory", "total_time"]:
    exp.add_report(
        cactus.CactusPlotReport(
            attributes=[attribute],
            xscale="linear",
            filter_unsolvable=1,
            filter=add_unsolvable,
        ),
        outfile="{}-{}.png".format(exp.name, attribute)
    )
exp()
