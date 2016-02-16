#ifndef MERGE_AND_SHRINK_SHRINK_MOD_LABEL_H
#define MERGE_AND_SHRINK_SHRINK_MOD_LABEL_H

#include "shrink_bisimulation.h"

namespace options {
class Options;
}

namespace merge_and_shrink {
class ShrinkModLabel : public ShrinkBisimulation {
protected:
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
