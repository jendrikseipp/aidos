#ifndef MERGE_AND_SHRINK_SHRINK_MOD_LABEL_APPROX_H
#define MERGE_AND_SHRINK_SHRINK_MOD_LABEL_APPROX_H

#include "shrink_bisimulation.h"

namespace utils {
    template <typename Block>
    class DynamicBitset;
}

namespace merge_and_shrink {
class ShrinkModLabelApprox : public ShrinkBisimulation {
    utils::DynamicBitset<unsigned short> compute_irrelevant_in_all_other_ts_labels(
        const FactoredTransitionSystem &fts,
        int excluded_ts_index) const;
    bool all_goal_variables_incorporated(
            const TransitionSystem &ts) const;
    void shrink_own_label_cycles(FactoredTransitionSystem &fts,
        int index,
        const utils::DynamicBitset<unsigned short> &irrelevant_labels_in_all_other_ts) const;
    void shrink_own_label_goal_paths(
        FactoredTransitionSystem &fts,
        int index,
        const utils::DynamicBitset<unsigned short> &irrelevant_labels_in_all_other_ts) const;
protected:
    virtual void compute_equivalence_relation(
        FactoredTransitionSystem &fts,
        int index,
        int target,
        StateEquivalenceRelation &equivalence_relation) const override;
    virtual void dump_strategy_specific_options() const override;
    virtual std::string name() const override;
public:
    explicit ShrinkModLabelApprox(const options::Options &opts);
    virtual ~ShrinkModLabelApprox() override;
};
}

#endif
