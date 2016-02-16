#include "shrink_mod_label.h"

#include "labels.h"
#include "label_equivalence_relation.h"
#include "factored_transition_system.h"
#include "transition_system.h"

#include "../option_parser.h"
#include "../plugin.h"

#include "../utils/dynamic_bitset.h"

#include <algorithm>
#include <cassert>
#include <iostream>
#include <memory>
#include <unordered_map>

using namespace std;

namespace merge_and_shrink {
using Bitset = Utils::DynamicBitset<unsigned short>;

ShrinkModLabel::ShrinkModLabel(const Options &opts)
    : ShrinkBisimulation(opts) {
}

ShrinkModLabel::~ShrinkModLabel() {
}

Bitset compute_irrelevant_in_all_other_ts_labels(
    const FactoredTransitionSystem &fts,
    int excluded_ts_index) {
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

void ShrinkModLabel::compute_equivalence_relation(
    FactoredTransitionSystem &fts,
    int index,
    int target,
    StateEquivalenceRelation &equivalence_relation) const {
    // (1) label inheritance
    Bitset irrelevant_labels_in_all_other_ts =
        compute_irrelevant_in_all_other_ts_labels(fts, index);
    fts.get_ts(index).label_inheritance(irrelevant_labels_in_all_other_ts);
    fts.recompute_distances(index);

    // (2) goal-label pruning
    fts.get_ts(index).prune_transitions_of_goal_states();

    // (3) bisimulation
    ShrinkBisimulation::compute_equivalence_relation(
        fts, index, target, equivalence_relation);
}

string ShrinkModLabel::name() const {
    return "mod label";
}

void ShrinkModLabel::dump_strategy_specific_options() const {
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
        return make_shared<ShrinkModLabel>(opts);
}

static PluginShared<ShrinkStrategy> _plugin("shrink_mod_label", _parse);
}
