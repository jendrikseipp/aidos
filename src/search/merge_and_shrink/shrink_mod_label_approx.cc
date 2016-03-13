#include "shrink_mod_label_approx.h"

#include "labels.h"
#include "label_equivalence_relation.h"
#include "factored_transition_system.h"
#include "transition_system.h"

#include "../globals.h"
#include "../option_parser.h"
#include "../plugin.h"
#include "../scc.h"

#include "../utils/dynamic_bitset.h"
#include "../utils/logging.h"

#include <algorithm>
#include <cassert>
#include <deque>
#include <iostream>
#include <memory>
#include <unordered_map>

using namespace std;

namespace merge_and_shrink {
using Bitset = utils::DynamicBitset<unsigned short>;

ShrinkModLabelApprox::ShrinkModLabelApprox(const Options &opts)
    : ShrinkBisimulation(opts) {
}

ShrinkModLabelApprox::~ShrinkModLabelApprox() {
}

Bitset ShrinkModLabelApprox::compute_irrelevant_in_all_other_ts_labels(
    const FactoredTransitionSystem &fts,
    int excluded_ts_index) const {
    int num_ts = fts.get_size();
    int num_labels = fts.get_labels().get_size();
    Bitset irrelevant_labels_in_all_other_ts(num_labels);
    irrelevant_labels_in_all_other_ts.set();
    for (int ts_index = 0; ts_index < num_ts; ++ts_index) {
        if (fts.is_active(ts_index) && ts_index != excluded_ts_index) {
            Bitset irrelevant_labels(num_labels);
            const TransitionSystem &ts = fts.get_ts(ts_index);
            for (const GroupAndTransitions &gat : ts) {
                const vector<Transition> &transitions = gat.transitions;
                bool group_relevant = false;
                if (static_cast<int>(transitions.size()) == ts.get_size()) {
                    /*
                      A label group is irrelevant in the earlier notion if it has
                      exactly a self loop transition for every state.
                    */
                    for (size_t i = 0; i < transitions.size(); ++i) {
                        if (transitions[i].target != transitions[i].src) {
                            group_relevant = true;
                            break;
                        }
                    }
                } else {
                    group_relevant = true;
                }
                if (!group_relevant) {
                    const LabelGroup &label_group = gat.label_group;
                    for (int label_no : label_group) {
                        irrelevant_labels.set(label_no);
                    }
                }
            }
            irrelevant_labels_in_all_other_ts &= irrelevant_labels;
        }
    }
    return irrelevant_labels_in_all_other_ts;
}

bool ShrinkModLabelApprox::all_goal_variables_incorporated(
    const TransitionSystem &ts) const {
    // HACK!
    for (const pair<int, int> goal : g_goal) {
        int goal_var = goal.first;
        bool goal_included = false;
        for (int var : ts.get_incorporated_variables()) {
            if (var == goal_var) {
                goal_included = true;
                break;
            }
        }
        if (!goal_included) {
            return false;
        }
    }
    return true;
}

void ShrinkModLabelApprox::shrink_own_label_cycles(
    FactoredTransitionSystem &fts,
    int index,
    const Bitset &irrelevant_labels_in_all_other_ts) const {
    // Build the forward graph consisting only of transitions induced by
    // "own labels", i.e. labels irrelevant in all other transition systems.
    const TransitionSystem &ts = fts.get_ts(index);
    int num_states = ts.get_size();
    vector<vector<int>> successor_graph(num_states);
    for (const GroupAndTransitions &gat : ts) {
        const LabelGroup &label_group = gat.label_group;
        bool use_group = false;
        for (int label : label_group) {
            if (irrelevant_labels_in_all_other_ts[label]) {
                use_group = true;
                break;
            }
        }

        if (use_group) {
            const vector<Transition> &transitions = gat.transitions;
            for (const Transition &t : transitions) {
                int source = t.src;
                int target = t.target;
                successor_graph[source].push_back(target);
            }
        }
    }

    // Compute SCCs of that graph
    SCC scc(successor_graph);
    vector<vector<int>> sccs(scc.get_result());

    // Aggregate each SCC into a single state
    StateEquivalenceRelation equivalence_relation;
    equivalence_relation.reserve(sccs.size());
    for (const vector<int> &scc : sccs) {
        StateEquivalenceClass equivalence_class;
        for (int state : scc) {
            equivalence_class.push_front(state);
        }
        equivalence_relation.push_back(equivalence_class);
    }

    // Perform the shrinking
    fts.apply_abstraction(index, equivalence_relation);
}

// TODO: copied from Distances
static void breadth_first_search(
    const vector<vector<int>> &graph, deque<int> &queue,
    vector<int> &distances) {
    while (!queue.empty()) {
        int state = queue.front();
        queue.pop_front();
        for (size_t i = 0; i < graph[state].size(); ++i) {
            int successor = graph[state][i];
            if (distances[successor] > distances[state] + 1) {
                distances[successor] = distances[state] + 1;
                queue.push_back(successor);
            }
        }
    }
}

void ShrinkModLabelApprox::shrink_own_label_goal_paths(
    FactoredTransitionSystem &fts,
    int index,
    const Bitset &irrelevant_labels_in_all_other_ts) const {
    const TransitionSystem &ts = fts.get_ts(index);
    if (all_goal_variables_incorporated(ts)) {
        // First, collapse all goal states into a single one.
        int num_states = ts.get_size();
        StateEquivalenceRelation equivalence_relation;
        equivalence_relation.reserve(num_states);
        StateEquivalenceClass goal_equivalence_class;
        for (int state = 0; state < num_states; ++state) {
            if (ts.is_goal_state(state)) {
                goal_equivalence_class.push_front(state);
            } else {
                StateEquivalenceClass singleton_equivalence_class;
                singleton_equivalence_class.push_front(state);
                equivalence_relation.push_back(singleton_equivalence_class);
            }
        }
        equivalence_relation.push_back(goal_equivalence_class);
        fts.apply_abstraction(index, equivalence_relation);

        // Second, compute the backward graph of own labels, perform bfs for
        // goal reachability of all states, and aggregate all states that
        // can reach the (singleton) goal (via own labels).
        num_states = ts.get_size();
        vector<vector<int>> backward_graph(num_states);
        for (const GroupAndTransitions &gat : ts) {
            const LabelGroup &label_group = gat.label_group;
            bool use_group = false;
            for (int label : label_group) {
                if (irrelevant_labels_in_all_other_ts[label]) {
                    use_group = true;
                    break;
                }
            }

            if (use_group) {
                const vector<Transition> &transitions = gat.transitions;
                for (const Transition &t : transitions) {
                    int source = t.src;
                    int target = t.target;
                    backward_graph[target].push_back(source);
                }
            }
        }

        vector<int> goal_distances(num_states, INF);
        deque<int> queue;
        for (int state = 0; state < num_states; ++state) {
            if (ts.is_goal_state(state)) {
                goal_distances[state] = 0;
                queue.push_back(state);
            }
        }
        breadth_first_search(backward_graph, queue, goal_distances);

        equivalence_relation.clear();
        StateEquivalenceClass own_label_path_equivalence_class;
        for (int state = 0; state < num_states; ++state) {
            if (goal_distances[state] != INF) {
                own_label_path_equivalence_class.push_front(state);
            } else {
                StateEquivalenceClass singleton_equivalence_class;
                singleton_equivalence_class.push_front(state);
                equivalence_relation.push_back(singleton_equivalence_class);
            }
        }
        equivalence_relation.push_back(own_label_path_equivalence_class);
        fts.apply_abstraction(index, equivalence_relation);
    }
}

void ShrinkModLabelApprox::compute_equivalence_relation(
    FactoredTransitionSystem &fts,
    int index,
    int target,
    StateEquivalenceRelation &equivalence_relation) const {
    Bitset irrelevant_labels_in_all_other_ts =
        compute_irrelevant_in_all_other_ts_labels(fts, index);
    if (irrelevant_labels_in_all_other_ts.count() > 0) {
        // (1) own-label cycles
        shrink_own_label_cycles(fts, index, irrelevant_labels_in_all_other_ts);

        // (2) own-label goal paths
        shrink_own_label_goal_paths(fts, index, irrelevant_labels_in_all_other_ts);
    }

    // (3) bisimulation
    ShrinkBisimulation::compute_equivalence_relation(
        fts, index, target, equivalence_relation);
}

string ShrinkModLabelApprox::name() const {
    return "mod label approx";
}

void ShrinkModLabelApprox::dump_strategy_specific_options() const {
    ShrinkBisimulation::dump_strategy_specific_options();
}

static shared_ptr<ShrinkStrategy>_parse(OptionParser &parser) {
    ShrinkStrategy::add_options_to_parser(parser);

    // bisimulation options
    parser.add_option<bool>("greedy", "use greedy bisimulation", "false");
    vector<string> at_limit;
    at_limit.push_back("RETURN");
    at_limit.push_back("USE_UP");
    parser.add_enum_option(
        "at_limit", at_limit,
        "what to do when the size limit is hit", "RETURN");

    Options opts = parser.parse();

    if (parser.help_mode())
        return nullptr;

    ShrinkStrategy::handle_option_defaults(opts);

    if (parser.dry_run())
        return nullptr;
    else
        return make_shared<ShrinkModLabelApprox>(opts);
}

static PluginShared<ShrinkStrategy> _plugin("shrink_mod_label_approx", _parse);
}
