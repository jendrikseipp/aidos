#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'rcp_pdbs_seq',
        [],
        build_options=["aidos_ipc"],
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
    IssueConfig(
        'rcp_seq_pdbs',
        [],
        build_options=["aidos_ipc"],
        driver_options=["--build", "aidos_ipc", "--alias=seq-unsolvable-aidos-order2", "--search-memory-limit", "7G", "--overall-time-limit", "30m"]),
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
