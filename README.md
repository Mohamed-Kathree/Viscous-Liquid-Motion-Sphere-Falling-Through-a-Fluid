# 🔴 Viscous Liquid Motion — Sphere Falling Through a Fluid

> A GlowScript/VPython simulation of a marble falling through a viscous fluid inside a test tube, modelling the interplay between gravity, buoyancy, and Stokes drag until the sphere reaches terminal velocity.

![VPython](https://img.shields.io/badge/VPython-GlowScript%202.7-5C2D91?style=flat-square&logo=python&logoColor=white)
![Physics](https://img.shields.io/badge/Topic-Viscosity%20%7C%20Fluid%20Dynamics-1B3A5C?style=flat-square)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square)

---

## Overview

A small marble (radius 7.5 mm, density 2728 kg/m³) is suspended at the top of a fluid-filled test tube and released from rest. As it falls, three vertical forces act on it simultaneously: its own weight pulling it down, a buoyant force pushing it up, and a velocity-dependent Stokes drag resisting its motion. The net force — and therefore the acceleration — decreases as the marble speeds up, until drag and buoyancy together balance gravity exactly. At this point the marble reaches **terminal velocity** and accelerates no further.

The simulation plots a velocity-time graph in real time, making the exponential approach to terminal velocity directly visible.

---

## Physics & Equations

### 1. Gravitational force (weight)

```
F_gravity = m × g
```

where `m = ρ_marble × V_marble` is the mass of the marble and `g = 9.8 m/s²`. Acts downward throughout the simulation.

---

### 2. Volume of the sphere

```
V_marble = (4/3) × π × r³
```

where `r = 0.0075 m`. Used to compute both the marble's mass and the volume of fluid displaced.

---

### 3. Buoyant force (Archimedes' principle)

```
F_buoyancy = ρ_fluid × V_marble × g
```

The fluid exerts an upward force on the marble equal to the weight of fluid displaced. Since `ρ_marble > ρ_fluid` (2728 > 1411 kg/m³), the marble is denser than the fluid and sinks — but buoyancy partially offsets gravity throughout the fall.

---

### 4. Stokes drag (viscous resistance)

For a sphere moving slowly through a viscous fluid at low Reynolds number, drag is given by **Stokes' Law**:

```
F_drag = 6π × η × r × v
```

where:

| Symbol | Quantity | Value |
|---|---|---|
| `η` | Dynamic viscosity of the fluid | 6 Pa·s |
| `r` | Radius of the marble | 0.0075 m |
| `v` | Instantaneous velocity of the marble | varies |

Key property: drag is **linear in velocity** — it grows proportionally as the marble speeds up, which is why acceleration decreases over time rather than remaining constant.

---

### 5. Net force and acceleration (Newton's second law)

Taking downward as positive:

```
F_net = F_gravity − F_buoyancy − F_drag
      = (m × g) − (ρ_fluid × V × g) − (6π × η × r × v)

a = F_net / m
```

As `v` increases, `F_drag` increases, `F_net` decreases, and `a` approaches zero.

---

### 6. Terminal velocity

Terminal velocity is reached when the net force equals zero — acceleration stops and the marble falls at constant speed:

```
F_gravity = F_buoyancy + F_drag

m × g = ρ_fluid × V × g  +  6π × η × r × v_terminal
```

Solving for `v_terminal`:

```
v_terminal = (F_gravity − F_buoyancy) / (6π × η × r)
           = (m × g − ρ_fluid × V × g) / (6π × η × r)
```

This is the **Stokes terminal velocity** formula — it depends on the size, density contrast, and fluid viscosity.

---

### 7. Numerical integration (Euler method)

The simulation advances in time steps of `h = 0.01 s`:

```
a(t)     = F_net(t) / m

v(t + h) = v(t) + a(t) × h
y(t + h) = y(t) − v(t + h) × h      (subtract: downward motion reduces y)
```

Drag is recomputed from the updated velocity at every step, so the feedback between speed and drag is captured correctly throughout the fall.

---

### 8. Stopping condition

The simulation runs while:

```
Marble.pos.y > 0
```

i.e. the marble has not yet reached the bottom of the test tube (`y = 0`).

---

## Methodology

```
1. Place marble at top of test tube: y = 0.13 m, v = 0
2. Compute constant forces: Fg (weight) and Fb (buoyancy)
3. Calculate theoretical terminal velocity from Stokes formula
4. Loop while y > 0:
   a. Compute Stokes drag:    F_drag = 6π × η × r × v
   b. Compute net force:      F_net  = Fg − Fb − F_drag
   c. Compute acceleration:   a      = F_net / m
   d. Update velocity:        v     += a × h
   e. Update position:        y     −= v × h
   f. Advance time:           t     += h
   g. Print drag, velocity at each step
   h. Plot velocity on graph
5. Print final velocity and elapsed time
```

---

## Outputs

| Output | Description |
|---|---|
| **Velocity-Time graph** | Shows exponential approach to terminal velocity |
| **Per-step console log** | Time, drag force, and instantaneous velocity at each step |
| **Final summary** | Total time elapsed, final velocity, theoretical terminal velocity |

---

## Parameters

| Parameter | Symbol | Value | Unit |
|---|---|---|---|
| Marble radius | `r` | 0.0075 | m |
| Marble density | `ρ_marble` | 2728 | kg/m³ |
| Fluid density | `ρ_fluid` | 1411 | kg/m³ |
| Dynamic viscosity | `η` | 6 | Pa·s |
| Gravitational acceleration | `g` | 9.8 | m/s² |
| Tube length | — | 0.13 | m |
| Time step | `h` | 0.01 | s |

---

## Running the simulation

1. Go to [glowscript.org](https://www.glowscript.org) and sign in
2. Create a new program and paste the source code
3. Click **Run** — the test tube and marble render in 3D; the velocity-time graph builds in real time
4. Watch the marble accelerate quickly at first, then level off as drag grows
5. The console logs drag and velocity at every step, and prints a final summary when the marble reaches the bottom

> No local installation required — GlowScript runs entirely in the browser.

---

## Physics context

This experiment is a computational version of the classic **falling sphere viscometer** — a standard laboratory method for measuring the viscosity of an unknown fluid. In a real experiment, you measure the terminal velocity of a sphere of known density and size, then rearrange the Stokes formula to solve for `η`. Here the process runs in reverse: given a known viscosity, the simulation predicts the terminal velocity and the time profile of the approach to it.

The velocity-time curve has the characteristic shape of `v(t) = v_terminal × (1 − e^(−t/τ))`, where the time constant `τ = m / (6π × η × r)` controls how quickly the marble reaches terminal velocity. A higher viscosity means a larger drag constant, a smaller terminal velocity, and a faster approach to it.

This is directly analogous to **charging a capacitor** through a resistor in an RC circuit — both systems approach their steady state exponentially, governed by a time constant that balances the driving force against a dissipative term proportional to the current state variable.

---

*Part of a series of physics and mathematical modelling simulations built in VPython.*
