# Buck converter
1/10/2026 - Repo is set up and folder structure is done

Installed CubeIDE, LTspice and GitHub Desktop; Nucleo recognised as STLINK-V3

10/10/2026 - Completed parts inventory: IRLZ44N, IR2104, UF4007, power resistor, all caps and resistors present.

11/10/2026 - Built the LTspice simulation of the buck converter. 

Output settled at about 4.45V rather than 5V because of the diode drop. 

Output voltage ripple was about 16mV.The output overshoots at startup before it settles.

In CubeIDE, the project has to be opened from the STM32 folder that the CubeMX made, instead of the whole firmware folder. The build option on CubeIDE wasn't available because of it. And, I made a mistake while naming the pin name in main.c, and then I debugged it using the console.


Got the Nucleo-G474RE blinking its LED from my own code (first successful build and flash).