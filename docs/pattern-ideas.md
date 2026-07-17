# Pattern Ideas

Use the number below when you want one built. Patterns are intended to work
with the configured physical segments and the existing global brightness
control.

1. **Rainbow sweep** - A continuous rainbow moves along the full installation. Implemented as `rainbow_sweep`.
2. **Breathing color** - One chosen color slowly brightens and dims. Implemented as `breathing_color`; its hue also changes over time.
3. **Meteor shower** - Random comets appear, cross a segment, and fade out. Implemented as `meteor_shower`.
4. **Twinkle field** - Independent, soft white or colored sparkles fade in and out. Implemented as `twinkle_field`.
5. **Fire** - Orange, red, and yellow flicker rises from each segment start.
6. **Police pulse** - Alternating red and blue flashes with a short dark gap.
7. **Color wipe** - A solid color progressively fills the LEDs, then changes. Implemented as `color_wipe`.
8. **Theater chase** - Spaced lights chase around each physical segment. Implemented as `theater_chase`.
9. **Larson scanner** - A bright scanner bar bounces end-to-end with a fading tail. Implemented as `larson_scanner`.
10. **Ocean waves** - Layered blue and teal bands drift at different speeds.
11. **Aurora** - Slow, blended green, cyan, and violet ribbons move across the strip. Implemented as `aurora`.
12. **Candy cane** - Red and white stripes rotate around the segments.
13. **Pulse train** - Short light packets travel from segment 1 through segment 4. Implemented as `pulse_train`.
14. **Confetti** - Brief random colored pixels pop and fade against black. Implemented as `confetti`.
15. **Gradient drift** - A smooth two-color gradient slides continuously along the LEDs.
16. **Clockwise relay** - One segment lights at a time in a repeating four-step relay.
17. **Lightning** - Rare white flashes with quick blue afterglow.
18. **Palette comet** - Comets use a constrained theme palette, such as autumn or ice.
19. **Sound-reactive bars** - An optional microphone input drives colored level bars. Not implemented: Plasma 2350 W has no onboard microphone. It can be added once an external analog or I2C microphone is connected.
20. **Status beacon** - A calm idle pattern that changes color for Wi-Fi or controller state.

## Diagnostic Pattern

`diagnostic_blocks` is the LED-counting pattern. It paints LEDs in consecutive
groups of 10, each group with a distinct color:

| LEDs | Color |
| --- | --- |
| 0-9 | red |
| 10-19 | green |
| 20-29 | blue |
| 30-39 | yellow |
| 40-49 | magenta |
| 50-59 | cyan |
| 60-69 | orange |
| 70-79 | violet |
| 80-89 | white |
| 90-99 | light blue |

If the actual strip ends part way through a color block, count the lit LEDs in
that final block and add them to the completed 10-LED blocks before it. For
example, seven light-blue LEDs after nine full blocks means $90 + 7 = 97$ LEDs.

To run it temporarily, set this in `device/config.py`, upload, and observe the
result:

```python
DEFAULT_PATTERN = "diagnostic_blocks"
```

Restore `DEFAULT_PATTERN = "comet"` after counting.