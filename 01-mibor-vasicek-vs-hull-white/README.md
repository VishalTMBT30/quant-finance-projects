# MIBOR Interest Rate Forecasting: Vasicek vs Hull-White

Forecasting the Indian **MIBOR** (Mumbai Interbank Offered Rate) for **3.5-year, 4.5-year and 5.5-year** horizons using two short-rate models, calibrated on the **last 2 years of historical MIBOR data**, and comparing which model is better.

---

## Objective

1. Collect 2 years of historical MIBOR data.
2. Estimate the parameters of the **Vasicek** and **Hull-White** models.
3. Use each model to get interest rates for **3.5, 4.5 and 5.5 years**.
4. Plot the results and conclude which model is better, and why.

---

## Models

### 1. Vasicek Model

$$dr_t = a\,(b - r_t)\,dt + \sigma\,dW_t$$

| Parameter | Meaning |
|-----------|---------|
| `a` | Speed of mean reversion |
| `b` | Long-run mean level of the rate |
| `σ` | Volatility of the short rate |

Expected short rate at time T:

$$E[r_T] = r_0\,e^{-aT} + b\,(1 - e^{-aT})$$

Because `a`, `b` and `σ` are constant, the model cannot exactly match today's yield curve.

### 2. Hull-White Model

$$dr_t = \big[\theta(t) - a\,r_t\big]\,dt + \sigma\,dW_t$$

The constant long-run mean is replaced by a time-dependent drift θ(t), which is chosen so the model reproduces the current term structure exactly:

$$\theta(t) = \frac{\partial f(0,t)}{\partial t} + a\,f(0,t) + \frac{\sigma^2}{2a}\left(1 - e^{-2at}\right)$$

where f(0,t) is the instantaneous forward rate from today's curve.

---

## Methodology

1. **Data**: daily MIBOR rates for the last 2 years (Source: [add source, e.g. FBIL], data csv file separately uploaded).
2. **Calibration**:
   - Vasicek: `a`, `b`, `σ` estimated from the historical series using regression on the discretised process.
   - Hull-White: `a` and `σ` estimated from the historical series; θ(t) derived from the current term structure ([add curve used]).
3. **Forecasting**: model-implied rates computed for 3.5, 4.5 and 5.5 years.
4. **Visualisation**: charts of each model and a side-by-side comparison.
5. **Comparison**: fit, flexibility and realism of both models.

---

## Repository Structure

```
01-mibor-vasicek-vs-hull-white/
├── mibor_vasicek.py                  # Python code: Vasicek model
├── mibor_hull_white.py               # Python code: Hull-White model
├── mibor_vasicek_calculation.xlsx    # Excel calculation: Vasicek model
├── mibor_hull_white_calculation.xlsx # Excel calculation: Hull-White model
├── images/
│   ├── vasicek_chart.png             # Vasicek chart
│   └── hull_white_chart.png          # Hull-White chart
└── README.md
```

| File | Description |
|------|-------------|
| `mibor_vasicek.py` | Python code for the Vasicek model |
| `mibor_hull_white.py` | Python code for the Hull-White model |
| `mibor_vasicek_calculation.xlsx` | Excel calculation of the Vasicek model |
| `mibor_hull_white_calculation.xlsx` | Excel calculation of the Hull-White model |
| `images/vasicek_chart.png` | Chart of Vasicek model results |
| `images/hull_white_chart.png` | Chart of Hull-White model results |

---
## How to Run

```bash
git clone https://github.com/<VishalTMBT30>/quant-finance-projects.git
cd quant-finance-projects/01-mibor-vasicek-vs-hull-white
pip install numpy pandas matplotlib scipy openpyxl
python mibor_vasicek.py
python mibor_hull_white.py
```

Each script reads the MIBOR data, calibrates its model, prints the 3.5 / 4.5 / 5.5-year rates and saves the chart to `images/`.

---

## Results

| Horizon | Vasicek | Hull-White |
|---------|---------|------------|
| 3.5 years | 6.06% | 2.21% |
| 4.5 years | 5.63% | 1.41% |
| 5.5 years | 6.19% | 0.61% |


![Vasicek](images/vasicek_chart.png)
![Hull-White](images/hull_white_chart.png)


---

## Which Model Is Better?
-- Vasicek model 


Realistic: Vasicek stays at about 5.6% to 6.2%, close to the 2-year average MIBOR of about 5.75%. Hull-White falls to 0.61%, which is unrealistic.
Stable: Vasicek reverts to a steady long-run level. Hull-White extends the last 2 years' downward trend, so its forecast keeps falling.
Note: Hull-White is theoretically stronger because it can fit the yield curve. It would perform better if it were calibrated to a real yield curve.
---

## Limitations & Future Work

- Only a 2-year window is used, so estimates are sensitive to the recent rate regime.
- Both models allow negative interest rates.
- Matching today's curve does not guarantee better future forecasts; out-of-sample backtesting is needed to confirm this.
- Possible extensions: CIR model, multi-factor models, longer calibration windows.

---

## Tools & Libraries

Python · NumPy · pandas · Matplotlib · SciPy · Excel

