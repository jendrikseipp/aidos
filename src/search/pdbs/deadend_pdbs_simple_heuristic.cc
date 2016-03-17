#include "deadend_pdbs_simple_heuristic.h"

#include "pattern_database.h"
#include "pattern_generator.h"

#include "../option_parser.h"
#include "../plugin.h"

#include "../utils/timer.h"

#include <iostream>
#include <limits>

using namespace std;

namespace pdbs {
static shared_ptr<PDBCollection> get_pdbs_from_options(
    const shared_ptr<AbstractTask> &task, const Options &opts) {
    shared_ptr<PatternCollectionGenerator> pattern_generator =
        opts.get<shared_ptr<PatternCollectionGenerator>>("patterns");
    utils::Timer timer;
    PatternCollectionInformation pattern_collection_info =
        pattern_generator->generate(task);
    shared_ptr<PDBCollection> pdbs = pattern_collection_info.get_pdbs();
    cout << "PDB collection construction time: " << timer << endl;
    return pdbs;
}

DeadendPDBsSimpleHeuristic::DeadendPDBsSimpleHeuristic(const Options &opts)
    : Heuristic(opts),
      pdbs(get_pdbs_from_options(task, opts)) {
}

int DeadendPDBsSimpleHeuristic::compute_heuristic(const GlobalState &global_state) {
    State state = convert_global_state(global_state);
    return compute_heuristic(state);
}

int DeadendPDBsSimpleHeuristic::compute_heuristic(const State &state) const {
    for (const shared_ptr<PatternDatabase> &pdb : *pdbs) {
        const int h = pdb->get_value(state);
        if (h == numeric_limits<int>::max()) {
            return DEAD_END;
        }
    }
    return 0;
}

static Heuristic *_parse(OptionParser &parser) {
    parser.add_option<shared_ptr<PatternCollectionGenerator>>(
        "patterns",
        "pattern generation method",
        "hillclimbing()");

    Heuristic::add_options_to_parser(parser);

    Options opts = parser.parse();
    if (parser.dry_run())
        return nullptr;

    return new DeadendPDBsSimpleHeuristic(opts);
}

static Plugin<Heuristic> _plugin("deadpdbs_simple", _parse);
}
