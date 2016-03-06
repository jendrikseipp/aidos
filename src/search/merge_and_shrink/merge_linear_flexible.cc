#include "merge_linear_flexible.h"

#include "factored_transition_system.h"

#include "../causal_graph.h"
#include "../globals.h"
#include "../option_parser.h"
#include "../plugin.h"
#include "../scc.h"

#include "../utils/collections.h"
#include "../utils/logging.h"
#include "../utils/markup.h"
#include "../utils/memory.h"
#include "../utils/rng.h"
#include "../utils/system.h"

#include <cassert>
#include <iostream>
#include <set>

using namespace std;

namespace merge_and_shrink {
MergeLinearFlexible::MergeLinearFlexible(const Options &opts)
    : MergeStrategy(),
      components(opts.get_list<string>("components")),
      need_first_index(true) {
}

vector<int> MergeLinearFlexible::select_next_vars(
    string current_component,
    vector<int> &variable_indices) {
    if (variable_indices.empty()) {
        variable_indices.resize(remaining_variables.size());
        iota(variable_indices.begin(), variable_indices.end(), 0);
    }
//    cout << "given variable indices: " << variable_indices << endl;
    vector<int> result;
    if (current_component == "goal") {
        for (size_t i = 0; i < variable_indices.size(); ++i) {
            int var = remaining_variables[i];
            if (is_goal_variable[var]) {
                result.push_back(i);
            }
        }
    } else if (current_component == "cg" || current_component == "cgroot"
               || current_component == "cgleaf") {
        // Take all cg predecessors
        vector<int> cg_predecessors;
        for (size_t i = 0; i < variable_indices.size(); ++i) {
            int var = remaining_variables[i];
            if (is_causal_predecessor[var]) {
                cg_predecessors.push_back(i);
            }
        }

        if (current_component == "cgroot") {
            // Compute smallest scc index
            int smallest_scc_index = INF;
            for (int index : cg_predecessors) {
                int var = remaining_variables[index];
                if (variable_to_scc_index[var] < smallest_scc_index) {
                    smallest_scc_index = variable_to_scc_index[var];
                }
            }

            // Include all variable with smallest scc index
            for (int index : cg_predecessors) {
                int var = remaining_variables[index];
                if (variable_to_scc_index[var] == smallest_scc_index) {
                    result.push_back(index);
                }
            }
        } else if (current_component == "cgleaf") {
            // Compute largest scc index
            int largest_scc_index = -1;
            for (int index : cg_predecessors) {
                int var = remaining_variables[index];
                if (variable_to_scc_index[var] > largest_scc_index) {
                    largest_scc_index = variable_to_scc_index[var];
                }
            }

            // Include all variable with largest scc index
            for (int index : cg_predecessors) {
                int var = remaining_variables[index];
                if (variable_to_scc_index[var] == largest_scc_index) {
                    result.push_back(index);
                }
            }
        } else {
            // Include all cg predecessors
            for (int index : cg_predecessors) {
                result.push_back(index);
            }
        }
    } else if (current_component == "empty") {
        ABORT("Not implemented");
    } else if (current_component == "levelroot") {
        int smallest_var = INF;
        int best_index = -1;
        for (int index : variable_indices) {
            int var = remaining_variables[index];
            if (var < smallest_var) {
                smallest_var = var;
                best_index = index;
            }
        }
        result.push_back(best_index);
    } else if (current_component == "levelleaf") {
        int largest_var = -1;
        int best_index = -1;
        for (int index : variable_indices) {
            int var = remaining_variables[index];
            if (var > largest_var) {
                largest_var = var;
                best_index = index;
            }
        }
        result.push_back(best_index);
    }
    return result;
}

void MergeLinearFlexible::set_variable(
    TaskProxy &task_proxy, int next_variable_index) {
    assert(utils::in_bounds(next_variable_index, remaining_variables));
    int var = remaining_variables[next_variable_index];
//    cout << "choosing index " << next_variable_index << ", var: " << var << endl;
    remaining_variables.erase(remaining_variables.begin() + next_variable_index);
    variable_order.push_back(var);
    const CausalGraph &cg = task_proxy.get_causal_graph();
    const vector<int> &new_vars = cg.get_eff_to_pre(var);
    for (int new_var : new_vars) {
        is_causal_predecessor[new_var] = true;
    }
}

void MergeLinearFlexible::initialize(const shared_ptr<AbstractTask> task) {
    MergeStrategy::initialize(task);
    TaskProxy task_proxy(*task);

    int num_variables = task_proxy.get_variables().size();
    remaining_variables.resize(num_variables);
    iota(remaining_variables.begin(), remaining_variables.end(), 0);
    is_causal_predecessor.resize(num_variables, false);
    is_goal_variable.resize(num_variables, false);
    for (FactProxy goal : task_proxy.get_goals()) {
        is_goal_variable[goal.get_variable().get_id()] = true;
    }

    vector<vector<int>> cg;
    cg.reserve(num_variables);
    for (VariableProxy var : task_proxy.get_variables()) {
        const std::vector<int> &successors =
            task_proxy.get_causal_graph().get_successors(var.get_id());
        cg.push_back(successors);
    }
    SCC scc(cg);
    vector<vector<int>> result(scc.get_result());
    variable_to_scc_index.resize(num_variables);
    for (size_t i = 0; i < result.size(); ++i) {
        const vector<int> &one_scc = result[i];
        for (int var : one_scc) {
            variable_to_scc_index[var] = i;
        }
    }

    for (int i = 0; i < num_variables; ++i) {
//        cout << "Looking for next variable" << endl;
        vector<int> current_candidate_indices;
        for (string current_component : components) {
            vector<int> remaining_candidate_indices =
                select_next_vars(current_component, current_candidate_indices);
//            cout << "Component " << current_component << " found indices: ";
//            cout << remaining_candidate_indices << " corresponds to variables: ";
//            for (int index : remaining_candidate_indices) {
//                cout << remaining_variables[index] << ", ";
//            }
//            cout << endl;
            if (!remaining_candidate_indices.empty()) {
                current_candidate_indices = remaining_candidate_indices;
            }
            if (current_candidate_indices.size() == 1) {
                break;
            }
        }

        int chosen_index = -1;
        if (current_candidate_indices.size() > 1) {
//            cout << "Need random tie breaking" << endl;
            int random_index = g_rng(current_candidate_indices.size());
            chosen_index = current_candidate_indices[random_index];
        } else {
//            cout << "Only one remaining candidate" << endl;
            chosen_index = current_candidate_indices.front();
        }
        set_variable(task_proxy, chosen_index);
        assert(static_cast<int>(variable_order.size()) == i + 1);
//        cout << endl;
    }
    assert(static_cast<int>(variable_order.size()) == num_variables);
    cout << "final variable order: " << variable_order << endl;
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

static shared_ptr<MergeStrategy>_parse(OptionParser &parser) {
    parser.document_synopsis(
        "Several linear merge strategies to be combined flexibly.",
        "See Hoffmann et al ECAI 2014.");
    parser.add_list_option<string>(
        "components",
        "specify a list of component linear strategies used in the given order");
    Options opts = parser.parse();
    set<string> valid_choices;
    valid_choices.insert("goal");
    valid_choices.insert("cg");
    valid_choices.insert("cgroot");
    valid_choices.insert("cgleaf");
    valid_choices.insert("empty");
    valid_choices.insert("levelroot");
    valid_choices.insert("levelleaf");
    vector<string> components = opts.get_list<string>("components");
    set<string> chosen_components;
    for (size_t i = 0; i < components.size(); ++i) {
        string comp = components[i];
        if (!valid_choices.count(comp)) {
            cerr << "Unknown component " << comp << endl;
            utils::exit_with(utils::ExitCode::INPUT_ERROR);
        }
        if (chosen_components.count(comp)) {
            cerr << "Cannot choose twice the same component" << endl;
            utils::exit_with(utils::ExitCode::INPUT_ERROR);
        } else {
            chosen_components.insert(comp);
        }
        if ((comp == "levelroot" || comp == "levelleaf") && i != components.size() - 1) {
            cerr << "Can choose levelroot and levelleaf only as the last component" << endl;
            utils::exit_with(utils::ExitCode::INPUT_ERROR);
        }
        if (comp == "goal" && i == 0) {
            cerr << "Cannot choose goal as the first component" << endl;
            utils::exit_with(utils::ExitCode::INPUT_ERROR);
        }
        if (comp == "empty") {
            cerr << "Not implemented" << endl;
            utils::exit_with(utils::ExitCode::INPUT_ERROR);
        }
    }
    if ((chosen_components.count("cg") && chosen_components.count("cgroot")) ||
        (chosen_components.count("cg") && chosen_components.count("cgleaf")) ||
        (chosen_components.count("cgroot") && chosen_components.count("cgleaf"))) {
        cerr << "Can only choose one of cg, cgroot and cgleaf" << endl;
        utils::exit_with(utils::ExitCode::INPUT_ERROR);
    }

    if (parser.dry_run())
        return nullptr;
    else
        return make_shared<MergeLinearFlexible>(opts);
}

static PluginShared<MergeStrategy> _plugin("merge_linear_flexible", _parse);
}
