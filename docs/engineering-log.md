# Buck converter
## 2026-10-1 - Repo is set up and folder structure is done

Installed CubeIDE, LTspice and GitHub Desktop; Nucleo recognised as STLINK-V3

## 2026-10-10 - Completed parts inventory: IRLZ44N, IR2104, UF4007, power resistor, all caps and resistors present.

## 2026-10-11 - Built the LTspice simulation of the buck converter. 

Output settled at about 4.45V rather than 5V because of the diode drop. 

Output voltage ripple was about 16mV. The output overshoots at startup before it settles.

In CubeIDE, the project has to be opened from the STM32 folder that the CubeMX made, instead of the whole firmware folder. The build option on CubeIDE wasn't available because of it. And, I made a mistake while naming the pin name in main.c, and then I debugged it using the console.


Got the Nucleo-G474RE blinking its LED from my own code (first successful build and flash).


(PWM)
Configured TIM1 channel 1 for PWM in CubeMX: prescaler 0, period 3399, pulse 1417, giving 50 kHz at 41.7% duty from the 170 MHz clock. Started the timer with `HAL_TIM_PWM_Start` in `main.c`. The LED blink still works alongside it. Checked at home with an LED and a 220 Ω resistor on D7: it glows steadily. Frequency and duty cycle still to be measured with an oscilloscope in the lab.

## 2026-10-12 (driver test)
- Built the IR2104 gate driver section on the breadboard with no MOSFETs fitted, Vs tied to ground for the test. Powered from the lab supply at 12 V with a 50 mA current limit; supply current was 3 mA.
- Oscilloscope (CH1 on IN, CH2 on HO): frequency 50.00 kHz, duty cycle 41.72 %, against 50 kHz and 41.7 % expected. HO swings to about 11.60 V, and its rising edge lags IN slightly, consistent with the datasheet propagation delay.
- Multimeter: VCC 12.001 V, SD 3.245 V, HO average 4.517 V, VB 11.606 V. Supply drew 3mA.
- The edges show ringing from the probe ground lead; not significant at this stage.

## 2026-10-14 (power stage)
- Moved VS from ground to the switching node and added Q1, Q2, the 220 uH inductor, the 220 uF output capacitor and the 10 ohm load. Q2's gate is tied to ground so its body diode acts as the freewheeling diode.
- A diode-mode reading of 0.01 V on SW before power-up turned out to be the load resistor connected through a second breadboard, a path of about 10 ohm, not a short.
- First power-up at 10 V with a 0.5 A limit: 0.149 A, constant voltage. Then 12 V.
- At 12 V: output 4.3253 V on the multimeter, input current 0.183 A, load 10.11 ohm. Output power 1.850 W, input power 2.196 W, efficiency 84.3 %.
- SW: 12.00 V high, -0.600 V low, 50.09 kHz, 40.11 % duty, against 41.7 % set in firmware. Output is below the simulation's 4.45 V because the real pulse is shorter.
- The oscilloscope's automatic readings jumped between frames because of ringing on the edges, so I froze a frame with Run/Stop where they were stable.
- Open-loop output is about 0.7 V short of 5 V. The next stage closes the loop.

## 2026-10-19 (closed loop)
- Added a voltage divider (10 kΩ and 5.1 kΩ) and a 100 nF capacitor from OUT to the Nucleo's A0 (PA0, ADC1 channel 1). Divider ratio 5.1 / 15.1 = 0.3377.
- Configured ADC1 in CubeMX: 12-bit, software trigger, 92.5-cycle sampling, synchronous clock divided by 4.
- Wrote a 1 kHz PI controller in main.c: Kp 0.002, Ki 10, duty limited to 55 %, target soft-started over 100 ms, and a latching shutdown above 5.8 V. Serial output logs time, target, measured and duty every 5 ms.
- The first flash didn't take: the serial window stayed blank and the LED still blinked fast. Flashing again fixed it.
- At 12.00 V in with the 10.11 ohm load: output 4.9878 V on the multimeter against a 5.000 V target (0.24 % low), duty 47.2 %, supply current 0.218 A. The Nucleo's own reading averaged about 4.99 V, so the divider ratio needed no correction.
- Startup captured over serial: the output follows the ramp and reaches 5 V in about 0.1 s with no visible overshoot.
- Efficiency from the supply display came out between 92 and 94 % depending on which current reading I use (0.223 A or 0.218 A at 12 V). The duty cycle predicts an input current of about 0.23 A, which supports the higher reading, so I quote about 92 %. The synchronous stage will measure input current with the multimeter.
- Line-regulation test at 11, 12, 13 and 14 V input with the 10.11 ohm load: output 4.9925, 4.9878, 4.9851 and 4.9880 V, a 7.4 mV spread or about 2.5 mV per volt of input, with the duty cycle falling from 51.3 % to 40.7 % to compensate.
- Input current at 12, 13 and 14 V gives 92.0, 92.2 and 92.5 % efficiency. The 11 V reading (0.293 A, 76 %) looks wrong and needs re-measuring; I don't know why it is off.

## (synchronous stage)
- Switched to synchronous rectification: removed the wire tying Q2's gate to ground, drove it from the IR2104's LO pin through 10 ohm, and added a 10 kohm pull-down on the gate.
- Moved the IR2104's shutdown pin from the Nucleo's 3V3 to D8 (PA9, label SD_EN) with a 10 kohm pull-down, so the driver is off through reset and trips. Reason: with LO driving Q2, "no PWM" turns Q2 fully on, which would short the inductor across a charged output capacitor. A simple model predicted a reverse current of about 3.6 A in that case.
- Pre-power continuity check: Q2's gate row read about 20 ohm to ground instead of 10 kohm. The 10 ohm LO resistor was in pin 6's row (the switching node) instead of pin 5's row, which put it in series with the inductor and the 10 ohm load (about 10 + 0.2 + 10.1 ohm). Moving it to pin 5 fixed the reading. Powered up like that, Q2's gate would have been tied to the switching node and caused shoot-through.
- Pin 3 read about 5.4 kohm to ground instead of 10 kohm with the D8 wire in. I attribute this to the Nucleo's input circuitry in parallel with the pull-down, but I did not confirm it by lifting the D8 wire. The driver enabled and the converter regulated normally.
- First power-up gave no output because I had not plugged in the D7 PWM wire. After fixing it the converter regulated.
- Buck 3 at 11.99 V: output 4.9740 V on the multimeter, supply current 0.212 A, duty 43.9 % (47.2 % with the body diode), efficiency about 96 % (output 2.447 W, input 2.542 W, load 10.11 ohm).
- The model predicted duty 44.3 %, 12 mA less input current and about 5 points more efficiency. The duty cycle fell more than predicted. The efficiency gain is 2 to 4 points depending on which Buck 2 current reading is used, because the supply's current display wanders by several mA.
- Did not do a back-to-back Buck 2 comparison in this session, did not measure input current with the multimeter, and did not test pressing RESET while regulating.
- The output sits 0.5 % under target on the multimeter with a flat duty cycle, which an integral controller should not allow. Cause not found.