#! /usr/bin/env python
# -*- coding: utf-8 -*-

from downward import suites

import common_setup
from common_setup import IssueConfig, IssueExperiment

import os

configs = [
    IssueConfig(
        'blind',
        ['--search', 'unsolvable_search([blind()], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'blind_prune_080',
        ['--search', 'unsolvable_search([blind()], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
    IssueConfig(
        'blind_prune_020',
        ['--search', 'unsolvable_search([blind()], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))'],
        build_options=["release64"],
        driver_options=["--build", "release64", "--search-memory-limit", "7G", "--search-time-limit", "30m"]),
]
revisions = ["unsolvable"]

def get_domain_dir():
    return os.path.expanduser("~/projects/downward/unsolve-ipc-2016/domains/FINAL")

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
    'over-tpp:prob01.pddl',
    'over-tpp:prob02.pddl',
    'over-tpp:prob03.pddl',
    'over-tpp:prob04.pddl',
    'over-tpp:prob05.pddl',
    'over-tpp:prob06.pddl',
    'over-tpp:prob07.pddl',
    'over-tpp:prob08.pddl',
    'over-tpp:prob09.pddl',
    'over-tpp:prob10.pddl',
    'over-tpp:prob11.pddl',
    'over-tpp:prob12.pddl',
    'over-tpp:prob13.pddl',
    'over-tpp:prob14.pddl',
    'over-tpp:prob15.pddl',
    'over-tpp:prob16.pddl',
    'over-tpp:prob17.pddl',
    'over-tpp:prob18.pddl',
    'over-tpp:prob19.pddl',
    'over-tpp:prob20.pddl',
    'over-tpp:prob21.pddl',
    'over-tpp:prob22.pddl',
    'over-tpp:prob23.pddl',
    'over-tpp:prob24.pddl',
    'over-tpp:prob25.pddl',
    'over-tpp:prob26.pddl',
    'over-tpp:prob27.pddl',
    'over-tpp:prob28.pddl',
    'over-tpp:prob29.pddl',
    'over-tpp:prob30.pddl',
    'over-tpp:satprob01.pddl',
    'over-tpp:satprob02.pddl',
    'over-tpp:satprob03.pddl',
    'over-tpp:satprob04.pddl',
    'sliding-tiles:prob01.pddl',
    'sliding-tiles:prob02.pddl',
    'sliding-tiles:prob03.pddl',
    'sliding-tiles:prob04.pddl',
    'sliding-tiles:prob05.pddl',
    'sliding-tiles:prob06.pddl',
    'sliding-tiles:prob07.pddl',
    'sliding-tiles:prob08.pddl',
    'sliding-tiles:prob09.pddl',
    'sliding-tiles:prob10.pddl',
    'sliding-tiles:prob11.pddl',
    'sliding-tiles:prob12.pddl',
    'sliding-tiles:prob13.pddl',
    'sliding-tiles:prob14.pddl',
    'sliding-tiles:prob15.pddl',
    'sliding-tiles:prob16.pddl',
    'sliding-tiles:prob17.pddl',
    'sliding-tiles:prob18.pddl',
    'sliding-tiles:prob19.pddl',
    'sliding-tiles:prob20.pddl',
    'sliding-tiles:satprob01.pddl',
    'sliding-tiles:satprob02.pddl',
    'sliding-tiles:satprob03.pddl',
    'sliding-tiles:satprob04.pddl',
    'sliding-tiles:satprob05.pddl',
    'chessboard-pebbling:prob03.pddl',
    'chessboard-pebbling:prob04.pddl',
    'chessboard-pebbling:prob05.pddl',
    'chessboard-pebbling:prob06.pddl',
    'chessboard-pebbling:prob07.pddl',
    'chessboard-pebbling:prob08.pddl',
    'chessboard-pebbling:prob09.pddl',
    'chessboard-pebbling:prob10.pddl',
    'chessboard-pebbling:prob11.pddl',
    'chessboard-pebbling:prob12.pddl',
    'chessboard-pebbling:prob13.pddl',
    'chessboard-pebbling:prob14.pddl',
    'chessboard-pebbling:prob15.pddl',
    'chessboard-pebbling:prob16.pddl',
    'chessboard-pebbling:prob17.pddl',
    'chessboard-pebbling:prob18.pddl',
    'chessboard-pebbling:prob19.pddl',
    'chessboard-pebbling:prob20.pddl',
    'chessboard-pebbling:prob21.pddl',
    'chessboard-pebbling:prob22.pddl',
    'chessboard-pebbling:prob23.pddl',
    'chessboard-pebbling:prob24.pddl',
    'chessboard-pebbling:prob25.pddl',
    'document-transfer:prob01.pddl',
    'document-transfer:prob02.pddl',
    'document-transfer:prob03.pddl',
    'document-transfer:prob04.pddl',
    'document-transfer:prob05.pddl',
    'document-transfer:prob06.pddl',
    'document-transfer:prob07.pddl',
    'document-transfer:prob08.pddl',
    'document-transfer:prob09.pddl',
    'document-transfer:prob10.pddl',
    'document-transfer:prob11.pddl',
    'document-transfer:prob12.pddl',
    'document-transfer:prob13.pddl',
    'document-transfer:prob14.pddl',
    'document-transfer:prob15.pddl',
    'document-transfer:prob16.pddl',
    'document-transfer:prob17.pddl',
    'document-transfer:prob18.pddl',
    'document-transfer:prob19.pddl',
    'document-transfer:prob20.pddl',
    'document-transfer:satprob01.pddl',
    'document-transfer:satprob02.pddl',
    'document-transfer:satprob03.pddl',
    'document-transfer:satprob04.pddl',
    'document-transfer:satprob05.pddl',
    'document-transfer:unknownprob01.pddl',
    'document-transfer:unknownprob02.pddl',
    'document-transfer:unknownprob03.pddl',
    'document-transfer:unknownprob04.pddl',
    'document-transfer:unknownprob05.pddl',
    'document-transfer:unknownprob06.pddl',
    'document-transfer:unknownprob07.pddl',
    'document-transfer:unknownprob08.pddl',
    'document-transfer:unknownprob09.pddl',
    'over-rovers:prob01.pddl',
    'over-rovers:prob02.pddl',
    'over-rovers:prob03.pddl',
    'over-rovers:prob04.pddl',
    'over-rovers:prob05.pddl',
    'over-rovers:prob06.pddl',
    'over-rovers:prob07.pddl',
    'over-rovers:prob08.pddl',
    'over-rovers:prob09.pddl',
    'over-rovers:prob10.pddl',
    'over-rovers:prob11.pddl',
    'over-rovers:prob12.pddl',
    'over-rovers:prob13.pddl',
    'over-rovers:prob14.pddl',
    'over-rovers:prob15.pddl',
    'over-rovers:prob16.pddl',
    'over-rovers:prob17.pddl',
    'over-rovers:prob18.pddl',
    'over-rovers:prob19.pddl',
    'over-rovers:prob20.pddl',
    'over-rovers:satprob01.pddl',
    'over-rovers:satprob02.pddl',
    'over-rovers:satprob03.pddl',
    'over-rovers:satprob04.pddl',
    'over-rovers:satprob05.pddl',
    'over-rovers:satprob06.pddl',
    'bag-gripper:prob01.pddl',
    'bag-gripper:prob02.pddl',
    'bag-gripper:prob03.pddl',
    'bag-gripper:prob04.pddl',
    'bag-gripper:prob05.pddl',
    'bag-gripper:prob06.pddl',
    'bag-gripper:prob07.pddl',
    'bag-gripper:prob08.pddl',
    'bag-gripper:prob09.pddl',
    'bag-gripper:prob10.pddl',
    'bag-gripper:prob11.pddl',
    'bag-gripper:prob12.pddl',
    'bag-gripper:prob13.pddl',
    'bag-gripper:prob14.pddl',
    'bag-gripper:prob15.pddl',
    'bag-gripper:prob16.pddl',
    'bag-gripper:prob17.pddl',
    'bag-gripper:prob18.pddl',
    'bag-gripper:prob19.pddl',
    'bag-gripper:prob20.pddl',
    'bag-gripper:prob21.pddl',
    'bag-gripper:prob22.pddl',
    'bag-gripper:prob23.pddl',
    'bag-gripper:prob24.pddl',
    'bag-gripper:prob25.pddl',
    'bag-gripper:satprob01.pddl',
    'bag-gripper:satprob02.pddl',
    'bag-gripper:satprob03.pddl',
    'bag-gripper:satprob04.pddl',
    'bag-gripper:satprob05.pddl',
    'pegsol:prob05.pddl',
    'pegsol:prob06.pddl',
    'pegsol:prob09.pddl',
    'pegsol:prob10.pddl',
    'pegsol:prob11.pddl',
    'pegsol:prob12.pddl',
    'pegsol:prob13.pddl',
    'pegsol:prob14.pddl',
    'pegsol:prob15.pddl',
    'pegsol:prob16.pddl',
    'pegsol:prob17.pddl',
    'pegsol:prob18.pddl',
    'pegsol:prob19.pddl',
    'pegsol:prob20.pddl',
    'pegsol:prob21.pddl',
    'pegsol:prob22.pddl',
    'pegsol:prob23.pddl',
    'pegsol:prob24.pddl',
    'pegsol:prob25.pddl',
    'pegsol:prob26.pddl',
    'pegsol:prob27.pddl',
    'pegsol:prob28.pddl',
    'pegsol:prob29.pddl',
    'pegsol:prob30.pddl',
    'pegsol:satprob01.pddl',
    'pegsol:satprob02.pddl',
    'pegsol:satprob03.pddl',
    'pegsol:satprob04.pddl',
    'pegsol:satprob05.pddl',
    'over-nomystery:prob01.pddl',
    'over-nomystery:prob02.pddl',
    'over-nomystery:prob03.pddl',
    'over-nomystery:prob04.pddl',
    'over-nomystery:prob05.pddl',
    'over-nomystery:prob06.pddl',
    'over-nomystery:prob07.pddl',
    'over-nomystery:prob08.pddl',
    'over-nomystery:prob09.pddl',
    'over-nomystery:prob10.pddl',
    'over-nomystery:prob11.pddl',
    'over-nomystery:prob12.pddl',
    'over-nomystery:prob13.pddl',
    'over-nomystery:prob14.pddl',
    'over-nomystery:prob15.pddl',
    'over-nomystery:prob16.pddl',
    'over-nomystery:prob17.pddl',
    'over-nomystery:prob18.pddl',
    'over-nomystery:prob19.pddl',
    'over-nomystery:prob20.pddl',
    'over-nomystery:prob21.pddl',
    'over-nomystery:prob22.pddl',
    'over-nomystery:prob23.pddl',
    'over-nomystery:prob24.pddl',
    'over-nomystery:satprob01.pddl',
    'over-nomystery:satprob02.pddl',
    'over-nomystery:satprob03.pddl',
    'over-nomystery:satprob04.pddl',
    'over-nomystery:satprob05.pddl',
    'tetris:prob01.pddl',
    'tetris:prob02.pddl',
    'tetris:prob03.pddl',
    'tetris:prob04.pddl',
    'tetris:prob05.pddl',
    'tetris:prob06.pddl',
    'tetris:prob07.pddl',
    'tetris:prob08.pddl',
    'tetris:prob09.pddl',
    'tetris:prob10.pddl',
    'tetris:prob11.pddl',
    'tetris:prob12.pddl',
    'tetris:prob13.pddl',
    'tetris:prob14.pddl',
    'tetris:prob15.pddl',
    'tetris:prob16.pddl',
    'tetris:prob17.pddl',
    'tetris:prob18.pddl',
    'tetris:prob19.pddl',
    'tetris:prob20.pddl',
    'bottleneck:prob01.pddl',
    'bottleneck:prob02.pddl',
    'bottleneck:prob03.pddl',
    'bottleneck:prob04.pddl',
    'bottleneck:prob05.pddl',
    'bottleneck:prob06.pddl',
    'bottleneck:prob07.pddl',
    'bottleneck:prob08.pddl',
    'bottleneck:prob09.pddl',
    'bottleneck:prob10.pddl',
    'bottleneck:prob11.pddl',
    'bottleneck:prob12.pddl',
    'bottleneck:prob13.pddl',
    'bottleneck:prob14.pddl',
    'bottleneck:prob15.pddl',
    'bottleneck:prob16.pddl',
    'bottleneck:prob17.pddl',
    'bottleneck:prob18.pddl',
    'bottleneck:prob19.pddl',
    'bottleneck:prob20.pddl',
    'bottleneck:prob21.pddl',
    'bottleneck:prob22.pddl',
    'bottleneck:prob23.pddl',
    'bottleneck:prob24.pddl',
    'bottleneck:prob25.pddl',
    'pegsol-row5:prob01.pddl',
    'pegsol-row5:prob02.pddl',
    'pegsol-row5:prob03.pddl',
    'pegsol-row5:prob04.pddl',
    'pegsol-row5:prob05.pddl',
    'pegsol-row5:prob06.pddl',
    'pegsol-row5:prob07.pddl',
    'pegsol-row5:prob08.pddl',
    'pegsol-row5:prob09.pddl',
    'pegsol-row5:prob10.pddl',
    'pegsol-row5:prob11.pddl',
    'pegsol-row5:prob12.pddl',
    'pegsol-row5:prob13.pddl',
    'pegsol-row5:prob14.pddl',
    'pegsol-row5:prob15.pddl',
    'pegsol-row5:satprob01.pddl',
    'pegsol-row5:satprob02.pddl',
    'pegsol-row5:satprob03.pddl',
    'pegsol-row5:satprob04.pddl',
    'pegsol-row5:satprob05.pddl',
    'cave-diving:prob01.pddl',
    'cave-diving:prob02.pddl',
    'cave-diving:prob03.pddl',
    'cave-diving:prob04.pddl',
    'cave-diving:prob05.pddl',
    'cave-diving:prob06.pddl',
    'cave-diving:prob07.pddl',
    'cave-diving:prob08.pddl',
    'cave-diving:prob09.pddl',
    'cave-diving:prob10.pddl',
    'cave-diving:prob11.pddl',
    'cave-diving:prob12.pddl',
    'cave-diving:prob13.pddl',
    'cave-diving:prob14.pddl',
    'cave-diving:prob15.pddl',
    'cave-diving:prob16.pddl',
    'cave-diving:prob17.pddl',
    'cave-diving:prob18.pddl',
    'cave-diving:prob19.pddl',
    'cave-diving:prob20.pddl',
    'cave-diving:prob21.pddl',
    'cave-diving:prob22.pddl',
    'cave-diving:prob23.pddl',
    'cave-diving:prob24.pddl',
    'cave-diving:prob25.pddl',
    'cave-diving:satprob01.pddl',
    'cave-diving:satprob02.pddl',
    'cave-diving:satprob03.pddl',
    'cave-diving:satprob04.pddl',
    'cave-diving:satprob05.pddl',
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
    'bag-barman:prob01.pddl',
    'bag-barman:prob02.pddl',
    'bag-barman:prob03.pddl',
    'bag-barman:prob04.pddl',
    'bag-barman:prob05.pddl',
    'bag-barman:prob06.pddl',
    'bag-barman:prob07.pddl',
    'bag-barman:prob08.pddl',
    'bag-barman:prob09.pddl',
    'bag-barman:prob10.pddl',
    'bag-barman:prob11.pddl',
    'bag-barman:prob12.pddl',
    'bag-barman:prob13.pddl',
    'bag-barman:prob14.pddl',
    'bag-barman:prob15.pddl',
    'bag-barman:prob16.pddl',
    'bag-barman:prob17.pddl',
    'bag-barman:prob18.pddl',
    'bag-barman:prob19.pddl',
    'bag-barman:prob20.pddl',
    'bag-barman:satprob01.pddl',
    'bag-barman:satprob02.pddl',
    'bag-barman:satprob03.pddl',
    'bag-barman:satprob04.pddl',
    'bag-barman:satprob05.pddl',
    'bag-barman:satprob06.pddl',
    'bag-barman:satprob07.pddl',
    'bag-barman:satprob08.pddl',
    'bag-barman:satprob09.pddl',
    'bag-barman:satprob10.pddl',
    'bag-barman:satprob11.pddl',
    'bag-barman:satprob12.pddl',
    'bag-barman:satprob13.pddl',
    'bag-barman:satprob14.pddl',
    'bag-barman:satprob15.pddl',
    'bag-barman:satprob16.pddl',
    'bag-barman:satprob17.pddl',
    'bag-barman:satprob18.pddl',
    'bag-barman:satprob19.pddl',
    'bag-barman:satprob20.pddl',
    'bag-transport:prob01.pddl',
    'bag-transport:prob02.pddl',
    'bag-transport:prob03.pddl',
    'bag-transport:prob04.pddl',
    'bag-transport:prob05.pddl',
    'bag-transport:prob06.pddl',
    'bag-transport:prob07.pddl',
    'bag-transport:prob08.pddl',
    'bag-transport:prob09.pddl',
    'bag-transport:prob10.pddl',
    'bag-transport:prob11.pddl',
    'bag-transport:prob12.pddl',
    'bag-transport:prob13.pddl',
    'bag-transport:prob14.pddl',
    'bag-transport:prob15.pddl',
    'bag-transport:prob16.pddl',
    'bag-transport:prob17.pddl',
    'bag-transport:prob18.pddl',
    'bag-transport:prob19.pddl',
    'bag-transport:prob20.pddl',
    'bag-transport:prob21.pddl',
    'bag-transport:prob22.pddl',
    'bag-transport:prob23.pddl',
    'bag-transport:prob24.pddl',
    'bag-transport:prob25.pddl',
    'bag-transport:prob26.pddl',
    'bag-transport:prob27.pddl',
    'bag-transport:prob28.pddl',
    'bag-transport:prob29.pddl',
    'bag-transport:satprob01.pddl',
    'bag-transport:satprob02.pddl',
    'bag-transport:satprob03.pddl',
    'bag-transport:satprob04.pddl',
    'bag-transport:satprob05.pddl',
    'bag-transport:satprob06.pddl',
    'bag-transport:satprob07.pddl',
    'bag-transport:satprob08.pddl',
    'bag-transport:satprob09.pddl',
    'bag-transport:satprob10.pddl',
    'bag-transport:satprob11.pddl',
    'bag-transport:satprob12.pddl',
    'bag-transport:satprob13.pddl',
    'bag-transport:satprob14.pddl',
    'bag-transport:satprob15.pddl',
    'bag-transport:satprob16.pddl',
    'bag-transport:satprob17.pddl',
    'bag-transport:satprob18.pddl',
    'bag-transport:satprob19.pddl',
    'bag-transport:satprob20.pddl',
    'bag-transport:satprob21.pddl',
    'bag-transport:satprob22.pddl',
    'bag-transport:satprob23.pddl',
    'bag-transport:satprob24.pddl',
    'bag-transport:satprob25.pddl',
    'bag-transport:satprob26.pddl',
    'bag-transport:satprob27.pddl',
    'bag-transport:satprob28.pddl',
    'bag-transport:satprob29.pddl',
])

def add_unsolvable(run):
    if run.get("error") == "incomplete-search-found-no-plan":
        run["unsolvable"] = 1
    return run

exp.add_absolute_report_step(
    filter=add_unsolvable,
    attributes=exp.DEFAULT_TABLE_ATTRIBUTES + ["unsolvable"])

exp.add_absolute_report_step(
    resolution="domain",
    filter=add_unsolvable,
    attributes=["unsolvable"],
    format="tex"
)

exp()
