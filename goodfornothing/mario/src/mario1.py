#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


COLORS = [
    (0, 0, 0),
    (227, 48, 25),  # Red
    (206, 34, 34),  # Med Red
    (176, 28, 28),  # Dk Red
    (219, 152, 61),
    (253, 213, 154),
    (26, 103, 147),  # Blue
    (99, 192, 226),  # Lt Blue
    (17, 53, 113),  # Dk Blue
    (254, 254, 254),  # White
]

MARIO = np.array([
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, ],
    [9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 0, 0, 0, 9, 9, ],
    [9, 9, 9, 9, 9, 9, 0, 0, 1, 1, 1, 0, 0, 4, 4, 4, 0, 9, ],
    [9, 9, 9, 9, 9, 0, 3, 2, 2, 2, 1, 1, 0, 4, 4, 4, 0, 9, ],
    [9, 9, 9, 9, 0, 3, 2, 2, 0, 0, 0, 0, 0, 0, 4, 4, 0, 9, ],
    [9, 9, 9, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 9, ],
    [9, 9, 9, 0, 3, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 9, 9, ],
    [9, 9, 0, 0, 0, 0, 4, 4, 4, 0, 4, 0, 4, 0, 2, 3, 0, 9, ],
    [9, 9, 0, 4, 0, 0, 4, 4, 4, 0, 4, 0, 4, 0, 2, 3, 0, 9, ],
    [9, 0, 4, 4, 0, 0, 0, 4, 4, 4, 4, 5, 5, 5, 0, 3, 0, 9, ],
    [9, 0, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 0, 3, 0, 9, ],
    [9, 9, 0, 4, 4, 4, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 9, 9, ],
    [9, 9, 9, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 3, 0, 9, 9, ],
    [9, 9, 9, 9, 0, 0, 0, 4, 4, 4, 4, 4, 0, 2, 3, 0, 9, 9, ],
    [9, 9, 9, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 3, 0, 9, 9, 9, ],
    [9, 9, 0, 3, 1, 1, 1, 2, 0, 0, 2, 1, 0, 0, 9, 9, 9, 9, ],
    [9, 0, 3, 2, 1, 0, 0, 0, 6, 0, 3, 2, 1, 0, 0, 9, 9, 9, ],
    [9, 0, 3, 3, 0, 4, 4, 4, 0, 6, 0, 3, 2, 2, 0, 9, 9, 9, ],
])
