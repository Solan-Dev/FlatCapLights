class HeartRateState:
    def __init__(self, period_window=5):
        self.period_window = max(1, int(period_window))
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
        self.period_samples_ms = []
        self.cadence_spm = None
        self.speed_mps = None
        self.stride_length_m = None
        self.total_distance_m = None
        self.last_cadence_update_ms = None
        self.step_anchor_ms = None
        self.cadence_packet_count = 0
        self.cadence_decode_error_count = 0

    def reset_connection(self):
        self.connected = False
        self.bpm = None
        self.rr_intervals = ()
        self.last_update_ms = None
        self.connected_at_ms = None
        self.beat_anchor_ms = None
        self.beat_period_ms = None
        self.period_samples_ms = []
        self.cadence_spm = None
        self.speed_mps = None
        self.stride_length_m = None
        self.total_distance_m = None
        self.last_cadence_update_ms = None
        self.step_anchor_ms = None

    def update_measurement(self, bpm, rr_intervals, now_ms):
        self.bpm = bpm
        self.rr_intervals = rr_intervals
        self.last_update_ms = now_ms
        self.packet_count += 1
        if rr_intervals:
            measured_period_ms = max(1, int(rr_intervals[-1] * 1000))
        else:
            measured_period_ms = max(1, int(60000 / bpm))

        self.period_samples_ms.append(measured_period_ms)
        if len(self.period_samples_ms) > self.period_window:
            self.period_samples_ms.pop(0)
        self.beat_period_ms = sum(self.period_samples_ms) // len(self.period_samples_ms)

        if self.beat_anchor_ms is None:
            self.beat_anchor_ms = now_ms

    def update_cadence(
        self,
        cadence_spm,
        speed_mps,
        stride_length_m,
        total_distance_m,
        now_ms,
    ):
        self.cadence_spm = cadence_spm
        self.speed_mps = speed_mps
        self.stride_length_m = stride_length_m
        self.total_distance_m = total_distance_m
        self.last_cadence_update_ms = now_ms
        self.cadence_packet_count += 1
        if self.step_anchor_ms is None:
            self.step_anchor_ms = now_ms