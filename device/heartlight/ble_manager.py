import asyncio
import bluetooth
import aioble


HEART_RATE_SERVICE = bluetooth.UUID(0x180D)
RUNNING_SPEED_CADENCE_SERVICE = bluetooth.UUID(0x1814)


class HeartRateBleManager:
    def __init__(self, state, diagnostics=True):
        self.state = state
        self.diagnostics = diagnostics
        self.running = False

    def log(self, *parts):
        if self.diagnostics:
            print("BLE:", *parts)

    def candidate_score(self, result):
        services = result.services()
        if HEART_RATE_SERVICE not in services:
            return None

        score = 100
        if RUNNING_SPEED_CADENCE_SERVICE in services:
            score += 20

        name = result.name() or ""
        lowered_name = name.lower()
        if "garmin" in lowered_name or "enduro" in lowered_name:
            score += 10
        return score

    async def scan_once(self, duration_ms=5000):
        best_result = None
        best_score = None
        self.state.scanning = True
        self.log("scanning for Heart Rate service")
        try:
            async with aioble.scan(
                duration_ms,
                interval_us=30000,
                window_us=30000,
                active=True,
            ) as scanner:
                async for result in scanner:
                    score = self.candidate_score(result)
                    if score is None:
                        continue
                    if best_result is None or score > best_score or (
                        score == best_score and result.rssi > best_result.rssi
                    ):
                        best_result = result
                        best_score = score
        finally:
            self.state.scanning = False

        if best_result:
            self.state.candidate_name = best_result.name() or "unnamed"
            self.state.candidate_rssi = best_result.rssi
            self.log("candidate", self.state.candidate_name, "RSSI", best_result.rssi)
        return best_result

    async def discovery_loop(self):
        self.running = True
        while self.running:
            await self.scan_once()
            await asyncio.sleep_ms(1000)

    def stop(self):
        self.running = False