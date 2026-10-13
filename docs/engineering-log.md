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
- Multimeter: VCC 12 V, VB 11.606 V, SD 3.245 V.
- The edges show ringing from the probe ground lead; not significant at this stage.