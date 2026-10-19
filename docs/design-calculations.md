# Design calculations

## Specification

Vin = 12 V, target Vout = 5 V, load 10 Ω (measured 10.11 Ω), switching frequency
50 kHz, L = 220 µH, output capacitor 220 µF, input capacitor 470 µF. I chose
50 kHz as a compromise: a higher frequency allows a smaller inductor and capacitor
but wastes more energy in switching and is harder to keep clean on a breadboard.

## Results

| Quantity | Formula | Value |
|---|---|---|
| Duty cycle | D = Vout / Vin | 0.417 (41.7 %) |
| Output current | I = Vout / R | 0.5 A |
| Output power | P = Vout x I | 2.5 W |
| Inductor ripple current | ΔI = (Vin - Vout) x D / (L x f) | 0.27 A peak to peak |
| Peak inductor current | I + ΔI/2 | 0.63 A (the inductor is rated 1 A) |
| Minimum inductor current | I - ΔI/2 | 0.37 A, so continuous conduction |
| Output ripple (ideal capacitor) | ΔV = ΔI / (8 x f x C) | about 3 mV |
| Feedback divider | Vout x R2 / (R1 + R2) | 5 V gives 1.69 V with 10 kΩ and 5.1 kΩ |
| Critical inductance | L_crit = (Vin - Vout) x D x T / (2 x I) | about 58 µH |

220 µH is nearly four times the critical inductance, so the converter stays in
continuous conduction down to a load current of about 0.13 A (a load of about 38 Ω).

## Where the formulas come from

- Vout = D x Vin comes from volt-second balance. In steady state the inductor
  current ends each cycle where it started, so (Vin - Vout) x D x T = Vout x (1 - D) x T.
- ΔI comes from the inductor law V = L x di/dt, with V = Vin - Vout across the
  inductor for a time D/f.
- ΔV comes from the charge in the part of the current triangle above its
  average: a triangle of base T/2 and height ΔI/2, which is ΔI / (8f), divided by C.

## Against simulation and measurement

The simulation gave 4.45 V open loop, with about 16 mV ripple. The breadboard gave
4.325 V. The ideal formulas ignore the diode drop, the inductor's winding
resistance, the capacitor's series resistance and the driver's turn-on delay, which
shortens each pulse (the duty cycle at the switching node measured about 40 %
against the 41.7 % set in firmware). Output ripple was not measured.