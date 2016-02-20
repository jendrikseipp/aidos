#!/usr/bin/env python

from task import parse_task, write_task
from dtg import DTG
from projection import project



def detect_resources(task):
    resources = []
    for var_id, var in enumerate(task.variables):
        if var_id not in task.goals:
            dtg = DTG(task, var_id)
            if dtg.is_resource:
                resources.append(dtg)
                print "Found resource: variable %s (%s) with availability %s" % (
                        var_id, var.facts[0], dtg.resource_availability)
    return resources



def project_out_largest_resource(input_filename, output_filename):
    task = parse_task(input_filename)
    resources = detect_resources(task)
    best = None
    for resource in resources:
        if best is None or resource.resource_availability > best.resource_availability:
            best = resource
    projected_task = project(task, best)
    print "Resource projection reduced number of operators from %s to %s" % (
            len(task.operators), len(projected_task.operators))
    write_task(projected_task, output_filename)
    print "Resource projected task written to '%s'" % output_filename
    return best.resource_availability

if __name__ == "__main__":
    limit = project_out_largest_resource("output", "output.resource")
    print "Now run a search with f-bound=%s" % limit
