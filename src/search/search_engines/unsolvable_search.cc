#include "unsolvable_search.h"

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
UnsolvableSearch::UnsolvableSearch(const Options &opts)
    : SearchEngine(opts),
      heuristics(opts.get_list<Heuristic *>("heuristics")),
      pruning_method(opts.get<shared_ptr<PruningMethod>>("pruning")),
      max_g(0) {
    assert(cost_type == ONE);
}

bool UnsolvableSearch::is_dead_end(const GlobalState &global_state) {
    statistics.inc_evaluated_states();
    for (Heuristic *heuristic : heuristics) {
        if (heuristic->is_dead_end(global_state)) {
            return true;
        }
    }
    return false;
}

void UnsolvableSearch::initialize() {
    cout << "Conducting unsolvable search, unit-cost bound = " << bound
         << endl;

    const GlobalState &initial_state = g_initial_state();

    if (is_dead_end(initial_state)) {
        cout << "Initial state is a dead end." << endl;
    } else {
        SearchNode node = search_space.get_node(initial_state);
        node.open_initial();
        queue.push_back(initial_state.get_id());
    }
}

void UnsolvableSearch::print_checkpoint_line(int g) const {
    cout << "[g=" << g << ", ";
    statistics.print_basic_statistics();
    cout << "]" << endl;
}

void UnsolvableSearch::print_statistics() const {
    statistics.print_detailed_statistics();
    search_space.print_statistics();
    pruning_method->print_statistics();
}

SearchStatus UnsolvableSearch::step() {
    pair<SearchNode, bool> n = fetch_next_node();
    if (!n.second) {
        return FAILED;
    }
    SearchNode node = n.first;

    const int g = node.get_g();
    if (g > max_g) {
        print_checkpoint_line(g);
        max_g = g;
    }

    GlobalState s = node.get_state();
    if (check_goal_and_set_plan(s))
        return SOLVED;

    vector<const GlobalOperator *> applicable_ops;
    g_successor_generator->generate_applicable_ops(s, applicable_ops);

    pruning_method->prune_operators(s, applicable_ops);

    for (const GlobalOperator *op : applicable_ops) {
        if (g + 1 >= bound)
            continue;

        GlobalState succ_state = g_state_registry->get_successor_state(s, *op);
        statistics.inc_generated();

        SearchNode succ_node = search_space.get_node(succ_state);

        // Previously encountered dead end. Don't re-evaluate.
        if (succ_node.is_dead_end())
            continue;

        if (succ_node.is_new()) {
            /*
              Note: we must call reach_state for each heuristic, so
              don't break out of the for loop early.
            */
            for (Heuristic *heuristic : heuristics) {
                heuristic->reach_state(s, *op, succ_state);
            }

            if (is_dead_end(succ_state)) {
                succ_node.mark_as_dead_end();
                statistics.inc_dead_ends();
                continue;
            }
            succ_node.open(node, op);

            queue.push_back(succ_state.get_id());
        }
    }
    return IN_PROGRESS;
}

pair<SearchNode, bool> UnsolvableSearch::fetch_next_node() {
    while (true) {
        if (queue.empty()) {
            cout << "Completely explored state space -- no solution!" << endl;
            // HACK! HACK! we do this because SearchNode has no default/copy constructor
            SearchNode dummy_node = search_space.get_node(g_initial_state());
            return make_pair(dummy_node, false);
        }
        StateID id = queue.front();
        queue.pop_front();
        // TODO is there a way we can avoid creating the state here and then
        //      recreate it outside of this function with node.get_state()?
        //      One way would be to store GlobalState objects inside SearchNodes
        //      instead of StateIDs
        GlobalState s = g_state_registry->lookup_state(id);
        SearchNode node = search_space.get_node(s);

        if (node.is_closed())
            continue;

        node.close();
        assert(!node.is_dead_end());
        statistics.inc_expanded();
        return make_pair(node, true);
    }
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
    parser.document_synopsis("Breadth-first search", "");

    parser.add_list_option<Heuristic *>("heuristics", "list of heuristics");

    add_pruning_option(parser);
    SearchEngine::add_options_to_parser(parser);
    Options opts = parser.parse();

    // Ignore cost_type value given on the command line.
    opts.set<int>("cost_type", static_cast<int>(ONE));

    opts.verify_list_non_empty<Heuristic *>("heuristics");

    if (parser.dry_run()) {
        return nullptr;
    }
    return new UnsolvableSearch(opts);
}

static Plugin<SearchEngine> _plugin("unsolvable_search", _parse);
}
