#include "unsolvable_all_states_potential_heuristic.h"

#include "potential_function.h"

#include "../option_parser.h"
#include "../plugin.h"

#include <unordered_map>

using namespace std;


namespace potentials {
static const double max_potential = 1e8;

UnsolvableAllStatesPotentialHeuristic::UnsolvableAllStatesPotentialHeuristic(
    const Options &opts)
    : Heuristic(opts),
      lp_solver(lp::LPSolverType(opts.get_enum("lpsolver"))) {
    construct_lp();
    lp_solver.solve();
    assert(lp_solver.has_optimal_solution());
    potential_function = extract_potential_function();
}

UnsolvableAllStatesPotentialHeuristic::~UnsolvableAllStatesPotentialHeuristic() {
}

static int get_undefined_value(const VariableProxy &var) {
    return var.get_domain_size();
}

int UnsolvableAllStatesPotentialHeuristic::get_lp_var_id(
    const FactProxy &fact) const {
    int var_id = fact.get_variable().get_id();
    int value = fact.get_value();
    assert(utils::in_bounds(var_id, lp_var_ids));
    assert(utils::in_bounds(value, lp_var_ids[var_id]));
    return lp_var_ids[var_id][value];
}

void UnsolvableAllStatesPotentialHeuristic::construct_lp() {
    VariablesProxy vars = task_proxy.get_variables();
    lp_var_ids.resize(vars.size());

    vector<lp::LPVariable> lp_variables;
    for (VariableProxy var : vars) {
        const int var_id = var.get_id();
        const int orig_domain_size = var.get_domain_size();
        // Note the "+1" for "undefined" facts.
        lp_var_ids[var_id].resize(orig_domain_size + 1);
        /* Add LP variable for each "real" fact. Set its coefficient to
           the fraction of syntactic states it appears in. Ignore
           "undefined" facts here. They're not part of any state. */
        const double coefficient = 1.0 / orig_domain_size;
        for (int value = 0; value < orig_domain_size; ++value) {
            lp_var_ids[var_id][value] = lp_variables.size();
            lp_variables.emplace_back(
                -lp_solver.get_infinity(), max_potential, coefficient);
        }
        // Add LP variable for "undefined" fact.
        const int undefined_value = orig_domain_size;
        lp_var_ids[var_id][undefined_value] = lp_variables.size();
        lp_variables.emplace_back(-lp_solver.get_infinity(), max_potential, 0.0);
    }

    vector<lp::LPConstraint> lp_constraints;
    for (OperatorProxy op : task_proxy.get_operators()) {
        // Create constraint:
        // Sum_{V in vars(eff(o))} (P_{V=pre(o)[V]} - P_{V=eff(o)[V]}) <= 0
        unordered_map<int, int> var_to_precondition;
        for (FactProxy pre : op.get_preconditions()) {
            var_to_precondition[pre.get_variable().get_id()] = pre.get_value();
        }
        lp::LPConstraint constraint(-lp_solver.get_infinity(), 0);
        for (EffectProxy effect : op.get_effects()) {
            VariableProxy var = effect.get_fact().get_variable();
            int var_id = var.get_id();

            // Set pre to pre(op) if defined, otherwise to u = |dom(var)|.
            int pre = -1;
            auto it = var_to_precondition.find(var_id);
            if (it == var_to_precondition.end()) {
                pre = get_undefined_value(var);
            } else {
                pre = it->second;
            }

            int post = effect.get_fact().get_value();
            int pre_lp = lp_var_ids[var_id][pre];
            int post_lp = lp_var_ids[var_id][post];
            assert(pre_lp != post_lp);
            constraint.insert(pre_lp, 1);
            constraint.insert(post_lp, -1);
        }
        lp_constraints.push_back(move(constraint));
    }

    /* Create full goal state. Use value |dom(V)| as "undefined" value
       for variables V undefined in the goal. */
    vector<int> goal(task_proxy.get_variables().size(), -1);
    for (FactProxy fact : task_proxy.get_goals()) {
        goal[fact.get_variable().get_id()] = fact.get_value();
    }
    for (VariableProxy var : task_proxy.get_variables()) {
        if (goal[var.get_id()] == -1)
            goal[var.get_id()] = get_undefined_value(var);
    }

    for (VariableProxy var : task_proxy.get_variables()) {
        /*
          Create constraint (using variable bounds): P_{V=goal[V]} = 0
          When each variable has a goal value (including the
          "undefined" value), this is equivalent to the goal-awareness
          constraint \sum_{fact in goal} P_fact <= 0. We can't set the
          potential of one goal fact to +2 and another to -2, but if
          all variables have goal values, this is not beneficial
          anyway.
        */
        int var_id = var.get_id();
        lp::LPVariable &lp_var = lp_variables[lp_var_ids[var_id][goal[var_id]]];
        lp_var.lower_bound = 0;
        lp_var.upper_bound = 0;

        int undef_val_lp = lp_var_ids[var_id][get_undefined_value(var)];
        for (int val = 0; val < var.get_domain_size(); ++val) {
            int val_lp = lp_var_ids[var_id][val];
            // Create constraint: P_{V=v} <= P_{V=u}
            // Note that we could eliminate variables P_{V=u} if V is
            // undefined in the goal.
            lp::LPConstraint constraint(-lp_solver.get_infinity(), 0);
            constraint.insert(val_lp, 1);
            constraint.insert(undef_val_lp, -1);
            lp_constraints.push_back(constraint);
        }
    }
    lp_solver.load_problem(
        lp::LPObjectiveSense::MAXIMIZE, lp_variables, lp_constraints);
}

unique_ptr<PotentialFunction>
UnsolvableAllStatesPotentialHeuristic::extract_potential_function() const {
    assert(lp_solver.has_optimal_solution());

    VariablesProxy vars = task_proxy.get_variables();

    vector<vector<double>> fact_potentials;
    fact_potentials.resize(vars.size());
    for (VariableProxy var : vars) {
        fact_potentials[var.get_id()].resize(var.get_domain_size());
    }

    const vector<double> solution = lp_solver.extract_solution();
    for (FactProxy fact : vars.get_facts()) {
        fact_potentials[fact.get_variable().get_id()][fact.get_value()] =
            solution[get_lp_var_id(fact)];
    }
    return utils::make_unique_ptr<PotentialFunction>(move(fact_potentials));
}

int UnsolvableAllStatesPotentialHeuristic::compute_heuristic(
    const GlobalState &global_state) {
    assert(potential_function);
    State state = task_proxy.convert_global_state(global_state);
    int h = potential_function->get_value(state);
    if (h >= 1) {
        return DEAD_END;
    }
    return 0;
}

static Heuristic *_parse(OptionParser &parser) {
    parser.document_synopsis(
        "Potential heuristic detecting dead ends",
        "");

    Heuristic::add_options_to_parser(parser);
    lp::add_lp_solver_option_to_parser(parser);

    Options opts = parser.parse();
    if (parser.dry_run())
        return nullptr;

    return new UnsolvableAllStatesPotentialHeuristic(opts);
}

static Plugin<Heuristic> _plugin("unsolvable_all_states_potential", _parse);
}
