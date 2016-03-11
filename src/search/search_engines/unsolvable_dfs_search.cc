#include "unsolvable_dfs_search.h"

#include "search_common.h"

#include "../globals.h"
#include "../heuristic.h"
#include "../option_parser.h"
#include "../plugin.h"
#include "../pruning_method.h"
#include "../successor_generator.h"

#include <cassert>
#include <cstdlib>

using namespace std;

namespace unsolvable_search {
UnsolvableDFSSearch::UnsolvableDFSSearch(const Options &opts)
    : SearchEngine(opts),
      heuristics(opts.get_list<Heuristic *>("heuristics")),
      pruning_method(opts.get<shared_ptr<PruningMethod>>("pruning")) {
    assert(cost_type == ONE);
    for (Heuristic *heuristic : heuristics) {
        if (!heuristic->dead_ends_are_reliable()) {
            cerr << "Unsolvable search only supports safe heuristics." << endl;
            utils::exit_with(utils::ExitCode::UNSUPPORTED);
        }
    }
}

bool UnsolvableDFSSearch::is_dead_end(const GlobalState &global_state) {
    statistics.inc_evaluated_states();
    for (Heuristic *heuristic : heuristics) {
        if (heuristic->is_dead_end(global_state)) {
            return true;
        }
    }
    return false;
}

void UnsolvableDFSSearch::initialize() {
    cout << "Conducting unsolvable DFS search" << endl;
    assert(g_state_registry->size() == 0);
    /* Generate the initial state (we don't need the result,
       but the state has to be created in the registry). */
    g_state_registry->get_initial_state();
    // The initial state has id 0, so we'll start there.
    current_state_id = 0;
}

void UnsolvableDFSSearch::print_statistics() const {
    statistics.print_detailed_statistics();
    search_space.print_statistics();
    pruning_method->print_statistics();
}

SearchStatus UnsolvableDFSSearch::step() {
    if (current_state_id == static_cast<int>(g_state_registry->size())) {
        // We checked all states in the registry without finding a goal.
        return UNSOLVABLE;
    }

    GlobalState s = g_state_registry->lookup_state(StateID(current_state_id));
    /* Next time we'll look at the next state that was created in the registry.
       This results in a depth-first order. */
    current_state_id++;

    if (!is_dead_end(s)) {
        if (test_goal(s)) {
            cout << "Solution found!" << endl;
            return SOLVED;
        }

        vector<const GlobalOperator *> applicable_ops;
        g_successor_generator->generate_applicable_ops(s, applicable_ops);

        pruning_method->prune_operators(s, applicable_ops);

        for (const GlobalOperator *op : applicable_ops) {
            /* Generate the successor state (we don't need the result,
               but the state has to be created in the registry). */
            g_state_registry->get_successor_state(s, *op);
            statistics.inc_generated();
        }
    }
    return IN_PROGRESS;
}

/* TODO: merge this into SearchEngine::add_options_to_parser when all search
         engines support pruning. */
static void add_pruning_option(OptionParser &parser) {
    parser.add_option<shared_ptr<PruningMethod>>(
        "pruning",
        "Pruning methods can prune or reorder the set of applicable operators in "
        "each state and thereby influence the number and order of successor states "
        "that are considered.",
        "null()");
}

static SearchEngine *_parse(OptionParser &parser) {
    parser.document_synopsis(
        "Unsolvable depth-first search",
        "Depth-first search with full duplicate detection for showing unsolvability");

    parser.add_list_option<Heuristic *>("heuristics", "list of heuristics");

    add_pruning_option(parser);
    SearchEngine::add_options_to_parser(parser);
    Options opts = parser.parse();

    // Ignore cost_type value given on the command line.
    opts.set<int>("cost_type", static_cast<int>(ONE));

    if (opts.get<int>("bound") < numeric_limits<int>::max()) {
        cerr << "Unsolvable DFS doesn't support g-bound." << endl;
        utils::exit_with(utils::ExitCode::UNSUPPORTED);
    }

    opts.verify_list_non_empty<Heuristic *>("heuristics");

    if (parser.dry_run()) {
        return nullptr;
    }
    return new UnsolvableDFSSearch(opts);
}

static Plugin<SearchEngine> _plugin("unsolvable_dfs_search", _parse);
}
