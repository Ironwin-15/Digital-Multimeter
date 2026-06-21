# Smart Multimeter Simulation

A software simulation of an industry-grade digital multimeter capable of measuring **Resistance (R), Capacitance (C), and Inductance (L)** over a dynamic range of (10^5). The simulator incorporates realistic noise models, automatic range selection with hysteresis, and OTG serial packet generation.

Resistance measurement is implemented using a **voltage-divider method** with automatic range selection, while capacitance and inductance measurements are based on **RC time constant** and **LC resonance** respectively. Gaussian noise is added to simulate practical measurement imperfections.

The auto-ranging engine automatically selects the most suitable range and uses hysteresis to avoid oscillations. The achieved average resistance measurement error is **0.50%**, significantly improving over a fixed-range implementation.


---

# Part 2 — How to Set It Up

Clone the repository and install dependencies:

```bash
git clone https://github.com/Ironwin-15/Digital-Multimeter.git

cd Digital-Multimeter

pip install -r requirements.txt
```

---

# Part 3 — How to Run the Simulation

Run:

```bash
python simulate.py
```

The script performs a 50-point logarithmic sweep over all measurement ranges. It simulates noisy measurements, performs auto-ranging, computes measurement errors, and generates the required plots inside the `results/` directory.

---

# Part 4 — Results

| Method                       | R Error | C Error | L Error |
| ---------------------------- | ------- | ------- | ------- |
| Fixed-range (no auto)        | 9.1%  | 0.43%   | 0.63%   |
| Your auto-ranging simulation | 0.50%   | 0.43%   | 0.63%   |

Lower percentage error indicates better measurement accuracy.

---

# Measurement Equations

## Resistance Measurement

Voltage divider:

$$
V_x=\frac{R_x}{R_x+R_f}V_f
$$

$$
R_x=\frac{R_fV_x}{V_f-V_x}
$$

---

## Capacitance Measurement

RC charging:

$$
\tau=RC
$$

At 63.2% charging,

$$
C=\frac{t}{R}
$$

---

## Inductance Measurement

LC resonance:

$$
f=\frac{1}{2\pi\sqrt{LC}}
$$

Hence,

$$
L=\frac{1}{(2\pi f)^2C_{ref}}
$$

---

# Error Analysis

## Resistance Error

From

$$
R_x=\frac{R_fV_x}{V_f-V_x}
$$

relative error becomes

$$\frac{\Delta R_x}{R_x}=\frac{V_fR_f}{V_x(V_f-V_x)}\Delta V_x$$

Substituting the divider relation gives

$$\frac{\Delta R_x}{R_x}=\frac{(R_x+R_f)^2}{R_xR_fV_f}\Delta V_x$$

Minimum error occurs when

$$
\boxed{R_f=R_x}
$$

which forms the basis of auto-ranging.

---

## Capacitance Error

Since

$$
C=\frac{t}{R}
$$
Hence, 
$$
\boxed{
\frac{\Delta C}{C}=\frac{\Delta t}{t}=\frac{\Delta t}{RC}
}$$

In this case, we dont require Auto ranging, since its an already decreasing function in R, hence can choose a very high R to reduce error.

---

## Inductance Error

Since

$$
L=\frac1{(2\pi f)^2C}
$$

$$
\boxed{
\frac{\Delta L}{L}
=2\frac{\Delta f}{f}=4\pi\Delta f\sqrt{LC_{ref}}
}
$$

Even in this case, we dont require Auto ranging, since its an increasing function in C, hence can choose a very high C to reduce error.

---

# Auto-Ranging Algorithm

Five ranges are implemented:

| Range | Maximum Value |
| ----- | ------------- |
| 1     | 100 Ω         |
| 2     | 1 kΩ          |
| 3     | 10 kΩ         |
| 4     | 100 kΩ        |
| 5     | 1 MΩ          |

### Step-Up Rule

If measured value exceeds 90% of the current range, increment the up-counter.

### Step-Down Rule

If measured value falls below 10% of the current range, increment the down-counter.

### Hysteresis

Three consecutive triggers are required before switching range.

### Overload Protection

Measurements beyond 1 MΩ return:

```text
OL
```

---

# OTG Packet Format

Example:

```json
{
  "timestamp": 1710000000,
  "mode": "Resistance",
  "reading": 4701.2,
  "unit": "Ohm",
  "range_state": 3
}
```

---

# Conclusion

This project demonstrates a complete software implementation of an auto-ranging digital multimeter. The system uses physical measurement principles, realistic noise models, and adaptive range selection to achieve accurate measurements across a dynamic range of five decades while emulating the operating principles of commercial digital multimeters.
