# Aidos

Aidos is a classical planner aimed at detecting unsolvable planning tasks.

## Team

* Jendrik Seipp
* Florian Pommerening
* Silvan Sievers
* Martin Wehrle
* Chris Fawcett
* Yusra Alkhazraji

## Description

Planner abstract: https://ai.dmi.unibas.ch/papers/seipp-et-al-uipc2016.pdf

Three variants of Aidos participated in the Unsolvability IPC 2016
(https://unsolve-ipc.eng.unimelb.edu.au/). All of them proved more tasks
unsolvable than any of the other competitors.

Aidos 1 and 2 are portfolios of three components:

1. Larger and larger PDBs are computed to extract partial states
   describing reachable dead-ends in a preprocessing step, which are then
   used for pruning in a depth-first search. The search also uses stubborn
   sets for partial order reduction but switches this off unless a lot of
   successors are pruned this way.

2. An LP solver is used to find a mapping from fact conjunctions
   (features) to values (potentials) in a way where applying each operator
   can only increase the potential of a state but the goal state must have
   a lower potential than the current state. If such a solution exists,
   the current state is unsolvable. This is used for pruning a depth-first
   search. As above, the search uses stubborn sets for partial order
   reduction but here we switch it off only if almost no successors are
   pruned.

3. The largest depletable resource in the task is discovered (if no such
   resource is discovered, this component does nothing). The resource is
   projected out of the task and the operator costs in the remaining task
   are redistributed to describe how much of the resource is used by this
   operator. The remaining task is then solved by an optimal planner using
   the state equation heuristic with added landmark constraints from
   LM-cut, and a CEGAR heuristic in an A* search with stubborn sets. If
   the cost of the optimal solution exceed the resource availability, the
   task is unsolvable.

Aidos 1 distributes the 30 minutes based on our experiments, while Aidos 2
distributes the time uniformly.

Aidos 3 is also a sequential portfolio, but the components and time limits
are chosen from a larger design space automatically.

## Instructions

Aidos can be built natively, but on modern systems we recommend building it in a
Docker container. To do so, you need to obtain a license for CPLEX, download the
installer for version 12.9, and place it next to this file (it should be called
`cplex_studio129.linux-x86-64.bin`). You can then build the docker container by
running

    sudo docker build . --tag aidos

in the directory containing this file, the CPLEX installer and the source code.
To run the Aidos 1 portfolio inside Docker, run

    sudo docker run -v /home/jendrik/projects/Downward/benchmarks:/tmp/benchmarks \
        --interactive --tty aidos \
        --alias seq-unsolvable-aidos-1 \
        --overall-time-limit 30m \
        /tmp/benchmarks/gripper/{domain,prob01}.pddl

For experiments, we recommend using Singularity instead of Docker. You can
create a Singularity image from the created Docker container by running

    sudo singularity build aidos.sif docker-daemon://aidos:latest

The resulting file `aidos.sif` can be run like a binary. Note that all three
versions of Aidos are portfolios and require specifying a time limit.

    # Aidos 1 portfolio (recommended)
    ./aidos.sif --alias seq-unsolvable-aidos-1 --overall-time-limit 30m PDDL_FILE

You can also run the three main component algorithms of Aidos 1 and 2 individually:

    # Deadend Database
    ./aidos.sif PDDL_FILE --search \
        "unsolvable_search([deadpdbs(max_time=900)], pruning=stubborn_sets_ec(min_pruning_ratio=0.80))"

    # Deadend Potentials
    ./aidos.sif PDDL_FILE \
        --heuristic \
        "h_seq=operatorcounting([state_equation_constraints(), feature_constraints(max_size=2)], cost_type=zero)" \
        --search \
        "unsolvable_search([h_seq], pruning=stubborn_sets_ec(min_pruning_ratio=0.20))"

    # Resource Detection
    ./aidos.sif PDDL_FILE \
        --heuristic \
        "h_seq=operatorcounting([state_equation_constraints(), lmcut_constraints()])" \
        --heuristic \
        "h_cegar=cegar(subtasks=[original()], pick=max_hadd, max_time=1350, f_bound=compute)" \
        --search \
        "astar(f_bound=compute, eval=max([h_cegar, h_seq]), pruning=stubborn_sets_ec(min_pruning_ratio=0.50))"


Aidos is built on top of the Fast Downward planning system.

# Fast Downward

Fast Downward is a domain-independent planning system.

The following directories are not part of Fast Downward as covered by this
license:
* ./benchmarks
* ./src/VAL
* ./src/search/ext

For the rest, the following license applies:

    Copyright (C) 2003-2016 Malte Helmert
    Copyright (C) 2008-2016 Gabriele Roeger
    Copyright (C) 2012-2016 Florian Pommerening
    Copyright (C) 2010-2015 Jendrik Seipp
    Copyright (C) 2010, 2011, 2013-2015 Silvan Sievers
    Copyright (C) 2013, 2015 Salome Simon
    Copyright (C) 2014, 2015 Patrick von Reth
    Copyright (C) 2015 Manuel Heusner, Thomas Keller
    Copyright (C) 2009-2014 Erez Karpas
    Copyright (C) 2014 Robert P. Goldman
    Copyright (C) 2010-2012 Andrew Coles
    Copyright (C) 2010, 2012 Patrik Haslum
    Copyright (C) 2003-2011 Silvia Richter
    Copyright (C) 2009-2011 Emil Keyder
    Copyright (C) 2010, 2011 Moritz Gronbach, Manuela Ortlieb
    Copyright (C) 2011 Vidal Alcázar Saiz, Michael Katz, Raz Nissim
    Copyright (C) 2010 Moritz Goebelbecker
    Copyright (C) 2007-2009 Matthias Westphal
    Copyright (C) 2009 Christian Muise

    Fast Downward is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free Software
    Foundation, either version 3 of the License, or (at your option) any later
    version.

    Fast Downward is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
    PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with
    this program. If not, see <http://www.gnu.org/licenses/>.

For contact information see http://www.fast-downward.org/.
