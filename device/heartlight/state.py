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

    def reset_connection(self):
        self.connected = False
        self.bpm = None
        self.rr_intervals = ()
        self.last_update_ms = None