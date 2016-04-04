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
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos-1", "--search-memory-limit", "7G", "--overall-time-limit", "5m"]),
    IssueConfig(
        'aidos-2',
        [],
        build_options=["aidos_ipc"],
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos-2", "--search-memory-limit", "7G", "--overall-time-limit", "5m"]),
]
revisions = ["unsolvable-portfolio-order"]

def get_domain_dir():
    path = os.path.abspath(common_setup.get_repo_base())
    path = os.path.dirname(path)
    return os.path.join(path, "unsolvable-pddl-tasks")

cores = 2
exp = IssueExperiment(
    revisions=revisions,
    configs=configs,
    suite=suites.suite_optimal_with_ipc11(),
    test_suite=[],
    email="florian.pommerening@unibas.ch",
    extra_environment_options='#$ -pe smp %d' % cores,
)

def add_unsolvable(run):
    if run.get("error") == "incomplete-search-found-no-plan":
        run["unsolvable"] = 1
    return run

exp.add_absolute_report_step(
    filter=add_unsolvable,
    attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp()
