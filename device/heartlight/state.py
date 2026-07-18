class HeartRateState:
    def __init__(self):
        self.bpm = None
        self.rr_intervals = ()
        self.last_update_ms = None
        self.connected = False
        self.packet_count = 0
        self.decode_error_count = 0
        self.scanning = False
        self.candidate_name = None
        self.candidate_rssi = None
        self.connected_at_ms = None
        self.beat_anchor_ms = None
        self.beat_period_ms = None

    def reset_connection(self):
        self.connected = False
        self.bpm = None
        self.rr_intervals = ()
        self.last_update_ms = None
        self.connected_at_ms = None
        self.beat_anchor_ms = None
        self.beat_period_ms = None

    def update_measurement(self, bpm, rr_intervals, now_ms):
        self.bpm = bpm
        self.rr_intervals = rr_intervals
        self.last_update_ms = now_ms
        self.packet_count += 1
        self.beat_anchor_ms = now_ms
        if rr_intervals:
            self.beat_period_ms = max(1, int(rr_intervals[-1] * 1000))
        else:
            self.beat_period_ms = max(1, int(60000 / bpm))