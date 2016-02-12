#include "deadend_detection_heuristic.h"

#include "pattern_database.h"
#include "pattern_generator.h"

#include "../option_parser.h"
#include "../plugin.h"

#include "../utils/countdown_timer.h"

#include <memory>

using namespace std;

namespace pdbs {
class DeadEndTreeNode {
public:
    virtual ~DeadEndTreeNode() = default;
    virtual void add(const std::vector<FactProxy> &partial_state, int index = 0) = 0;
    virtual bool contains(const std::vector<FactProxy> &partial_state, int index = 0) = 0;
    virtual bool contains(const State &state) = 0;
};

class DeadEndTreeLeafNode : public DeadEndTreeNode {
public:
    virtual void add(const std::vector<FactProxy> &/*partial_state*/, int /*index*/) override {
        // No need to add, this node already recognizes the dead end.
    }

    virtual bool contains(const std::vector<FactProxy> &/*partial_state*/, int /*index*/) override {
        return true;
    }

    virtual bool contains(const State &/*state*/) override {
        return true;
    }
};

class DeadEndTreeSwitchNode : public DeadEndTreeNode {
    int var_id;
    vector<DeadEndTreeNode *> value_successors;
    DeadEndTreeNode *ignore_successor;
public:
    DeadEndTreeSwitchNode(VariableProxy var)
        : var_id(var.get_id()),
          value_successors(var.get_domain_size(), nullptr),
          ignore_successor(nullptr) {
    }

    virtual ~DeadEndTreeSwitchNode() {
        for (DeadEndTreeNode *child : value_successors)
            delete child;
        delete ignore_successor;
    }

    virtual void add(const std::vector<FactProxy> &partial_state, int index = 0) override {
        const FactProxy &current_fact = partial_state[index];
        VariableProxy current_var = current_fact.get_variable();
        int current_value = current_fact.get_value();
        DeadEndTreeNode **successor;
        int next_index = index;
        if (var_id == current_var.get_id()) {
            successor = &value_successors[current_value];
            ++next_index;
        } else {
            successor = &ignore_successor;
        }

        if (*successor) {
            (*successor)->add(partial_state, next_index);
        } else {
            if (index == static_cast<int>(partial_state.size()) - 1) {
                *successor = new DeadEndTreeLeafNode();
            } else {
                VariableProxy next_var = partial_state[next_index].get_variable();
                *successor = new DeadEndTreeSwitchNode(next_var);
                (*successor)->add(partial_state, next_index);
            }
        }
    }

    virtual bool contains(const std::vector<FactProxy> &partial_state, int index = 0) override {
        if (index == static_cast<int>(partial_state.size()))
            return false;
        const FactProxy &current_fact = partial_state[index];
        int current_var_id = current_fact.get_variable().get_id();
        int current_value = current_fact.get_value();
        int next_index = index;
        if (var_id == current_var_id) {
            ++next_index;
            DeadEndTreeNode *value_successor = value_successors[current_value];
            if (value_successor && value_successor->contains(partial_state, next_index))
                return true;
        }
        if (ignore_successor && ignore_successor->contains(partial_state, next_index))
            return true;
        return false;
    }

    virtual bool contains(const State &state) override {
        DeadEndTreeNode *value_successor = value_successors[state[var_id].get_value()];
        if (value_successor && value_successor->contains(state))
            return true;
        if (ignore_successor && ignore_successor->contains(state))
            return true;
        return false;
    }
};

DeadEndCollection::DeadEndCollection()
    : num_deadends(0),
      root(nullptr) {
}

DeadEndCollection::~DeadEndCollection() {
    delete root;
}

void DeadEndCollection::add(const std::vector<FactProxy> &dead){
    if (!root) {
        root = new DeadEndTreeSwitchNode(dead[0].get_variable());
    }
    root->add(dead);
    ++num_deadends;
}

bool DeadEndCollection::recognizes(const std::vector<FactProxy> &partial_state) const {
    if (root) {
        return root->contains(partial_state);
    }
    return false;
}

bool DeadEndCollection::recognizes(const State &state) const {
    if (root) {
        return root->contains(state);
    }
    return false;
}

PDBDeadendDetectionHeuristic::PDBDeadendDetectionHeuristic(const options::Options &opts)
    : Heuristic(opts),
      max_deadends(opts.get<int>("max_deadends")) {
    shared_ptr<PatternCollectionGenerator> pattern_generator =
        opts.get<shared_ptr<PatternCollectionGenerator>>("patterns");
    utils::CountdownTimer timer(opts.get<int>("max_time"));
    State initial_state = task_proxy.get_initial_state();
    pattern_generator->generate(task, [&](const Pattern &pattern) {
        add_pattern_deadends(pattern);
        bool memory_exhausted = deadend_collection.size() >= max_deadends;
        bool initial_state_recognized = deadend_collection.recognizes(initial_state);
        return memory_exhausted || initial_state_recognized || timer.is_expired();
    });
    cout << "Found " << deadend_collection.size() << " dead ends in " << timer << endl;
}

void PDBDeadendDetectionHeuristic::add_pattern_deadends(const Pattern &pattern) {
    PatternDatabase pdb(task_proxy, pattern, false, true);
    for (const vector<FactProxy> &dead : pdb.get_dead_ends()) {
        if (!deadend_collection.recognizes(dead)) {
            deadend_collection.add(dead);
        }
    }
}

int PDBDeadendDetectionHeuristic::compute_heuristic(const GlobalState &global_state) {
    State state = convert_global_state(global_state);
    return compute_heuristic(state);
}

int PDBDeadendDetectionHeuristic::compute_heuristic(const State &state) const {
    if (deadend_collection.recognizes(state)) {
        return DEAD_END;
    } else {
        return 0;
    }
}

static Heuristic *_parse(OptionParser &parser) {
    parser.add_option<shared_ptr<PatternCollectionGenerator>>(
        "patterns",
        "pattern generation method",
        "systematic(1000)");

    parser.add_option<int>(
        "max_time",
        "maximal time used to search for dead ends",
        "900");

    parser.add_option<int>(
        "max_deadends",
        "maximal number of dead ends stored before starting the search",
        "1000000");

    Heuristic::add_options_to_parser(parser);

    Options opts = parser.parse();
    if (parser.dry_run())
        return nullptr;

    return new PDBDeadendDetectionHeuristic(opts);
}

static Plugin<Heuristic> _plugin("deadpdbs", _parse);
}
