import csv
import matplotlib.pyplot as plt

vin = [11, 12, 13, 14]
vout = [4.9925, 4.9878, 4.9851, 4.9880]
iin = [0.293, 0.223, 0.205, 0.190]
duty = [51.3, 47.3, 43.8, 40.7]

with open("line_regulation.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["vin_V", "vout_V", "iin_A", "duty_percent"])
    w.writerows(zip(vin, vout, iin, duty))

fig, (a1, a2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6))
a1.plot(vin, vout, "o-")
a1.axhline(5.0, linestyle="--")
a1.set_ylim(4.9, 5.1)
a1.set_ylabel("output (V)")
a1.grid(True)
a2.plot(vin, duty, "o-", color="tab:orange")
a2.set_ylabel("duty cycle (%)")
a2.set_xlabel("input voltage (V)")
a2.grid(True)
fig.suptitle("Line regulation, 10.11 ohm load")
fig.savefig("line_regulation.png", dpi=150)