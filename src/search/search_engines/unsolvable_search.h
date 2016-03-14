#ifndef SEARCH_ENGINES_UNSOLVABLE_SEARCH_H
#define SEARCH_ENGINES_UNSOLVABLE_SEARCH_H

#include "../search_engine.h"

#include <memory>
#include <vector>

class Heuristic;
class PruningMethod;

namespace options {
class Options;
}

namespace unsolvable_search {
/* NOTE:
    Doesn't support reach_state
    Doesn't support bound
    Doesn't produce log lines for new g values
    Doesn't generate a plan file for solvable tasks
*/
class UnsolvableSearch : public SearchEngine {
    int current_state_id;
    std::vector<Heuristic *> heuristics;
    std::shared_ptr<PruningMethod> pruning_method;

    bool is_dead_end(const GlobalState &global_state);

protected:
    virtual void initialize() override;
    virtual SearchStatus step() override;

public:
    explicit UnsolvableSearch(const options::Options &opts);
    virtual ~UnsolvableSearch() = default;

    virtual void print_statistics() const override;
};
}

#endif
