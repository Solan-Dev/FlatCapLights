# Garmin Enduro 1 to Pimoroni Plasma 2350 W over BLE

## Status

Implementation brief for review. This document defines the proposed direct Bluetooth Low Energy connection between a Garmin Enduro 1 and a Pimoroni Plasma 2350 W running MicroPython. The intended deployment is a short installation lasting a couple of nights.

## Objective

Use the Enduro 1's wrist heart-rate sensor to drive addressable LEDs connected to the Plasma 2350 W over a direct BLE connection.

```text
Garmin Enduro 1 -- BLE Virtual Run --> Plasma 2350 W -- PIO --> LED strip
```

The lighting effect itself is outside this brief. The BLE layer must expose current heart rate and any supplied RR intervals through a stable internal state interface.

## Confirmed Garmin behaviour

The normal **Broadcast Heart Rate** function on the Enduro 1 is primarily the ANT+ route and is not the route used here.

The Enduro 1 supports a **Virtual Run** activity. Garmin documents that Virtual Run pairs the watch with a compatible third-party application over Bluetooth and transmits pace, heart rate and cadence. The intended watch procedure is:

1. Press `START`.
2. Select **Virtual Run**.
3. Allow the receiving device to connect.
4. Press `START` to begin the activity timer.
5. Stop and save or discard the activity when finished.

Garmin documentation:

