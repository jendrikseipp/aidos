#include "abstraction.h"

#include "abstract_state.h"
#include "utils.h"

#include "../globals.h"
#include "../task_tools.h"

#include "../utils/logging.h"
#include "../utils/memory.h"

#include <algorithm>
#include <cassert>
#include <iostream>
#include <unordered_map>

using namespace std;

namespace cegar {
struct Flaw {
    // Last concrete and abstract state reached while tracing solution.
    const State concrete_state;
    // TODO: After conversion to smart pointers, store as unique_ptr?
    AbstractState *current_abstract_state;
    // Hypothetical Cartesian set we would have liked to reach.
    const AbstractState desired_abstract_state;

    Flaw(
        State &&concrete_state,
        AbstractState *current_abstract_state,
        AbstractState &&desired_abstract_state)
        : concrete_state(move(concrete_state)),
          current_abstract_state(current_abstract_state),
          desired_abstract_state(move(desired_abstract_state)) {
    }

    vector<Split> get_possible_splits() const {
        vector<Split> splits;
        /*
          For each fact in the concrete state that is not contained in
          the current abstract state (reason: abstract and concrete
          traces diverged) or the desired abstract state (reason:
          unsatisfied precondition or goal), loop over all values of
          the corresponding variable. The values that are in both the
          current and the desired abstract state are the "wanted" ones.
        */
        for (FactProxy wanted_fact : concrete_state) {
            if (!current_abstract_state->contains(wanted_fact) ||
                !desired_abstract_state.contains(wanted_fact)) {
                VariableProxy var = wanted_fact.get_variable();
                vector<int> wanted;
                for (int value = 0; value < var.get_domain_size(); ++value) {
                    FactProxy fact = var.get_fact(value);
                    if (current_abstract_state->contains(fact) &&
                        desired_abstract_state.contains(fact)) {
                        wanted.push_back(value);
                    }
                }
                assert(!wanted.empty());
                splits.emplace_back(var.get_id(), move(wanted));
            }
        }
        assert(!splits.empty());
        return splits;
    }
};

Abstraction::Abstraction(
    const shared_ptr<AbstractTask> task,
    int max_states,
    int max_h,
    double max_time,
    bool use_general_costs,
    PickSplit pick,
    bool debug)
    : task_proxy(*task),
      max_states(max_states),
      max_h(max_h),
      abstract_search(
          get_operator_costs(task_proxy),
          states,
          use_general_costs),
      split_selector(task, pick),
      timer(max_time),
      init(nullptr),
      deviations(0),
      unmet_preconditions(0),
      unmet_goals(0),
      debug(debug) {
    assert(max_states >= 1);
    g_log << "Start building abstraction." << endl;
    cout << "Maximum number of states: " << max_states << endl;
    cout << "Maximum h value: " << max_h << endl;
    build();
    g_log << "Done building abstraction." << endl;
    cout << "Time for building abstraction: " << timer << endl;

    /* Even if we found a concrete solution, we might have refined in the
       last iteration, so we should update the h values. */
    update_h_values();

    print_statistics();
}

Abstraction::~Abstraction() {
    for (AbstractState *state : states)
        delete state;
}

bool Abstraction::is_goal(AbstractState *state) const {
    return goals.count(state) == 1;
}

void Abstraction::separate_facts_unreachable_before_goal() {
    assert(goals.size() == 1);
    assert(states.size() == 1);
    assert(task_proxy.get_goals().size() == 1);
    FactProxy goal = task_proxy.get_goals()[0];
    unordered_set<FactProxy> reachable_facts = get_relaxed_possible_before(
        task_proxy, goal);
    for (VariableProxy var : task_proxy.get_variables()) {
        if (!may_keep_refining())
            break;
        int var_id = var.get_id();
        vector<int> unreachable_values;
        for (int value = 0; value < var.get_domain_size(); ++value) {
            FactProxy fact = var.get_fact(value);
            if (reachable_facts.count(fact) == 0)
                unreachable_values.push_back(value);
        }
        if (!unreachable_values.empty())
            refine(init, var_id, unreachable_values);
    }
    goals.clear();
    goals.insert(states.begin(), states.end());
}

void Abstraction::create_trivial_abstraction() {
    init = AbstractState::get_trivial_abstract_state(
        task_proxy, refinement_hierarchy.get_root());
    goals.insert(init);
    states.insert(init);
}

bool Abstraction::may_keep_refining() const {
    /* TODO: Think about whether we really want to go to the memory limit.
       Without doing so, the algorithm would be more deterministic. */
    return utils::extra_memory_padding_is_reserved() &&
           get_num_states() < max_states &&
           init->get_h_value() < max_h &&
           !timer.is_expired();
}

void Abstraction::build() {
    create_trivial_abstraction();
    /*
      For landmark tasks we have to map all states in which the
      landmark might have been achieved to arbitrary abstract goal
      states. For the other types of subtasks our method won't find
      unreachable facts, but calling it unconditionally for subtasks
      with one goal doesn't hurt and simplifies the implementation.
    */
    if (task_proxy.get_goals().size() == 1) {
        separate_facts_unreachable_before_goal();
    }
    bool found_concrete_solution = false;
    while (may_keep_refining()) {
        bool found_abstract_solution = abstract_search.find_solution(init, goals);
        if (!found_abstract_solution) {
            cout << "Abstract problem is unsolvable!" << endl;
            break;
        }
        unique_ptr<Flaw> flaw = find_flaw(abstract_search.get_solution());
        if (!flaw) {
            found_concrete_solution = true;
            break;
        }
        AbstractState *abstract_state = flaw->current_abstract_state;
        vector<Split> splits = flaw->get_possible_splits();
        const Split &split = split_selector.pick_split(*abstract_state, splits);
        refine(abstract_state, split.var_id, split.values);
    }
    cout << "Concrete solution found: " << found_concrete_solution << endl;
}

void Abstraction::refine(AbstractState *state, int var, const vector<int> &wanted) {
    if (debug)
        cout << "Refine " << *state << " for " << var << "=" << wanted << endl;
    pair<AbstractState *, AbstractState *> new_states = state->split(var, wanted);
    AbstractState *v1 = new_states.first;
    AbstractState *v2 = new_states.second;

    states.erase(state);
    states.insert(v1);
    states.insert(v2);

    /* Since the search is always started from the abstract initial state, v2
       is never the new initial state and v1 is never a goal state. */
    if (state == init) {
        assert(v1->includes(task_proxy.get_initial_state()));
        assert(!v2->includes(task_proxy.get_initial_state()));
        init = v1;
        if (debug)
            cout << "New init state: " << *init << endl;
    }
    if (is_goal(state)) {
        goals.erase(state);
        goals.insert(v2);
        if (debug)
            cout << "New/additional goal state: " << *v2 << endl;
    }

    int num_states = get_num_states();
    if (num_states % 1000 == 0)
        g_log << "Abstract states: " << num_states << "/" << max_states << endl;

    delete state;
}

unique_ptr<Flaw> Abstraction::find_flaw(const Solution &solution) {
    if (debug)
        cout << "Check solution:" << endl;

    AbstractState *abstract_state = init;
    State concrete_state = task_proxy.get_initial_state();
    assert(abstract_state->includes(concrete_state));

    if (debug)
        cout << "  Initial abstract state: " << *abstract_state << endl;

    for (const Arc &step : solution) {
        if (!utils::extra_memory_padding_is_reserved())
            break;
        int op_id = step.first;
        OperatorProxy op = task_proxy.get_operators()[op_id];
        AbstractState *next_abstract_state = step.second;
        if (is_applicable(op, concrete_state)) {
            if (debug)
                cout << "  Move to " << *next_abstract_state << " with "
                     << op.get_name() << endl;
            State next_concrete_state = concrete_state.get_successor(op);
            if (!next_abstract_state->includes(next_concrete_state)) {
                if (debug)
                    cout << "  Paths deviate." << endl;
                ++deviations;
                return utils::make_unique_ptr<Flaw>(
                    move(concrete_state),
                    abstract_state,
                    next_abstract_state->regress(op));
            }
            abstract_state = next_abstract_state;
            concrete_state = move(next_concrete_state);
        } else {
            if (debug)
                cout << "  Operator not applicable: " << op.get_name() << endl;
            ++unmet_preconditions;
            return utils::make_unique_ptr<Flaw>(
                move(concrete_state),
                abstract_state,
                AbstractState::get_abstract_state(
                    task_proxy, op.get_preconditions()));
        }
    }
    assert(is_goal(abstract_state));
    if (is_goal_state(task_proxy, concrete_state)) {
        // We found a concrete solution.
        return nullptr;
    } else {
        if (debug)
            cout << "  Goal test failed." << endl;
        ++unmet_goals;
        return utils::make_unique_ptr<Flaw>(
            move(concrete_state),
            abstract_state,
            AbstractState::get_abstract_state(
                task_proxy, task_proxy.get_goals()));
    }
}

void Abstraction::update_h_values() {
    abstract_search.backwards_dijkstra(goals);
    for (AbstractState *state : states) {
        state->set_h_value(state->get_search_info().get_g_value());
    }
}

int Abstraction::get_h_value_of_initial_state() const {
    return init->get_h_value();
}

vector<int> Abstraction::get_needed_costs() {
    return abstract_search.get_needed_costs(init, task_proxy.get_operators().size());
}

void Abstraction::print_statistics() {
    int total_incoming_arcs = 0;
    int total_outgoing_arcs = 0;
    int total_loops = 0;
    int dead_ends = 0;
    for (AbstractState *state : states) {
        if (state->get_h_value() == INF)
            ++dead_ends;
        const Arcs &incoming_arcs = state->get_incoming_arcs();
        const Arcs &outgoing_arcs = state->get_outgoing_arcs();
        const Loops &loops = state->get_loops();
        total_incoming_arcs += incoming_arcs.size();
        total_outgoing_arcs += outgoing_arcs.size();
        total_loops += loops.size();
    }
    assert(total_outgoing_arcs == total_incoming_arcs);

    int total_cost = 0;
    for (OperatorProxy op : task_proxy.get_operators())
        total_cost += op.get_cost();

    cout << "Total operator cost: " << total_cost << endl;
    cout << "States: " << get_num_states() << endl;
    cout << "Dead ends: " << dead_ends << endl;
    cout << "Init h: " << get_h_value_of_initial_state() << endl;

    cout << "Transitions: " << total_incoming_arcs << endl;
    cout << "Self-loops: " << total_loops << endl;

    cout << "Deviations: " << deviations << endl;
    cout << "Unmet preconditions: " << unmet_preconditions << endl;
    cout << "Unmet goals: " << unmet_goals << endl;
    cout << endl;
}
}
