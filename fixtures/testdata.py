import numpy as np

# format is
#   key: (data, sample_rate)

barb_fixtures = {
    "test1.barb": ([0, 1, 2, 3, 4, -5, -4, -3, -2, -1, 0], 10),
    "test2.barb": ([-10, -9, -8, -7, -6, -5, -4, -3, -2, -1], 10),
    "test3.barb": ([0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0, 9, 0, 8, 0, 7, 0, 6, 0, 5, 0, 4],
                   1e9)
}