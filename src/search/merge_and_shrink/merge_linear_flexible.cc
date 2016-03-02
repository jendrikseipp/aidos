#include "merge_linear_flexible.h"

#include "factored_transition_system.h"

#include "../option_parser.h"
#include "../plugin.h"

#include "../utils/logging.h"
#include "../utils/markup.h"
#include "../utils/memory.h"
#include "../utils/system.h"

#include <cassert>
#include <iostream>

using namespace std;

namespace merge_and_shrink {
MergeLinearFlexible::MergeLinearFlexible(const Options &opts)
    : MergeStrategy(),
      components(opts.get_list<string>("components")),
      need_first_index(true) {
}

void MergeLinearFlexible::initialize(const shared_ptr<AbstractTask> task) {
    MergeStrategy::initialize(task);
    TaskProxy task_proxy(*task);
    int num_variables = task_proxy.get_variables().size();
    vector<int> variables(num_variables);
    iota(variables.begin(), variables.end(), 0);

    // TODO: compute the actual variable order from given component names

    variable_order = variables;
}

pair<int, int> MergeLinearFlexible::get_next(FactoredTransitionSystem &fts) {
    assert(initialized());
    assert(!done());

    int next_index1;
    if (need_first_index) {
        need_first_index = false;
        next_index1 = variable_order.front();
        variable_order.erase(variable_order.begin());
        cout << "First variable: " << next_index1 << endl;
    } else {
        // The most recent composite transition system is appended at the end
        int num_transition_systems = fts.get_size();
        next_index1 = num_transition_systems - 1;
    }
    int next_index2 = variable_order.front();
    variable_order.erase(variable_order.begin());
    cout << "Next variable: " << next_index2 << endl;
    assert(fts.is_active(next_index1));
    assert(fts.is_active(next_index2));
    --remaining_merges;
    return make_pair(next_index1, next_index2);
}

void MergeLinearFlexible::dump_strategy_specific_options() const {
    cout << "component names: " << components << endl;
}

string MergeLinearFlexible::name() const {
    return "linear flexible";
}

void MergeLinearFlexible::add_options_to_parser(OptionParser &parser) {
    vector<string> merge_strategies;
    merge_strategies.push_back("CG_GOAL_LEVEL");
    merge_strategies.push_back("CG_GOAL_RANDOM");
    merge_strategies.push_back("GOAL_CG_LEVEL");
    merge_strategies.push_back("RANDOM");
    merge_strategies.push_back("LEVEL");
    merge_strategies.push_back("REVERSE_LEVEL");
    parser.add_enum_option("variable_order", merge_strategies,
                           "the order in which atomic transition systems are merged",
                           "CG_GOAL_LEVEL");
}

static shared_ptr<MergeStrategy>_parse(OptionParser &parser) {
    parser.document_synopsis(
        "Several linear merge strategies to be combined flexibly.",
        "See Hoffmann et al ECAI 2014.");
    parser.add_list_option<string>(
        "components",
        "specify a list of component linear strategies used in the given order");
    Options opts = parser.parse();
    if (parser.dry_run())
        return nullptr;
    else
        return make_shared<MergeLinearFlexible>(opts);
}

static PluginShared<MergeStrategy> _plugin("merge_linear_flexible", _parse);
}
