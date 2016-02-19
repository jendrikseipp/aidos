from lab.reports import Attribute, avg

def get():
    # planner outcome attributes
    unsolvable = Attribute('unsolvable', absolute=True, min_wins=False)
    search_out_of_memory = Attribute('search_out_of_memory', absolute=True, min_wins=True)
    search_out_of_time = Attribute('search_out_of_time', absolute=True, min_wins=True)

    # m&s attributes
    ms_construction_time = Attribute('ms_construction_time', absolute=False, min_wins=True, functions=[avg])
    ms_abstraction_constructed = Attribute('ms_abstraction_constructed', absolute=True, min_wins=False)
    ms_final_size = Attribute('ms_final_size', absolute=False, min_wins=True)
    ms_out_of_memory = Attribute('ms_out_of_memory', absolute=True, min_wins=True)
    ms_out_of_time = Attribute('ms_out_of_time', absolute=True, min_wins=True)
    ms_memory_delta = Attribute('ms_memory_delta', absolute=False, min_wins=True)
    ms_unsolvable = Attribute('ms_unsolvable', absolute=True, min_wins=False)

    attributes = [
        unsolvable,
        search_out_of_memory,
        search_out_of_time,

        ms_construction_time,
        ms_abstraction_constructed,
        ms_final_size,
        ms_out_of_memory,
        ms_out_of_time,
        ms_memory_delta,
        ms_unsolvable,
    ]

    return attributes
