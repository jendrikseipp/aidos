#ifndef SEARCH_ENGINES_UNSOLVABLE_SEARCH_H
#define SEARCH_ENGINES_UNSOLVABLE_SEARCH_H

#include "../search_engine.h"

#include <deque>
#include <memory>
#include <vector>

class GlobalOperator;
class Heuristic;
class PruningMethod;
class ScalarEvaluator;

namespace options {
class Options;
}

namespace unsolvable_search {
class UnsolvableSearch : public SearchEngine {
    std::deque<StateID> queue;
    std::vector<Heuristic *> heuristics;
    std::shared_ptr<PruningMethod> pruning_method;
    int max_g;

    std::pair<SearchNode, bool> fetch_next_node();
    void print_checkpoint_line(int g) const;
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
