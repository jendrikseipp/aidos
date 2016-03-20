#include "pattern_collection_generator_ordered_systematic.h"

#include "pattern_collection_generator_systematic.h"

#include "../option_parser.h"
#include "../plugin.h"
#include "../task_proxy.h"

#include <algorithm>
#include <cassert>
#include <iostream>

using namespace std;

namespace pdbs {
PatternCollectionGeneratorOrderedSystematic::PatternCollectionGeneratorOrderedSystematic(const options::Options &opts)
    : pattern_max_size(opts.get<int>("pattern_max_size")) {
}

PatternCollectionInformation PatternCollectionGeneratorOrderedSystematic::generate(
    shared_ptr<AbstractTask> task, function<bool(const Pattern &)> handle_pattern) {
    shared_ptr<PatternCollection> patterns = make_shared<PatternCollection>();
    TaskProxy task_proxy(*task);
    pattern_max_size = min(pattern_max_size, static_cast<int>(task_proxy.get_variables().size()));
    bool done = false;
    for (int pattern_size = 1; pattern_size < pattern_max_size; ++pattern_size) {
        cout << "Generating patterns for size " << pattern_size << endl;
        options::Options opts;
        opts.set<int>("pattern_max_size", pattern_size);
        opts.set<bool>("only_interesting_patterns", true);
        PatternCollectionGeneratorSystematic generator(opts);
        generator.generate(task, [&](const Pattern &pattern) {
                if (static_cast<int>(pattern.size()) == pattern_size) {
                    patterns->push_back(pattern);
                    if (handle_pattern) {
                        done = handle_pattern(pattern);
                    }
                }
                return done;
            });
        if (done)
            break;
    }
    return PatternCollectionInformation(task, patterns);
}


static shared_ptr<PatternCollectionGenerator> _parse(OptionParser &parser) {
    parser.add_option<int>(
        "pattern_max_size",
        "max number of variables per pattern",
        "infinity",
        Bounds("1", "infinity"));
    Options opts = parser.parse();
    if (parser.dry_run())
        return nullptr;

    return make_shared<PatternCollectionGeneratorOrderedSystematic>(opts);
}

static PluginShared<PatternCollectionGenerator> _plugin("ordered_systematic", _parse);
}
