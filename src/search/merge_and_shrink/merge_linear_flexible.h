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
    std::vector<std::string> components;
    std::vector<int> variable_order;
    bool need_first_index;
protected:
    virtual void dump_strategy_specific_options() const override;
public:
    explicit MergeLinearFlexible(const options::Options &opts);
    virtual ~MergeLinearFlexible() override = default;
    virtual void initialize(const std::shared_ptr<AbstractTask> task) override;

    virtual std::pair<int, int> get_next(FactoredTransitionSystem &fts) override;
    virtual std::string name() const override;
    static void add_options_to_parser(options::OptionParser &parser);
};
}

#endif
