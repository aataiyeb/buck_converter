import csv
import matplotlib.pyplot as plt

t, target, vout = [], [], []
with open("loop_startup.csv") as f:
    for row in csv.DictReader(f):
        t.append(int(row["ms"]) / 1000)
        target.append(int(row["target_mV"]) / 1000)
        vout.append(int(row["vout_mV"]) / 1000)

steady = [v for tt, v in zip(t, vout) if tt > 1.5]
rise = next(tt for tt, v in zip(t, vout) if v >= 4.95)
print(f"reaches 4.95 V at {rise * 1000:.0f} ms")
print(f"steady state (t > 1.5 s): mean {sum(steady) / len(steady):.4f} V, "
      f"min {min(steady):.3f} V, max {max(steady):.3f} V")

fig, ax = plt.subplots()
ax.plot(t, target, "--", label="target")
ax.plot(t, vout, label="measured output")
ax.set_xlim(0, 0.3)
ax.set_xlabel("time (s)")
ax.set_ylabel("volts")
ax.legend()
ax.grid(True)
fig.savefig("loop_startup_zoom.png", dpi=150)