- [Enduro 1: Going for a Virtual Run](https://www8.garmin.com/manuals/webhelp/GUID-BD965919-30AA-4EB5-95D7-A899658C50EB/EN-US/GUID-9F45EF2C-D6D5-4583-B4C6-A386743B650A.html)
- [Garmin support: Using the Virtual Run Feature](https://support.garmin.com/en-US/?faq=pyniXQfLiu3BS1yKFlLn36)
- [Enduro 1: Broadcasting Heart Rate Data](https://www8.garmin.com/manuals/webhelp/GUID-BD965919-30AA-4EB5-95D7-A899658C50EB/EN-US/GUID-D8D363C2-0690-48D4-95E2-A3557E7D53C2.html)

### Device identity finding

Garmin's public Enduro and Virtual Run documentation does **not** specify:

- whether Virtual Run performs BLE bonding;
- whether the watch remembers a particular Virtual Run client;
- whether its advertised BLE address is public, static-random or private;
- how long that address remains stable;
- whether a serial number is exposed through the standard BLE Device Information Service.

Therefore, the implementation must not claim or require a permanent Garmin BLE address. BLE privacy permits peripherals to use addresses that change, and Garmin provides no product-level guarantee to the contrary.

For this short deployment, permanent identity is unnecessary. The receiver will rediscover the watch whenever required and use layered, runtime identification. A previously observed address may be cached as a preference, but never treated as the only way to find the watch.

## Plasma operating mode and pairing model

BLE heart-rate operation is a specific selectable mode on the Plasma board. **Button A** cycles through the board's available operating modes. When the user selects the BLE heart-rate mode, the Plasma begins scanning for the Garmin Virtual Run BLE connection.

Selecting this mode does not erase or reconfigure other modes. Leaving it stops the heart-rate presentation and ends or closes the active BLE session cleanly.

### Visual states in BLE heart-rate mode

| State | LED behaviour |
| --- | --- |
| Searching/not connected | Strong red heartbeat animation, using a synthetic resting beat so it is visibly waiting |
| Connection established | Brief green confirmation flash |
| Connected and receiving heart rate | Orange-red base colour with LED brightness pulsing in time with the received heartbeat |
| Connection lost or measurements become stale | Return to the strong red searching heartbeat while scanning resumes |

The green indication is a transition, not a persistent state. After it completes, the board moves directly into the connected orange-red heartbeat display.

For heartbeat timing, prefer RR intervals supplied in Heart Rate Measurement notifications. When RR intervals are absent, derive the pulse period from the latest BPM. The renderer should phase the brightness pulse independently of notification arrival time so the animation remains smooth between BLE updates.

Treat Virtual Run as a connectable BLE fitness-sensor session, not as conventional phone-style permanent pairing.

- The Plasma is the BLE **central/GATT client**.
- The Enduro is the BLE **peripheral/GATT server**.
- No PIN or passkey workflow is expected.
- The Plasma scans only while disconnected.
- The Plasma connects, discovers the required GATT characteristic and subscribes to notifications.
- Closing Virtual Run or moving out of range ends the session.
- The Plasma automatically scans and reconnects when Virtual Run becomes available again.

Do not add bonding unless the Enduro explicitly requests security during implementation. Forced bonding adds stale-key and firmware-compatibility failure modes without a documented requirement.

## Reliable watch selection for a two-night deployment

### Selection strategy

When Button A selects BLE heart-rate mode:

1. Plasma displays the strong red searching heartbeat and scans for connectable BLE advertisements.
2. User opens Virtual Run with the Enduro within approximately 0.5 m of the Plasma.
3. Prefer advertisements containing the standard Heart Rate service UUID `0x180D`.
4. Give additional preference to Running Speed and Cadence service UUID `0x1814`, if advertised.
5. Give additional preference to a local name containing `Garmin` or `Enduro`, if supplied.
6. Prefer the strongest RSSI candidate matching the services.
7. Connect and verify the Heart Rate service and measurement characteristic.
8. Accept the device only after receiving valid Heart Rate Measurement notifications.
9. Flash green to confirm the completed connection.
10. Enter the orange-red live heartbeat display.
11. Cache the successful address in RAM for fast reconnection during the current power cycle.
12. Optionally store the last successful address in a config file, but always fall back to a fresh service-based scan.

## BLE services and data

Required standard UUIDs:

| Purpose | UUID |
| --- | --- |
| Heart Rate service | `0x180D` |
| Heart Rate Measurement characteristic | `0x2A37` |
| Running Speed and Cadence service, supporting evidence only | `0x1814` |
| Device Information service, optional | `0x180A` |
| Manufacturer Name, optional | `0x2A29` |
| Model Number, optional | `0x2A24` |
| Serial Number, optional | `0x2A25` |

The implementation must not require the optional identity characteristics. If they exist, log them for diagnostics.

### Heart Rate Measurement format

`0x2A37` notifications use the Bluetooth Heart Rate Profile format:

- byte 0: flags;
- next 1 or 2 bytes: heart rate in BPM;
- optional 2-byte energy-expended field;
- optional repeated 2-byte RR intervals, each in units of 1/1024 second.

The decoder must support both 8-bit and 16-bit BPM and correctly skip optional fields. It must reject truncated packets without terminating the BLE session.

Useful specifications:

- [Bluetooth SIG Heart Rate Service](https://www.bluetooth.com/specifications/specs/heart-rate-service-1-0/)
- [Bluetooth SIG Device Information Service](https://www.bluetooth.com/specifications/specs/dis-1-2/)

## Plasma firmware and dependencies

Use the latest stable Pimoroni MicroPython firmware specifically supporting **Plasma 2350 W** and its RM2/CYW43439 radio.

Dependencies:

| Module | Source | Role |
| --- | --- | --- |
| `bluetooth` | MicroPython/Pimoroni firmware | BLE radio and UUIDs |
| `asyncio` | MicroPython firmware | Cooperative task scheduling |
| `aioble` | `micropython-lib` | BLE scanning, connection, discovery and notifications |
| `plasma` | Pimoroni firmware | LED-strip output |
| `struct`, `time`, `machine` | MicroPython firmware | Decoding, timing and watchdog |

References:

- [Pimoroni RP2350 MicroPython releases](https://github.com/pimoroni/pimoroni-pico-rp2350/releases)
- [Pimoroni Plasma repository and firmware links](https://github.com/pimoroni/plasma)
- [MicroPython Bluetooth API](https://docs.micropython.org/en/latest/library/bluetooth.html)
- [Official `aioble` library](https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble)
- [`aioble` client example](https://github.com/micropython/micropython-lib/blob/master/micropython/bluetooth/aioble/examples/temp_client.py)

Install `aioble` during development with `mip.install("aioble")`, then keep a known working copy on the board. Production startup must not download dependencies.

## Application architecture

```text
main.py
  ├── BLE connection manager
  │     ├── scan and select candidate
  │     ├── connect and discover GATT
  │     ├── subscribe to 0x2A37
  │     └── disconnect and retry with backoff
  ├── heart-rate decoder
  ├── shared latest-state object
  ├── LED renderer at a fixed frame rate
  └── supervisor/watchdog
```

Suggested files:

```text
/
├── boot.py
├── main.py
├── config.py
└── lib/heartlight/
    ├── ble_manager.py
    ├── heart_rate.py
    ├── state.py
    ├── renderer.py
    └── diagnostics.py
```

### BLE connection manager

The connection manager owns all BLE operations. Its lifecycle is:

```text
SCANNING -> CONNECTING -> DISCOVERING -> SUBSCRIBED
    ^              failure/disconnect              |
    +---------------- BACKOFF <--------------------+
```

Requirements:

- initialise BLE once at application startup;
- scan only while disconnected;
- use the layered selection strategy above;
- use explicit timeouts around scan, connect and discovery;
- subscribe to `0x2A37` notifications;
- consider the session healthy only after a valid measurement arrives;
- cleanly close failed connections before rescanning;
- retry indefinitely with bounded backoff of approximately 1, 2, 4, 8 and 15 seconds;
- reset backoff after a healthy subscription;
- never reboot merely because the watch is absent.

### Shared state

BLE processing publishes into one bounded latest-state object:

```python
class HeartRateState:
    bpm = None
    rr_intervals = ()
    last_update_ms = None
    connected = False
    packet_count = 0
    decode_error_count = 0
```

The LED renderer reads this state but does not perform BLE operations. Do not build an unbounded notification queue.

### Stale-data policy

- Under 3 seconds old: healthy.
- 3–10 seconds old: stale; fade or show a neutral state.
- Over 10 seconds old: disconnected presentation, even if the BLE link has not formally closed.
- A fresh valid measurement immediately restores the healthy state.

### LED renderer

The renderer runs independently at a fixed frame interval, initially 20 ms/50 Hz. It must never wait for a BLE packet. It implements the searching red heartbeat, connection-confirmation green flash and live orange-red heartbeat described above. It consumes `bpm`, RR intervals, connection status and measurement age.

## Operational workflow

### Start of each session

1. Power the Plasma and LED strip.
2. Use Button A to select BLE heart-rate mode.
3. Plasma displays the strong red searching heartbeat.
4. Wear the Enduro snugly enough to obtain a heart-rate reading.
5. On the Enduro, press `START` and select **Virtual Run**.
6. Keep it close to the Plasma until the LEDs flash green.
7. Press `START` on the Enduro to begin the activity.
8. The LEDs change to orange-red and their brightness follows the heartbeat.

### End of session

1. Stop Virtual Run on the Enduro.
2. Save or discard the recorded activity.
3. Plasma detects stale data and returns to the strong red searching heartbeat.
4. It remains ready to reconnect when Virtual Run is opened again.

Avoid simultaneously connecting Zwift or another Virtual Run client, because the number of concurrent third-party BLE clients is not documented and should be assumed to be one.

## Diagnostics

Rate-limited USB serial diagnostics should record:

- firmware/application version;
- scan started/stopped;
- candidate name, address type, RSSI and advertised services;
- connection and discovery result;
- optional manufacturer/model/serial fields if available;
- notification count and last BPM;
- decode-error count;
- disconnect reason where exposed;
- reconnect/backoff state.

Do not print every animation frame or every raw packet during normal operation.

## Acceptance criteria

The implementation is ready for the two-night deployment when all of the following pass:

1. Button A can select BLE heart-rate mode from the board's available modes.
2. Entering BLE heart-rate mode displays a strong red synthetic heartbeat while disconnected.
3. Plasma connects after Virtual Run is opened.
4. Successful connection produces a clearly visible, brief green flash.
5. A plausible live BPM is received and exposed to the renderer.
6. The connected display is orange-red and its brightness pulses with RR timing where supplied, otherwise BPM-derived timing.
7. Stopping Virtual Run returns the display to the red searching heartbeat within 10 seconds.
8. Reopening Virtual Run reconnects without rebooting the Plasma.
9. Power-cycling the Plasma and reopening Virtual Run restores operation.
10. Power-cycling the Enduro does not permanently strand the Plasma on a cached address.
11. Leaving the watch absent for at least 15 minutes does not crash or exhaust memory.
12. Malformed or unexpected notification data does not stop reconnection or rendering.
13. LED rendering remains smooth while BLE reconnects.
14. Leaving BLE heart-rate mode stops its presentation and BLE session cleanly.

## Deliberate non-goals

- ANT+ support
- medical-grade beat timing
- long-term historical storage
- multi-watch support
- cryptographic watch identity
- permanent BLE bonding
- automatic starting of Virtual Run from the Plasma

## Open implementation checks

These are empirical integration checks for the developer, not reasons to change the architecture:

1. Exact advertised local name of the Enduro in Virtual Run.
2. Whether `0x180D` and `0x1814` appear in the advertisement or only after connection.
3. Whether Device Information characteristics are exposed.
4. Whether HR notifications begin on the Virtual Run waiting screen or only after the activity timer starts.
5. Exact RM2 Bluetooth initialisation required by the selected Pimoroni firmware build.
6. Whether the Enduro address remains stable across Virtual Run sessions and watch restarts. The software must work either way.

These findings should be logged during the first hardware run and used to tighten candidate scoring without changing the direct watch-to-board architecture.
