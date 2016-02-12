#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment
from relativescatter import RelativeScatterPlotReport

import os

configs = [
    IssueConfig(
        "blind",
        ["--search", "astar(blind())"]),
    IssueConfig(
        "deadpdbs-naive",
        ["--search", "astar(deadpdbs(patterns=systematic(1000, only_interesting_patterns=false)))"]),
    IssueConfig(
        "deadpdbs-systematic",
        ["--search", "astar(deadpdbs(patterns=systematic(1000)))"]),
    IssueConfig(
        "deadpdbs-ordered-systematic",
        ["--search", "astar(deadpdbs(patterns=ordered_systematic()))"]),
]
revisions = ["8b3cc2f75507"]

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
    "unsat-mystery",
    "unsat-nomystery",
    "unsat-pegsol-strips",
    "unsat-rovers",
    "unsat-tiles",
    "unsat-tpp",
])

exp.add_comparison_table_step()

for attribute in ["memory", "total_time"]:
    for config in configs:
        exp.add_report(
            RelativeScatterPlotReport(
                attributes=[attribute],
                filter_config=["{}-{}".format(rev, conf) for rev in revisions for conf in ["blind", config.nick]],
                get_category=lambda run1, run2: run1.get("domain"),
            ),
            outfile="{}-{}-{}.png".format(exp.name, attribute, config.nick)
        )

exp()
