# Firmware

Firmware for the buck converter, running on an STM32G474 (Nucleo-G474RE).
The project is generated with STM32CubeMX, and the application code is
written by hand inside the `USER CODE` sections of `main.c`.
The CubeIDE project lives in `buck-firmware/`.

## Status

- [x] LED blink (confirms the toolchain, build and flash all work)
- [ ] 50 kHz PWM output on TIM1
- [ ] ADC reading of the output voltage
- [ ] PI controller

## LED blink

The green LED toggles every 100 ms from the main loop.

```c
HAL_GPIO_TogglePin(LED2_GPIO_PORT, LED2_PIN);
HAL_Delay(100);
```

Video: [blink.MOV](images/blink.MOV)

![Successful build](images/build-success.png)

Console output of a successful build.

## 50 kHz PWM output

TIM1 channel 1 outputs the switching signal on PA8 (D7). The timer runs from
the 170 MHz clock with no prescaler, so the numbers set the frequency and duty:

| Setting | Value | Result |
| Counter period | 3399 | 170 MHz / 3400 = 50 kHz |
| Pulse | 1417 | 1417 / 3400 = 41.7 % duty |

The timer is started once from `main.c`; after that the hardware generates
the waveform on its own.

```c
HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
```

![CubeMX pinout](images/cubemx-pinout.png)

PA8 configured as TIM1_CH1.

![TIM1 settings](images/tim1-settings.png)

### Measured on the oscilloscope

D7 measured 50.14 kHz at 41.72 % duty with a 3.36 V amplitude, against 50 kHz, 41.7 % and 3.3 V calculated.

![D7 and HO on the oscilloscope](../hardware/images/driver-scope.jpg)

Channel 1 (yellow) is D7, measured at the IR2104's input pin. Channel 2 is the driver's output, covered in the hardware README.