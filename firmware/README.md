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