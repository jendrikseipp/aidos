# Aidos 1 and 2 can use this minimal build. Aidos 3 needs release64.
aidos_ipc = [
    "-DCMAKE_BUILD_TYPE=Release",
    "-DALLOW_64_BIT=True",
    "-DCMAKE_CXX_FLAGS='-m64'",
    "-DDISABLE_PLUGINS_BY_DEFAULT=YES",
    "-DPLUGIN_CEGAR_ENABLED=YES",
    "-DPLUGIN_EAGER_SEARCH_ENABLED=YES",
    "-DPLUGIN_IPC_MAX_HEURISTIC_ENABLED=YES",
    "-DPLUGIN_LANDMARK_CUT_HEURISTIC_ENABLED=YES",
    "-DPLUGIN_OPERATOR_COUNTING_ENABLED=YES",
    "-DPLUGIN_PDBS_ENABLED=YES",
    "-DPLUGIN_StubbornSetsEC_ENABLED=YES",
    "-DPLUGIN_UNSOLVABLE_SEARCH_ENABLED=YES",
]
