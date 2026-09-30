# Derivation of θ(t) in the Hull-White Model

A step-by-step derivation of the Hull-White drift function **θ(t)** using the **risk-neutral pricing approach**, showing how the model is fitted to today's market term structure.

---

## Problem Statement

The Hull-White model uses the current term structure to get the value of θ, one of the parameters of the model. Derive the equation of θ using the risk-neutral process approach.

---

## File

| File | Description |
|------|-------------|
| `Project_4_Hull_White_Theta_Derivation.pdf` | Handwritten derivation (8 steps) |

There is no code in this project. It is a mathematical derivation.

---

## The Model

Under the risk-neutral measure, the short rate follows:

$$dr_t = \big[\theta(t) - a\,r_t\big]\,dt + \sigma\,dW_t$$

| Symbol | Meaning |
|--------|---------|
| `r` | Short interest rate |
| `θ(t)` | Time-dependent "push" on the rate (the unknown we want to find) |
| `a` | Speed of mean reversion (pull back towards normal) |
| `σ` | Volatility (size of the random shock) |
| `dW` | Random shock (Brownian motion) |

---

## Steps of the Derivation

| Step | What is done |
|------|--------------|
| 1 | Write the rate model under the risk-neutral measure |
| 2 | Write the bond price as the risk-neutral average of the discount factor: $P(t,T)=E^{Q}\left[e^{-\int_t^T r(s)ds}\,\middle|\,F_t\right]$, and define $B(t,T)=\frac{1-e^{-a(T-t)}}{a}$ |
| 3 | Solve the rate equation to get r(s) as a sum of three parts: starting rate, θ pushes, and random shocks |
| 4 | Find the average and variance of the total interest $X=\int_t^T r(s)\,ds$ |
| 5 | Use the rule $E[e^{-X}]=\exp\left(-E[X]+\frac{Var[X]}{2}\right)$ to get the bond price with θ inside |
| 6 | Set t = 0 and match the model to today's market forward rate $f(0,T)=-\frac{\partial \ln P(0,T)}{\partial T}$ |
| 7 | Differentiate once more so the integral disappears and θ(T) stands alone |
| 8 | Simplify to get the final answer |

---

## Key Results

**Mean and variance of total interest (Step 4):**

$$E[X] = r(t)\,B(t,T) + \int_t^T \theta(u)\,B(u,T)\,du$$

$$Var[X] = \sigma^2 \int_t^T B(u,T)^2\,du$$

**Bond price with θ inside (Step 5):**

$$\ln P(t,T) = -r(t)\,B(t,T) - \int_t^T \theta(u)\,B(u,T)\,du + \frac{\sigma^2}{2}\int_t^T B(u,T)^2\,du$$

**Matching condition with today's market curve (Step 6):**

$$f(0,T) = r(0)\,e^{-aT} + g(T) - \frac{\sigma^2}{2a^2}\left(1-e^{-aT}\right)^2, \qquad g(T)=\int_0^T e^{-a(T-u)}\theta(u)\,du$$

---

## Final Answer

$$\boxed{\theta(t) = \frac{\partial f(0,t)}{\partial t} + a\,f(0,t) + \frac{\sigma^2}{2a}\left(1-e^{-2at}\right)}$$

where f(0,t) is the instantaneous forward rate taken from today's market curve.

---

## What Each Term Means

| Term | Meaning |
|------|---------|
| $\frac{\partial f(0,t)}{\partial t}$ | Slope of today's forward curve. If the market curve is rising, the rate must drift upward along it |
| $a\,f(0,t)$ | Correction for mean reversion. The model pulls the rate back, so θ adds enough push to keep the rate on the market curve |
| $\frac{\sigma^2}{2a}\left(1-e^{-2at}\right)$ | Convexity correction from volatility. Small at first and grows with time |

---

## Sanity Check

If the forward curve is flat at f₀ and σ = 0, then θ = a·f₀. The long-run level θ/a then equals f₀, so the rate stays on the market curve, as expected. With θ constant, the model becomes the Vasicek model.

---

## Connection to Other Projects

This θ(t) is the quantity used in the Hull-White model in **Project 01 (MIBOR: Vasicek vs Hull-White)**, where it is what makes the model match today's curve.

