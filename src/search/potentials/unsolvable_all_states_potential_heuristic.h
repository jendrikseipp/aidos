#ifndef POTENTIALS_UNSOLVABLE_ALL_STATES_POTENTIAL_HEURISTIC_H
#define POTENTIALS_UNSOLVABLE_ALL_STATES_POTENTIAL_HEURISTIC_H

#include "../heuristic.h"

#include "../lp/lp_solver.h"

#include <memory>
#include <vector>

namespace potentials {
class PotentialFunction;

class UnsolvableAllStatesPotentialHeuristic : public Heuristic {
    lp::LPSolver lp_solver;
    std::vector<std::vector<int>> lp_var_ids;
    std::unique_ptr<PotentialFunction> potential_function;

    int get_lp_var_id(const FactProxy &fact) const;
    void construct_lp();
    std::unique_ptr<PotentialFunction> extract_potential_function() const;

protected:
    virtual int compute_heuristic(const GlobalState &global_state) override;

public:
    explicit UnsolvableAllStatesPotentialHeuristic(
        const options::Options &opts);
    ~UnsolvableAllStatesPotentialHeuristic();
};
}

#endif
