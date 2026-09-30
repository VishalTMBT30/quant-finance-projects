"""
Hull-White One-Factor Short Rate Model — Indian Overnight MIBOR
=================================================================
Standard form :  dr(t) = [theta(t) - a*r(t)] dt + sigma * dW(t)
Equivalent form (used here, numerically identical, easier to calibrate
and interpret from a single historical short-rate series):
                 dr(t) = a*[phi(t) - r(t)] dt + sigma * dW(t) ,   phi(t) = theta(t)/a

phi(t) is the instantaneous target level the rate is being pulled towards at
time t (exactly like Vasicek's constant "b", except it is allowed to move
over time). This is the piece that is genuinely different from Vasicek: b is
one fixed number for all T, phi(t) is a function of time.

Everything below is written from scratch using only numpy / pandas / matplotlib
(no calibration libraries, no scipy). It mirrors, step by step, the calculation
performed in HullWhite_MIBOR_Calculation.xlsx.

Pipeline
--------
1. Load 2 years of daily Indian Overnight MIBOR data.
2. Calibrate the mean-reversion speed (a / kappa) and volatility (sigma) with
   an OLS regression on  delta_r(t) = a_reg + b*r(t-1)  [Vasicek-style step,
   because this is exactly how the constant part of Hull-White is estimated
   from a single historical short-rate series].
3. Back out a time-varying theta(t) from the discretised SDE at every
   historical date, smooth it (60-day rolling mean), then fit a linear trend
   to the FULL 2-year window of phi(t) so we can extrapolate it forward
   (consistent with the same 2-year window used for kappa and sigma).
   -> This time-varying theta(t) is the one thing that is NOT present in the
      Vasicek model (Vasicek uses a single constant long-run mean, b).
4. Forecast E[r(T)] for T = 3.5, 4.5, 5.5 years with the closed-form solution
   of the Hull-White SDE for a linear theta(t).
5. Run a Monte Carlo simulation (Euler-Maruyama) of the full SDE to visualise
   the spread of possible future paths, and plot everything.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

RNG_SEED = 42
DATA_PATH = "/mnt/user-data/uploads/Project_First_data.csv"
OUT_IMAGE = "/mnt/user-data/outputs/HullWhite_MIBOR_Forecast.png"

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"], format="%d-%b-%y")
df = df.sort_values("Date").reset_index(drop=True)
df["r"] = df["Overnight MIBOR(%)"] / 100.0          # decimal short rate

dt = 1 / 365.0                                       # daily step, calendar-day convention
n = len(df)

df["r_prev"] = df["r"].shift(1)
df["delta_r"] = df["r"] - df["r_prev"]
calib = df.dropna().reset_index(drop=True)           # rows 2..n (drop first NaN row)

# ---------------------------------------------------------------------------
# 2. Calibrate kappa (a) and sigma  -- OLS on  delta_r = a_reg + b*r_prev
# ---------------------------------------------------------------------------
x = calib["r_prev"].values
y = calib["delta_r"].values

b, a_reg = np.polyfit(x, y, 1)                       # slope, intercept
kappa = -b / dt
theta_const_vasicek = -a_reg / b                     # kept only for comparison

fitted = a_reg + b * x
resid = y - fitted
sigma = resid.std(ddof=2) / np.sqrt(dt)

r0 = df["r"].iloc[-1]                                # last observed short rate

print("=== Calibrated constant parameters (mean-reversion part) ===")
print(f"n (data points)        : {n}")
print(f"dt                     : {dt:.6f}")
print(f"slope b                : {b:.6f}")
print(f"intercept a_reg        : {a_reg:.6f}")
print(f"kappa (a)              : {kappa:.4f}")
print(f"sigma                  : {sigma:.4f}")
print(f"r0 (last observed rate): {r0:.4%}")
print(f"[Vasicek-only ref] constant theta = {theta_const_vasicek:.4%}\n")

# ---------------------------------------------------------------------------
# 3. Time-varying phi(t) = theta(t)/a  -- backed out from the discretised SDE,
#    smoothed, then linearly fitted over the full 2-year window
#
#    Discretised SDE:  delta_r(t) = a*(phi(t-1) - r(t-1))*dt + noise
#                 =>    phi(t-1)  = r(t-1) + delta_r(t) / (a*dt)
# ---------------------------------------------------------------------------
calib["phi_raw"] = calib["r_prev"] + calib["delta_r"] / (kappa * dt)

WINDOW = 60  # ~ 3 trading months
calib["phi_smooth"] = calib["phi_raw"].rolling(WINDOW).mean()

t0_date = df["Date"].iloc[0]
calib["t_years"] = (calib["Date"] - t0_date).dt.days / 365.0
t_last = calib["t_years"].iloc[-1]

recent = calib.dropna(subset=["phi_smooth"])   # FULL 2-year window (all valid points)

phi1, phi0 = np.polyfit(recent["t_years"].values, recent["phi_smooth"].values, 1)
phi_at_t_last = phi0 + phi1 * t_last

print("=== Time-varying phi(t) = theta(t)/a  fit (full 2-year window) ===")
print(f"phi0 (intercept)       : {phi0:.6f}")
print(f"phi1 (slope / year)    : {phi1:.6f}")
print(f"phi(t_last)            : {phi_at_t_last:.4%}\n")


def phi_of_t(t_forward):
    """phi(t) for t_forward years AHEAD of the last observed date."""
    return phi0 + phi1 * (t_last + t_forward)


# ---------------------------------------------------------------------------
# 4. Closed-form forecast  E[r(T)]  for a linear phi(t) = phi0 + phi1*t
#
#    dr = a*(phi(t) - r) dt + sigma dW
#    E[r(T)] = r0*e^{-aT} + a * INT_0^T phi(s) e^{-a(T-s)} ds
#    with phi(s) = phi_at_t_last + phi1 * s   (s measured from "today")
#
#    Closed form of the integral gives:
#    E[r(T)] = r0*e^{-aT} + phi_at_t_last*(1-e^{-aT})
#              + phi1*( T - (1-e^{-aT})/a )
# ---------------------------------------------------------------------------
def hull_white_expectation(T):
    ekt = np.exp(-kappa * T)
    return (r0 * ekt
            + phi_at_t_last * (1 - ekt)
            + phi1 * (T - (1 - ekt) / kappa))


horizons = [3.5, 4.5, 5.5]
forecasts = {T: hull_white_expectation(T) for T in horizons}

print("=== Hull-White forecast E[r(T)] ===")
for T, val in forecasts.items():
    print(f"T = {T} years  ->  {val:.4%}")
print()

# ---------------------------------------------------------------------------
# 5. Monte Carlo simulation of the full SDE (Euler-Maruyama) for the plot
# ---------------------------------------------------------------------------
rng = np.random.default_rng(RNG_SEED)

sim_years = 6.0
sim_dt = 1 / 252.0                     # trading-day step for the simulation
n_steps = int(sim_years / sim_dt)
n_paths = 60

paths = np.zeros((n_paths, n_steps + 1))
paths[:, 0] = r0
time_grid = np.linspace(0, sim_years, n_steps + 1)

for i in range(n_steps):
    t_now = time_grid[i]
    ph = phi_of_t(t_now)
    dW = rng.normal(0, np.sqrt(sim_dt), n_paths)
    paths[:, i + 1] = paths[:, i] + kappa * (ph - paths[:, i]) * sim_dt + sigma * dW

mean_path = paths.mean(axis=0)
expectation_curve = np.array([hull_white_expectation(t) for t in time_grid])

future_dates = [df["Date"].iloc[-1] + pd.Timedelta(days=365.0 * t) for t in time_grid]

# ---------------------------------------------------------------------------
# 6. Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7))

# historical observed rate
ax.plot(df["Date"], df["r"] * 100, color="#1f4e78", lw=1.1, label="Historical MIBOR r(t)")

# historical smoothed phi(t) = theta(t)/a
ax.plot(calib["Date"], calib["phi_smooth"] * 100, color="#c55a11", lw=1.6,
        linestyle="--", label="Smoothed phi(t) = theta(t)/a  (60d avg)")

# simulated Monte-Carlo paths (thin, transparent)
for p in range(n_paths):
    ax.plot(future_dates, paths[p] * 100, color="#a6c9e2", lw=0.5, alpha=0.35, zorder=1)

# mean simulated path
ax.plot(future_dates, mean_path * 100, color="#4472c4", lw=1.3, label="Simulated mean path (MC)")

# closed-form expectation curve
ax.plot(future_dates, expectation_curve * 100, color="#7030a0", lw=2.4,
        label="Closed-form E[r(T)] (Hull-White)")

# mark the 3 requested forecast horizons
for T in horizons:
    d = df["Date"].iloc[-1] + pd.Timedelta(days=365.0 * T)
    val = forecasts[T] * 100
    ax.scatter([d], [val], color="red", zorder=5, s=55)
    ax.annotate(f"T={T}y\n{val:.2f}%", (d, val), textcoords="offset points",
                xytext=(0, 12), ha="center", fontsize=9, fontweight="bold", color="darkred")

ax.axvline(df["Date"].iloc[-1], color="gray", lw=0.8, linestyle=":")
ax.text(df["Date"].iloc[-1], ax.get_ylim()[1]*0.97 if ax.get_ylim()[1] else 0,
        " today ", fontsize=8, color="gray")

ax.set_title("Hull-White One-Factor Model — Indian Overnight MIBOR\n"
             "Calibration on last 2 years of daily data, forecast for 3.5 / 4.5 / 5.5 years",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Date")
ax.set_ylabel("Rate (%)")
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%y"))
plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
ax.legend(loc="upper right", fontsize=9)
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig(OUT_IMAGE, dpi=170)
print(f"Plot saved to {OUT_IMAGE}")
