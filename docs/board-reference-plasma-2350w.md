# Plasma 2350 W Reference

## Board Summary

- MCU: RP2350A
- Wireless: RM2 (CYW43439) Wi-Fi/Bluetooth
- LED support: WS2812/NeoPixel/SK6812 and APA102/DotStar
- Power/programming: USB-C
- Controls: BOOT button, RST button, user button, onboard RGB LED

## Official Resources

- Plasma repo: https://github.com/pimoroni/plasma
- Product page: https://shop.pimoroni.com/products/plasma-2350-w
- Latest firmware: https://github.com/pimoroni/plasma/releases/latest
- Pinout PDF: https://cdn.shopify.com/s/files/1/0174/1800/files/plasma2350_pinout_diagram.pdf
- Schematic PDF: https://cdn.shopify.com/s/files/1/0174/1800/files/Pimoroni_Plasma_2350_W_Schematic.pdf

## Firmware Notes

- To flash firmware: hold BOOT, tap RST, copy UF2 to the `RP2350` drive.
- Use the board-specific Plasma 2350 W UF2.
- `-with-filesystem` builds overwrite board files.

## Wi-Fi Credentials File

Most Pimoroni examples expect a file named `secrets.py` on the board root:

```python
WIFI_SSID = "your-ssid"
WIFI_PASSWORD = "your-password"
```

Filename and variable names must match exactly.

## Typical LED Connection

- LED strip 5V -> board 5V terminal
- LED strip GND -> board GND terminal
- LED data -> board LED data terminal/pin per board docs

Always share a common ground between board and LEDs.
