#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


COLORS = [
    (0, 0, 0),
    (181, 49, 32),  # Red
    (255, 204, 197),  # Flesh
    (255, 255, 255),  # White
]

MARIO = np.array([
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
    [3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, ],
    [3, 3, 3, 0, 1, 1, 1, 1, 1, 1, 0, 0, 3, 3, ],
    [3, 3, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 3, ],
    [3, 3, 0, 0, 0, 2, 2, 0, 2, 0, 0, 0, 3, 3, ],
    [3, 0, 2, 2, 0, 0, 2, 0, 2, 2, 2, 2, 0, 3, ],
    [3, 0, 2, 2, 0, 0, 2, 2, 0, 2, 2, 2, 0, 3, ],
    [3, 3, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 3, 3, ],
    [3, 3, 3, 0, 0, 2, 2, 2, 2, 2, 0, 3, 3, 3, ],
    [3, 3, 0, 1, 1, 0, 0, 1, 1, 0, 3, 3, 3, 3, ],
    [3, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 3, 3, 3, ],
    [3, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 3, 3, 3, ],
    [3, 3, 0, 2, 2, 2, 0, 0, 2, 0, 0, 3, 3, 3, ],
    [3, 3, 0, 2, 2, 1, 1, 1, 0, 0, 0, 3, 3, 3, ],
    [3, 3, 3, 0, 1, 1, 1, 1, 1, 0, 3, 3, 3, 3, ],
    [3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, ],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, ],
])
