#ifndef PDBS_DEADEND_DETECTION_HEURISTIC_H
#define PDBS_DEADEND_DETECTION_HEURISTIC_H

#include "types.h"

#include "../heuristic.h"

namespace pdbs {
class DeadEndTreeNode;

class DeadEndCollection{
    int num_deadends;
    DeadEndTreeNode *root;
public:
    DeadEndCollection();
    ~DeadEndCollection();

    void add(const std::vector<FactProxy> &dead);

    bool recognizes(const std::vector<FactProxy> &partial_state) const;
    bool recognizes(const State &state) const;

    int size() {
        return num_deadends;
    }
};

class PDBDeadendDetectionHeuristic : public Heuristic {
    int max_deadends;
    bool add_pattern_deadends(const Pattern &pattern);
    DeadEndCollection deadend_collection;
protected:
    virtual int compute_heuristic(const GlobalState &state) override;
    int compute_heuristic(const State &state) const;
public:
    explicit PDBDeadendDetectionHeuristic(const options::Options &opts);
    virtual ~PDBDeadendDetectionHeuristic() = default;
};
}

#endif
