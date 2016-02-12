#ifndef PDBS_DEADEND_DETECTION_HEURISTIC_H
#define PDBS_DEADEND_DETECTION_HEURISTIC_H

#include "types.h"

#include "../heuristic.h"

namespace utils {
class CountdownTimer;
}

namespace pdbs {
class DeadEndTreeNode;

class DeadEndCollection{
    int num_dead_ends;
    DeadEndTreeNode *root;
public:
    DeadEndCollection();
    ~DeadEndCollection();

    void add(const std::vector<FactProxy> &dead);

    bool recognizes(const std::vector<FactProxy> &partial_state) const;
    bool recognizes(const State &state) const;

    int size() {
        return num_dead_ends;
    }
};

class PDBDeadendDetectionHeuristic : public Heuristic {
    int max_dead_ends;
    bool add_pattern_dead_ends(const Pattern &pattern,
                               const utils::CountdownTimer &timer,
                               const State &initial_state);
    DeadEndCollection dead_end_collection;
protected:
    virtual int compute_heuristic(const GlobalState &state) override;
    int compute_heuristic(const State &state) const;
public:
    explicit PDBDeadendDetectionHeuristic(const options::Options &opts);
    virtual ~PDBDeadendDetectionHeuristic() = default;
};
}

#endif
