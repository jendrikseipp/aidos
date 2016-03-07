#ifndef SEARCH_ENGINES_UNSOLVABLE_SEARCH_H
#define SEARCH_ENGINES_UNSOLVABLE_SEARCH_H

#include "../search_engine.h"

#include "../open_lists/open_list.h"

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
    std::unique_ptr<StateOpenList> open_list;
    std::vector<Heuristic *> heuristics;
    std::shared_ptr<PruningMethod> pruning_method;

    std::pair<SearchNode, bool> fetch_next_node();
    void print_checkpoint_line(int g) const;

protected:
    virtual void initialize() override;
    virtual SearchStatus step() override;

public:
    explicit UnsolvableSearch(const options::Options &opts);
    virtual ~UnsolvableSearch() = default;

    virtual void print_statistics() const override;

    void dump_search_space() const;
};
}

#endif
