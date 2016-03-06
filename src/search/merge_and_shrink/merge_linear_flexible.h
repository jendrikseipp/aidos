#ifndef MERGE_AND_SHRINK_MERGE_LINEAR_FLEXIBLE_H
#define MERGE_AND_SHRINK_MERGE_LINEAR_FLEXIBLE_H

#include "merge_strategy.h"

#include "../variable_order_finder.h"

namespace options {
class Options;
class OptionParser;
}

namespace merge_and_shrink {
class MergeLinearFlexible : public MergeStrategy {
    const std::vector<std::string> components;
    std::vector<int> variable_order;
    std::vector<int> remaining_variables;
    std::vector<bool> is_goal_variable;
    std::vector<bool> is_causal_predecessor;
    bool need_first_index;
    std::vector<int> variable_to_scc_index;

    std::vector<int> select_next_vars(
        std::string current_component,
        std::vector<int> &variable_indices);
    void set_variable(TaskProxy &task_proxy, int next_variable_index);
protected:
    virtual void dump_strategy_specific_options() const override;
public:
    explicit MergeLinearFlexible(const options::Options &opts);
    virtual ~MergeLinearFlexible() override = default;
    virtual void initialize(const std::shared_ptr<AbstractTask> task) override;

    virtual std::pair<int, int> get_next(FactoredTransitionSystem &fts) override;
    virtual std::string name() const override;
};
}

#endif
