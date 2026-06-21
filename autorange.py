class AutoRanger:
    def __init__(self):
        self.current_range = 1
        self.up_trigger_count = 0
        self.down_trigger_count = 0

        self.ranges = {
            1: {"max": 100, "up": 90, "down": 0},
            2: {"max": 1000, "up": 900, "down": 100},
            3: {"max": 10000, "up": 9000, "down": 1000},
            4: {"max": 100000, "up": 90000, "down": 10000},
            5: {"max": 1000000, "up": 900000, "down": 100000},
            6: {"max": 10000000, "up": 9000000, "down": 1000000},
        }

    def process_reading(self, reading):
        # Changed from 8 to 6 to reflect the new max range
        if reading > self.ranges[6]["max"] and self.current_range == 6:
            return "OL", self.current_range

        current_up_thresh = self.ranges[self.current_range]["up"]
        current_down_thresh = self.ranges[self.current_range]["down"]

        # Changed from 8 to 6 to reflect the new max range
        if reading > current_up_thresh and self.current_range < 6:
            self.up_trigger_count += 1
            self.down_trigger_count = 0
        elif reading < current_down_thresh and self.current_range > 1:
            self.down_trigger_count += 1
            self.up_trigger_count = 0
        else:
            self.up_trigger_count = 0
            self.down_trigger_count = 0

        # Hysteresis rule: require 3 consecutive triggers before switching
        if self.up_trigger_count >= 3:
            self.current_range += 1
            self.up_trigger_count = 0
        elif self.down_trigger_count >= 3:
            self.current_range -= 1
            self.down_trigger_count = 0

        return reading, self.current_range
