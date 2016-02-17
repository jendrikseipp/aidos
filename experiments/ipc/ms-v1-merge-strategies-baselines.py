#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites
from lab.reports import Attribute

import common_setup
from common_setup import IssueConfig, IssueExperiment
from relativescatter import RelativeScatterPlotReport

import os
import platform

configs = [
    IssueConfig(
        "cggl-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_linear(variable_order=cg_goal_level),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "gcgl-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_linear(variable_order=goal_cg_level),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "rl-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_linear(variable_order=reverse_level),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "l-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_linear(variable_order=level),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
]
revisions = ["1f27ca781164"]

def get_domain_dir():
    path = os.path.abspath(common_setup.get_repo_base())
    path = os.path.dirname(path)
    return os.path.join(path, "unsolvable-pddl-tasks")

exp = IssueExperiment(
    revisions=revisions,
    configs=configs,
    suite=[],
    test_suite=[],
    email="silvan.sievers@unibas.ch",
)

def is_running_on_cluster():
    node = platform.node()
    return (
        "cluster" in node or
        node.startswith("gkigrid") or
        node in ["habakuk", "turtur"])

if is_running_on_cluster():
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
else:
    exp.add_suite(get_domain_dir(), [
        "bottleneck:bottleneck-prob-4-1.pddl",
        "3unsat:sat-3-22-5-1.pddl",
    ])

exp.add_resource('unsolvable_parser', 'unsolvable-parser.py', dest='unsolvable-parser.py')
exp.add_command('unsolvable-parser', ['unsolvable_parser'])
unsolvable = Attribute('unsolvable', absolute=True, min_wins=False)
exp.add_absolute_report_step(attributes=exp.DEFAULT_TABLE_ATTRIBUTES + [unsolvable])

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
