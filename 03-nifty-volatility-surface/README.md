# Nifty Option Volatility Smile: Black-Scholes Implied Volatility at 1M, 3M and 6M

The volatility of an option changes with its strike price. This project takes **Nifty index options** and builds a model to compute the **implied (future) volatility at different strikes** for **1-month, 3-month and 6-month** expiries, then plots volatility against strike to show the **volatility smile**.

---

## Objective

1. Take the Nifty option chain (calls and puts) for the 1M, 3M and 6M expiries.
2. Choose a pricing model and calculate its parameters from market data.
3. Compute the implied volatility at every available strike, for both calls and puts.
4. Plot volatility vs strike for each expiry.

---

## Model Used: Black-Scholes

**Call price**

$$C = S\,N(d_1) - K\,e^{-rT}\,N(d_2)$$

**Put price**

$$P = K\,e^{-rT}\,N(-d_2) - S\,N(-d_1)$$

where

$$d_1 = \frac{\ln(S/K) + \left(r + \frac{\sigma^2}{2}\right)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

Black-Scholes cannot be rearranged to give σ directly. So the market price of each option is known, and **σ is solved numerically** until the model price matches the market price. This σ is the **implied volatility** at that strike.

---

## Model Parameters

| Parameter | Meaning | How it is obtained |
|-----------|---------|--------------------|
| `S` | Nifty spot price | Estimated from **put-call parity** at the at-the-money strike: `S = C − P + K` |
| `K` | Strike price | Taken from the option chain |
| `T` | Time to expiry (years) | 1/12, 3/12 and 6/12 |
| `r` | Risk-free rate | Assumed 6.5% (India) |
| `σ` | Implied volatility | Solved numerically for every strike, for calls and puts |

**Calculated values**

| Expiry | T (years) | Spot S (estimated) | Rows processed |
|--------|-----------|--------------------|----------------|
| 1M     | 0.0833    | 23,261.60          | 129            |
| 3M     | 0.2500    | 23,544.30          | 28             |
| 6M     | 0.5000    | 23,893.10          | 13             |

---

## Methodology

1. **Load and clean** the NSE option chain data (remove commas, treat "-" as missing).
2. **Estimate spot (S)** using put-call parity at the strike where call and put prices are closest.
3. **Solve for σ** at each strike using the market last traded price (LTP):
   - Python uses the **Brent root-finding method**.
   - The Excel sheet shows the same calculation step by step with **Newton-Raphson iterations**.
4. **Plot** implied volatility against strike for calls and puts, with the spot price marked.

---

## Repository Structure

```
├── Project_3_Python.ipynb            # Python notebook: cleaning, S estimate, implied vol, plots
├── Project_3_BS_Parameters.xlsx      # Excel workbook: step-by-step Black-Scholes calculation
├── Project_3_1M_BS_Parameters.csv    # 1-month results (with calculated IV)
├── Project_3_3M_BS_Parameter.csv     # 3-month results
├── Project_3_6M_BS_Parameters.csv    # 6-month results
├── Project_3_Volatility_Smile_Image.png  # Volatility vs strike chart (1M, 3M, 6M)
└── README.md
```

**Key observations**
- The curves are **U-shaped (a volatility smile)**: implied volatility is lowest near the spot price and rises for strikes far away from it. This shows that Black-Scholes' assumption of constant volatility does not hold for real markets.
- Volatility is higher for far out-of-the-money **puts** (low strikes), showing the market pays more for downside protection (a **skew**).
- Fewer strikes are traded for longer expiries, so the 3M and 6M curves have fewer points than 1M.

---

## How to Run

1. Open `Project_3_Python.ipynb` in Google Colab or Jupyter.
2. Upload the three NSE option chain CSV files and update the file paths in the `FILES` dictionary.
3. Install the libraries if needed: `pip install pandas numpy scipy matplotlib`.
4. Run all cells. The notebook prints S for each expiry, saves the CSV results and the chart.

---

## Limitations & Future Work

- **Last traded prices (LTP)** can be stale for illiquid strikes. Using mid-prices of the bid and ask would be more reliable.
- **Spot (S)** is estimated from put-call parity at a single strike, and dividends are ignored. This can explain why call and put implied volatilities do not line up.
- **Deep in-the-money options** trade thinly and give unreliable implied volatility, so some strikes have gaps. Using out-of-the-money options only is the usual approach.
- Black-Scholes assumes constant volatility. Extensions: **SABR**, **Heston** or local volatility models, and fitting a smooth volatility surface across strikes and expiries.

---

## Tools & Libraries

Python · NumPy · pandas · SciPy · Matplotlib · Excel

