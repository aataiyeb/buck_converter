# Buck converter
1/10/2026 - Repo is set up and folder structure is done

Installed CubeIDE, LTspice and GitHub Desktop; Nucleo recognised as STLINK-V3

10/10/2026 - Completed parts inventory: IRLZ44N, IR2104, UF4007, power resistor, all caps and resistors present.

11/10/2026 - Built the LTspice simulation of the buck converter. 

Output settled at about 4.45V rather than 5V because of the diode drop. 

Output voltage ripple was about 16mV.The output overshoots at startup before it settles.

In CubeIDE, the project has to be opened from the STM32 folder that the CubeMX made, instead of the whole firmware folder. The build option on CubeIDE wasn't available because of it. And, I made a mistake while naming the pin name in main.c, and then I debugged it using the console.


Got the Nucleo-G474RE blinking its LED from my own code (first successful build and flash).


(PWM)
Configured TIM1 channel 1 for PWM in CubeMX: prescaler 0, period 3399, pulse 1417, giving 50 kHz at 41.7% duty from the 170 MHz clock. Started the timer with `HAL_TIM_PWM_Start` in `main.c`. The LED blink still works alongside it. Checked at home with an LED and a 220 Ω resistor on D7: it glows steadily. Frequency and duty cycle still to be measured with an oscilloscope in the lab.

12/10/2026 (driver test)
- Built the IR2104 gate driver section on the breadboard with no MOSFETs fitted, Vs tied to ground for the test. Powered from the lab supply at 12 V with a 50 mA current limit; supply current was 0.003 mA.
- Oscilloscope (CH1 on IN, CH2 on HO): frequency 50.00 kHz, duty cycle 41.72 %, against 50 kHz and 41.7 % expected. HO swings to about 11.60 V, and its rising edge lags IN slightly, consistent with the datasheet propagation delay.
- Multimeter: VCC 12.001 V, SD 3.245 V, HO average 4.517 V, VB 11.606 V. Supply drew 3mA.
- The edges show ringing from the probe ground lead; not significant at this stage.

14/10/2026 (power stage)
- Moved VS from ground to the switching node and added Q1, Q2, the 220 uH inductor, the 220 uF output capacitor and the 10 ohm load. Q2's gate is tied to ground so its body diode acts as the freewheeling diode.
- A diode-mode reading of 0.01 V on SW before power-up turned out to be the load resistor connected through a second breadboard, a path of about 10 ohm, not a short.
- First power-up at 10 V with a 0.5 A limit: 0.149 A, constant voltage. Then 12 V.
- At 12 V: output 4.3253 V on the multimeter, input current 0.183 A, load 10.11 ohm. Output power 1.850 W, input power 2.196 W, efficiency 84.3 %.
- SW: 12.00 V high, -0.600 V low, 50.09 kHz, 40.11 % duty, against 41.7 % set in firmware. Output is below the simulation's 4.45 V because the real pulse is shorter.
- The oscilloscope's automatic readings jumped between frames because of ringing on the edges, so I froze a frame with Run/Stop where they were stable.
- Open-loop output is about 0.7 V short of 5 V. The next stage closes the loop.

19/10/2026 (closed loop)
- Added a voltage divider (10 kΩ and 5.1 kΩ) and a 100 nF capacitor from OUT to the Nucleo's A0 (PA0, ADC1 channel 1). Divider ratio 5.1 / 15.1 = 0.3377.
- Configured ADC1 in CubeMX: 12-bit, software trigger, 92.5-cycle sampling, synchronous clock divided by 4.
- Wrote a 1 kHz PI controller in main.c: Kp 0.002, Ki 10, duty limited to 55 %, target soft-started over 100 ms, and a latching shutdown above 5.8 V. Serial output logs time, target, measured and duty every 5 ms.
- The first flash didn't take: the serial window stayed blank and the LED still blinked fast. Flashing again fixed it.
- At 12.00 V in with the 10.11 ohm load: output 4.9878 V on the multimeter against a 5.000 V target (0.24 % low), duty 47.2 %, supply current 0.218 A. The Nucleo's own reading averaged about 4.99 V, so the divider ratio needed no correction.
- Startup captured over serial: the output follows the ramp and reaches 5 V in about 0.1 s with no visible overshoot.
- Efficiency from the supply display came out between 92 and 94 % depending on which current reading I use (0.223 A or 0.218 A at 12 V). The duty cycle predicts an input current of about 0.23 A, which supports the higher reading, so I quote about 92 %. The synchronous stage will measure input current with the multimeter.
- Line-regulation test at 11, 12, 13 and 14 V input with the 10.11 ohm load: output 4.9925, 4.9878, 4.9851 and 4.9880 V, a 7.4 mV spread or about 2.5 mV per volt of input, with the duty cycle falling from 51.3 % to 40.7 % to compensate.
- Input current at 12, 13 and 14 V gives 92.0, 92.2 and 92.5 % efficiency. The 11 V reading (0.293 A, 76 %) looks wrong and needs re-measuring; I don't know why it is off.