import numpy as np
from collections import deque


class AttentionEngine:
    def __init__(self, window_size=50):
        self.window = deque(maxlen=window_size)

    def update(self, score):
        self.window.append(score)

    def get_average(self):
        if len(self.window) == 0:
            return 0
        return float(np.mean(self.window))

    def get_active_inactive(self):
        active = 0
        inactive = 0

        for s in self.window:
            if s >= 60:
                active += 1
            else:
                inactive += 1

        return active, inactive

    def get_history(self):
        return list(self.window)