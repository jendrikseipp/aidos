#ifndef PDBS_DEADEND_PDBS_SIMPLE_HEURISTIC_H
#define PDBS_DEADEND_PDBS_SIMPLE_HEURISTIC_H

#include "types.h"

#include "../heuristic.h"

#include <memory>

namespace pdbs {
class DeadendPDBsSimpleHeuristic : public Heuristic {
    std::shared_ptr<PDBCollection> pdbs;

protected:
    virtual int compute_heuristic(const GlobalState &state) override;
    int compute_heuristic(const State &state) const;

public:
    explicit DeadendPDBsSimpleHeuristic(const options::Options &opts);
    virtual ~DeadendPDBsSimpleHeuristic() = default;
};
}

#endif
