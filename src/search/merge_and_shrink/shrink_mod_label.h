#ifndef MERGE_AND_SHRINK_SHRINK_MOD_LABEL_H
#define MERGE_AND_SHRINK_SHRINK_MOD_LABEL_H

#include "shrink_bisimulation.h"

namespace utils {
    template <typename Block>
    class DynamicBitset;
}

namespace merge_and_shrink {
class ShrinkModLabel : public ShrinkBisimulation {
protected:
    utils::DynamicBitset<unsigned short> compute_irrelevant_in_all_other_ts_labels(
        const FactoredTransitionSystem &fts,
        int excluded_ts_index) const;
    bool all_goal_variables_incorporated(
        const TransitionSystem &ts) const;
    virtual void compute_equivalence_relation(
        FactoredTransitionSystem &fts,
        int index,
        int target,
        StateEquivalenceRelation &equivalence_relation) const override;
    virtual void dump_strategy_specific_options() const override;
    virtual std::string name() const override;
public:
    explicit ShrinkModLabel(const options::Options &opts);
    virtual ~ShrinkModLabel() override;
};
}

#endif
