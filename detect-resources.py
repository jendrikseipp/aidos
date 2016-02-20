#!/usr/bin/env python

from task import parse_task, write_task
from dtg import DTG
from projection import project

task = parse_task("output")


i = 0
for var_id, var in enumerate(task.variables):
    if var_id not in task.goals:
        dtg = DTG(task, var_id)
        if not dtg.is_resource:
            # DTG is no DAG
            continue
        if dtg.resource_availability <= 2:
            # boring
            continue
        print "RESOURCE", var_id, var.facts[0], dtg.resource_availability
        projected_task = project(task, dtg)
        print "  Operators reduced from %s to %s" % (len(task.operators), len(projected_task.operators))
        write_task(projected_task, "output.resource%s" % i)
        print "  Task written to 'output.resource%s'" % i
        i += 1


write_task(task, "output.copy")
