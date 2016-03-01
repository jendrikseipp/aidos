#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

from common_setup import IssueConfig, IssueExperiment, get_domain_dir, is_running_on_cluster
from relativescatter import RelativeScatterPlotReport
import extra_attributes

import os
import platform

configs = [
    IssueConfig(
        "sccs-reg-nto-pba-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=new_to_old,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-nto-pba-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=new_to_old,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-nto-pba-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=new_to_old,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-otn-pba-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=old_to_new,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-otn-pba-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=old_to_new,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-otn-pba-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=old_to_new,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-nto-abp-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=new_to_old,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-nto-abp-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=new_to_old,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-nto-abp-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=new_to_old,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-otn-abp-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=old_to_new,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-otn-abp-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=old_to_new,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-otn-abp-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=old_to_new,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-allrnd-b50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_bisimulation(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(,randomized_order=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-nto-pba-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=new_to_old,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-nto-pba-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=new_to_old,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-nto-pba-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=new_to_old,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-otn-pba-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=old_to_new,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-otn-pba-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=old_to_new,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-otn-pba-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=old_to_new,atomic_before_product=false),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-nto-abp-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=new_to_old,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-nto-abp-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=new_to_old,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-nto-abp-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=new_to_old,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-reg-otn-abp-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=regular,product_ts_order=old_to_new,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-inv-otn-abp-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=inverse,product_ts_order=old_to_new,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-rnd-otn-abp-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(atomic_ts_order=random,product_ts_order=old_to_new,atomic_before_product=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
    IssueConfig(
        "sccs-allrnd-modlabelapproxb50k",
        ["--search", "astar(merge_and_shrink(shrink_strategy=shrink_mod_label_approx(max_states=50000,threshold=1,greedy=false),merge_strategy=merge_sccs(,randomized_order=true),label_reduction=exact(before_shrinking=true,before_merging=false),only_dead_end_detection=false))"]),
]
revisions = ["573c8e4a055d"]

exp = IssueExperiment(
    revisions=revisions,
    configs=configs,
    suite=[],
    test_suite=[],
    email="silvan.sievers@unibas.ch",
)

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
exp.add_resource('ms_parser', 'ms-parser.py', dest='ms-parser.py')
exp.add_command('ms-parser', ['ms_parser'])
extra_attributes = extra_attributes.get()
exp.add_absolute_report_step(attributes=exp.DEFAULT_TABLE_ATTRIBUTES + extra_attributes)

#for attribute in ["raw_memory", "total_time"]:
    #for config in configs:
        #exp.add_report(
            #RelativeScatterPlotReport(
                #attributes=[attribute],
                #filter_config=["{}-{}".format(rev, conf) for rev in revisions for conf in ["blind", config.nick]],
                #get_category=lambda run1, run2: run1.get("domain"),
            #),
            #outfile="{}-{}-{}.png".format(exp.name, attribute, config.nick)
        #)

exp()
