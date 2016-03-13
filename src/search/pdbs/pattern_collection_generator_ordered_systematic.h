#ifndef PDBS_PATTERN_COLLECTION_GENERATOR_ORDERED_SYSTEMATIC_H
#define PDBS_PATTERN_COLLECTION_GENERATOR_ORDERED_SYSTEMATIC_H

#include "pattern_generator.h"

namespace options {
class Options;
}

namespace pdbs {
class PatternCollectionGeneratorOrderedSystematic : public PatternCollectionGenerator {
    int pattern_max_size;
public:
    explicit PatternCollectionGeneratorOrderedSystematic(const options::Options &opts);
    ~PatternCollectionGeneratorOrderedSystematic() = default;

    virtual PatternCollectionInformation generate(
        std::shared_ptr<AbstractTask> task,
        std::function<bool(const Pattern &)> handle_pattern = nullptr) override;
};
}

#endif
