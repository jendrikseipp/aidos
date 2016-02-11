#ifndef PDBS_PATTERN_COLLECTION_GENERATOR_SYSTEMATIC_H
#define PDBS_PATTERN_COLLECTION_GENERATOR_SYSTEMATIC_H

#include "pattern_generator.h"
#include "types.h"

#include "../utils/hash.h"

#include <cstdlib>
#include <memory>
#include <unordered_set>
#include <vector>

class CausalGraph;
class TaskProxy;

namespace options {
class Options;
}

namespace pdbs {
class CanonicalPDBsHeuristic;

// Invariant: patterns are always sorted.
class PatternCollectionGeneratorSystematic : public PatternCollectionGenerator {
    using PatternSet = std::unordered_set<Pattern>;

    const size_t max_pattern_size;
    const bool only_interesting_patterns;
    std::shared_ptr<PatternCollection> patterns;
    PatternSet pattern_set;  // Cleared after pattern computation.

    bool enqueue_pattern_if_new(const Pattern &pattern,
                                std::function<bool(const Pattern &)> handle_pattern);
    void compute_eff_pre_neighbors(const CausalGraph &cg,
                                   const Pattern &pattern,
                                   std::vector<int> &result) const;
    void compute_connection_points(const CausalGraph &cg,
                                   const Pattern &pattern,
                                   std::vector<int> &result) const;

    bool build_sga_patterns(TaskProxy task_proxy, const CausalGraph &cg,
                            std::function<bool(const Pattern &)> handle_pattern);
    void build_patterns(TaskProxy task_proxy,
                        std::function<bool(const Pattern &)> handle_pattern);
    void build_patterns_naive(TaskProxy task_proxy,
                              std::function<bool(const Pattern &)> handle_pattern);
public:
    explicit PatternCollectionGeneratorSystematic(const options::Options &opts);
    ~PatternCollectionGeneratorSystematic() = default;

    virtual PatternCollectionInformation generate(
        std::shared_ptr<AbstractTask> task,
        std::function<bool(const Pattern &)> handle_pattern = nullptr) override;
};
}

#endif
