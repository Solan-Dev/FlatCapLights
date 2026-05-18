# HatLights HTTP Controller API

## Wi-Fi Access Point

The board can boot as its own Wi-Fi network:
- SSID: `YorkshireHat`
- Password: `pie12345`

## Endpoints

### `/status`
**GET request** – Returns current state as JSON.

**Example:**
```
http://<hatlight-ip>/status
```

**Response:**
```json
{
  "effect_mode": "segment_parallel_chase",
  "brightness_percent": 75,
  "led_enabled": true,
  "available_effects": ["comet_chase", "segment_parallel_chase"]
}
```

### `/set`
**GET request** – Update settings. Returns updated state as JSON.

**Parameters (all optional):**
- `effect=<mode>` – Change effect mode (e.g., `comet_chase`, `segment_parallel_chase`)
- `brightness=<0-100>` – Set brightness percentage (0-100)
- `power=<on|off>` – Turn LEDs on or off (accepts: `on`, `off`, `1`, `0`, `true`, `false`)

**Examples:**

Change effect to comet_chase:
```
http://<hatlight-ip>/set?effect=comet_chase
```

Set brightness to 50%:
```
http://<hatlight-ip>/set?brightness=50
```

Turn LEDs off:
```
http://<hatlight-ip>/set?power=off
```

Combine multiple:
```
http://<hatlight-ip>/set?effect=segment_parallel_chase&brightness=80&power=on
```

**Response:**
Same as `/status` with updated values.

## Controller Device Example (MicroPython)

```python
import urequests
import json

# Find your HatLights board IP
HATLIGHT_IP = "192.168.x.x"  # Replace with actual IP

def get_status():
    """Query current state."""
    response = urequests.get(f"http://{HATLIGHT_IP}/status")
    data = response.json()
    response.close()
    return data

def set_effect(effect_name):
    """Change effect."""
    urequests.get(f"http://{HATLIGHT_IP}/set?effect={effect_name}").close()

def set_brightness(percent):
    """Set brightness 0-100."""
    urequests.get(f"http://{HATLIGHT_IP}/set?brightness={percent}").close()

def toggle_power(enabled):
    """Turn LEDs on/off."""
    power = "on" if enabled else "off"
    urequests.get(f"http://{HATLIGHT_IP}/set?power={power}").close()

# Example usage:
status = get_status()
print("Current:", status)

set_effect("comet_chase")
set_brightness(75)
toggle_power(True)
```

## Finding Your IP Address

If your HatLights board connects to WiFi, you can find it via:

1. **Router admin page** – Look for connected device
2. **Network scanner** – Use `nmap` or similar to scan your subnet
3. **Serial console** – Connect via USB and watch boot logs for IP address

**Temporary workaround for dynamic IP:** Assign a static IP in your router DHCP settings using the board's MAC address.

## Debugging

To test endpoints from your PC:
```bash
# Get status
curl http://<hatlight-ip>/status

# Set brightness
curl "http://<hatlight-ip>/set?brightness=50"

# Query available effects
curl http://<hatlight-ip>/status | grep available_effects
```
