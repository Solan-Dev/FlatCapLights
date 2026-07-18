import asyncio
import bluetooth
import aioble
import time

from .heart_rate import decode_measurement


HEART_RATE_SERVICE = bluetooth.UUID(0x180D)
HEART_RATE_MEASUREMENT = bluetooth.UUID(0x2A37)
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
            candidate = await self.scan_once()
            if candidate:
                await self.connect_and_monitor(candidate)
            await asyncio.sleep_ms(1000)

    def stop(self):
        self.running = False

    async def connect_and_monitor(self, result):
        connection = None
        try:
            self.log("connecting to", self.state.candidate_name)
            connection = await result.device.connect(timeout_ms=8000)
            async with connection:
                self.log("connected; discovering heart-rate characteristic")
                service = await connection.service(HEART_RATE_SERVICE, timeout_ms=5000)
                measurement = await service.characteristic(
                    HEART_RATE_MEASUREMENT,
                    timeout_ms=5000,
                )
                await measurement.subscribe(notify=True)
                self.log("subscribed; waiting for heart-rate measurement")

                while self.running and connection.is_connected():
                    try:
                        data = await measurement.notified(timeout_ms=5000)
                        bpm, rr_intervals = decode_measurement(data)
                    except asyncio.TimeoutError:
                        continue
                    except ValueError as exc:
                        self.state.decode_error_count += 1
                        self.log("invalid measurement", exc)
                        continue

                    now_ms = time.ticks_ms()
                    if not self.state.connected:
                        self.state.connected = True
                        self.state.connected_at_ms = now_ms
                        self.log("valid measurement; connected")
                    self.state.update_measurement(bpm, rr_intervals, now_ms)
                    self.log("heart rate", bpm, "BPM")
        except asyncio.TimeoutError:
            self.log("connection or discovery timeout")
        except Exception as exc:
            self.log("connection failed", exc)
        finally:
            self.state.reset_connection()
            if connection:
                try:
                    await connection.disconnect()
                except Exception:
                    pass
            self.log("disconnected")