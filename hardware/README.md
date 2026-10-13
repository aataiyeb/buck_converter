# Hardware

![Parts inventory](images/parts-inventory.jpg)

Breadboard build of the buck converter, built and tested in stages.

## Stage 4B: gate driver test (IR2104, no MOSFETs fitted)

The IR2104 was tested on its own first. Its switch pin (VS, pin 6) was tied to
ground, so the high-side output (HO) could be measured with an ordinary
oscilloscope probe. Powered from a Keithley 2231A-30-3 bench supply at 12 V;
the Nucleo-G474RE ran the 50 kHz PWM firmware over USB.

### Wiring

| Connect | To |
|---|---|
| IR2104 pin 1 (VCC) | +12V |
| 0.1 µF ceramic | pin 1 to pin 4 |
| Pin 4 (COM) | GND |
| Pin 2 (IN) | Nucleo D7 (PWM) |
| Pin 3 (SD) | Nucleo 3V3 (active-low shutdown, held high) |
| Pin 5 (LO) | not connected |
| Pin 6 (VS) | GND (temporary, for this test) |
| UF4007 | anode to pin 1, cathode (stripe) to pin 8 |
| 1 µF ceramic | pin 8 to pin 6 |
| Pin 7 (HO) | probe point |
| Nucleo GND | GND |

![Test setup](images/driver-setup.jpg)

The test setup: IR2104 on the breadboard, Nucleo on the left, oscilloscope
probes on pin 2 (channel 1) and pin 7 (channel 2).

### Results

| Measurement | Result | Expected |
|---|---|---|
| Supply | 12.00 V, 3 mA | 12 V, a few mA |
| VCC (pin 1) | 12.001 V | about 12 V |
| SD (pin 3) | 3.245 V | about 3.3 V (threshold is 3 V) |
| VB (pin 8) | 11.606 V | VCC minus the diode drop |
| HO average (pin 7, multimeter) | 4.517 V | duty cycle x high level |
| IN (pin 2) | 3.36 V, 50.14 kHz, 41.72 % duty | 3.3 V, 50 kHz, 41.7 % |
| HO (pin 7) | 11.60 V, 50.19 kHz, 38.94 % duty | about 11.6 V, 50 kHz, slightly under 41.7 % |

![IN and HO on the oscilloscope](images/driver-scope.jpg)

Oscilloscope: channel 1 (yellow) is the PWM input on pin 2, channel 2 (cyan)
is the gate-drive output on pin 7. HO follows IN with the same period.

![Bench supply](images/driver-supply.jpg)

Bench supply: channel 1 in constant-voltage mode at 12.00 V, drawing 3 mA.
Channels 2 and 3 are unused.

![VCC](images/meter-vcc.jpg)

Pin 1 (VCC): 12.001 V.

![SD](images/meter-sd.jpg)

Pin 3 (SD): 3.245 V.

![HO average](images/meter-ho.jpg)

Pin 7 (HO), average: 4.517 V.

![VB](images/meter-vb.jpg)

Pin 8 (VB): 11.606 V.

### What the measurements show

- The bootstrap circuit works. HO reaches 11.60 V on the scope, matching the
  11.606 V on VB measured with the multimeter. VB sits about 0.4 V below VCC,
  the forward drop of the UF4007 at this tiny current.
- HO follows IN at the same frequency, but its pulse is about 2.8 points
  narrower (38.94 % against 41.72 %), roughly 0.55 µs of the 20 µs period.
  This is the IR2104's propagation delay: it turns on more slowly than it
  turns off, which trims a little off every pulse. The multimeter agrees:
  11.60 V x 38.94 % = 4.517 V.
- That lost pulse width will pull the output of the open-loop converter slightly
  below the calculated value. The PI controller will compensate for it later.
- The frequency readings (50.14 and 50.19 kHz) are within the scope's
  resolution at 10 µs per division of the 50.000 kHz the timer produces.
- SD sits at 3.245 V, above the 3 V threshold but without much margin.
- The spikes on each edge come from the probe's ground lead and are not
  significant at this stage.