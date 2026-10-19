import sys, time, csv
import serial
import matplotlib.pyplot as plt

port = sys.argv[1]
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 4.0
rows, t0, last_ms = [], None, -1
deadline = time.time() + seconds + 30

with serial.Serial(port, 115200, timeout=1) as ser:
    ser.reset_input_buffer()
    while time.time() < deadline:
        parts = ser.readline().decode(errors="ignore").strip().split(",")
        if len(parts) != 4 or not all(p.lstrip("-").isdigit() for p in parts):
            continue
        ms, target, vout, duty = map(int, parts)
        if ms < last_ms:            # the Nucleo was reset: start again
            rows.clear(); t0 = None
        last_ms = ms
        if t0 is None:
            t0 = ms
        rows.append((ms - t0, target, vout, duty))
        if ms - t0 >= seconds * 1000:
            break

with open("loop_startup.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ms", "target_mV", "vout_mV", "duty_permille"])
    w.writerows(rows)

t = [r[0] / 1000 for r in rows]
fig, ax = plt.subplots()
ax.plot(t, [r[1] / 1000 for r in rows], "--", label="target")
ax.plot(t, [r[2] / 1000 for r in rows], label="measured output")
ax.set_xlabel("time (s)")
ax.set_ylabel("volts")
ax.legend()
ax.grid(True)
fig.savefig("loop_startup.png", dpi=150)
print(f"saved {len(rows)} samples")
