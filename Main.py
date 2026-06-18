GlowScript 2.7 VPython

# =============================================================================
# Viscous Liquid Motion — Sphere Falling Through a Fluid
# Models a marble falling through a viscous fluid inside a test tube,
# with forces: gravity, buoyancy, and Stokes drag.
# Terminal velocity is reached when Fnet → 0.
# =============================================================================


# ── Scene Objects ─────────────────────────────────────────────────────────────

Marble = sphere(
    pos    = vector(0, 0.13, 0),
    radius = 0.0075,
    color  = color.red
)

Test_tube = cylinder(
    pos     = vector(0, 0, 0),
    axis    = vector(0, 0.13, 0),
    radius  = 0.0125,
    color   = color.white,
    opacity = 0.2
)


# ── Graph Setup ───────────────────────────────────────────────────────────────

Velocity_Graph = graph(
    title  = 'Velocity-Time Graph',
    xtitle = 'Time (s)',
    ytitle = 'Velocity (m/s)'
)

Velocity_Curve = gcurve(color=color.blue)


# ── Physical Constants & Parameters ───────────────────────────────────────────

Density_Marble = 2728       # Marble density         (kg/m³)
Density_Fluid  = 1411       # Fluid density          (kg/m³)
Viscosity      = 6          # Dynamic viscosity      (Pa·s)
g              = 9.8        # Gravitational accel.   (m/s²)
h              = 0.01       # Time step              (s)


# ── Derived Quantities ────────────────────────────────────────────────────────

Volume_Marble = (4/3) * pi * Marble.radius**3   # Sphere volume   (m³)
Mass_Marble   = Density_Marble * Volume_Marble   # Marble mass     (kg)

Fg = Mass_Marble * g                             # Weight          (N)
Fb = Density_Fluid * Volume_Marble * g           # Buoyant force   (N)


# ── Initial Conditions ────────────────────────────────────────────────────────

V0   = 0      # Initial velocity  (m/s) — marble starts at rest
Time = 0      # Simulation clock  (s)


# ── Theoretical Terminal Velocity ─────────────────────────────────────────────
# At terminal velocity, Fnet = 0:  Fg = Fb + Drag
# Stokes drag: F_drag = 6πηrv  →  v_terminal = (Fg − Fb) / (6πηr)

V_terminal = (Fg - Fb) / (6 * pi * Viscosity * Marble.radius)
print(f"Theoretical terminal velocity: {V_terminal:.4f} m/s")


# ── Simulation Loop ───────────────────────────────────────────────────────────
# Runs while the marble is still inside the test tube (y > 0)

while Marble.pos.y > 0:

    rate(100)

    # Stokes drag — opposes downward motion (acts upward)
    Drag = 6 * pi * Viscosity * Marble.radius * V0

    # Net downward force: weight − buoyancy − drag
    Fnet         = Fg - Fb - Drag
    Acceleration = Fnet / Mass_Marble

    # Euler integration
    Vn            = V0 + Acceleration * h
    Marble.pos.y  = Marble.pos.y - Vn * h   # Subtract: downward motion reduces y

    # Advance time and update velocity
    Time += h
    V0    = Vn

    # Log drag force each step
    print(f"Time: {Time:.2f} s  |  Drag: {Drag:.6f} N  |  Velocity: {Vn:.4f} m/s")

    # Plot velocity against time
    Velocity_Curve.plot(Time, Vn)


# ── Results ───────────────────────────────────────────────────────────────────

print(f"\n--- Simulation complete ---")
print(f"Time elapsed:      {Time:.2f} s")
print(f"Final velocity:    {Vn:.4f} m/s")
print(f"Terminal velocity: {V_terminal:.4f} m/s")
