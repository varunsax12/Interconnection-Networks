class networkAttr(object):
    CORE_ROWS = None
    CORE_COLS = None
    CORE_CORES = None
    CORE_VCS = None
    NET_TOTCYCLES = None
    NET_STARTCYCLES = None

    def __init__(self, core_rows, core_cols, core_cores, core_vcs, net_cycles, start_cycles):
        networkAttr.CORE_ROWS = int(core_rows)
        networkAttr.CORE_COLS = int(core_cols)
        networkAttr.CORE_CORES = int(core_cores)
        networkAttr.CORE_VCS = int(core_vcs)
        networkAttr.NET_TOTCYCLES = int(net_cycles)
        networkAttr.NET_STARTCYCLES = int(start_cycles)
