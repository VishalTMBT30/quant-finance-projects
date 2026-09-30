# Bond Duration and DV01 Risk Analysis

Duration and key-rate DV01 of an 8% semi-annual coupon bond, calculated in Excel using interest rates from the Hull-White model (see Project 01).

---

## Problem Statement

A bond pays an **8% coupon semi-annually for 10 years**, with a principal of **Rs. 10 lakhs**.

a. Compute the duration of the bond.
b. Calculate the DV01 risk of the bond at the **1Y, 2Y, 3Y, 4Y and 5Y** points, using the rates and model from Project 01 (3.5, 4.5 and 5.5 years).

---

## File

| File | Description |
|------|-------------|
| `Project_2.xlsx` | Excel workbook with two sheets: duration and DV01 |

There is no code in this project. All calculations are live Excel formulas.

---

## Bond Details

| Item | Value |
|------|-------|
| Principal | Rs. 10,00,000 |
| Coupon rate | 8% per year |
| Coupon payment | Rs. 40,000 every 6 months |
| Tenor | 10 years (20 payments) |

---

## Workbook Sheets

### Sheet 1: Macaulay Duration (a)
- Cash flows of the bond: Rs. 40,000 each half-year, plus the principal in the last period.
- Each cash flow is discounted at a flat 4% half-yearly rate.
- Duration = Sum of (PV × time) / Sum of PV.
- **Macaulay Duration = 7.07 years** (14.13 half-year periods).

### Sheet 2: DV01 (b)
1. **Bond parameters:** coupon, frequency, tenor, principal and the 1 bp shock size.
2. **Model rates:** the Project 01 Hull-White rates for 3.5Y, 4.5Y and 5.5Y fit a straight line exactly:

   Rate(t) = 5.01% − 0.80% × t

3. **Rates at key points:**

   | Year | 1Y | 2Y | 3Y | 4Y | 5Y |
   |------|------|------|------|------|------|
   | Rate | 4.21% | 3.41% | 2.61% | 1.81% | 1.01% |

4. **Pricing:** all 20 cash flows are discounted with DF(t) = (1 + Rate(t))^(−t).
   - Bond price = **Rs. 21,80,621**
   - Macaulay duration on the model curve = **8.31 years**
5. **Key-rate shocks:** one node is shifted by +1 bp at a time. The shock is triangular, which means it fades to zero at the neighbouring nodes. The 5Y node is held flat after 5 years, so it covers the tail up to 10 years.
6. **DV01 = Base price − Bumped price**

---

## Results

| Key-Rate Node | Base Rate | DV01 (Rs.) |
|---------------|-----------|------------|
| 1Y | 4.21% | 8.28 |
| 2Y | 3.41% | 14.47 |
| 3Y | 2.61% | 21.67 |
| 4Y | 1.81% | 29.30 |
| 5Y | 1.01% | 1,783.30 |
| **Total** | | **1,857.02** |

**Check:** the total matches the DV01 from a parallel 1 bp shift of the whole curve (Rs. 1,857.02).

---

## Key Observations

- The 5Y node has by far the largest DV01. It carries all cash flows from year 5 to year 10, including the Rs. 10 lakh principal repayment.
- Short nodes (1Y to 4Y) have small DV01 because only coupons fall in their range.
- The bond is most sensitive to changes in long-term rates.

---

## Assumptions and Limitations

- Only three model rates (3.5Y, 4.5Y, 5.5Y) are available, so a straight line is used to get all other rates.
- The line extended beyond 5.5 years gives **negative rates after about 6.3 years**, and discount factors above 1. This is why the bond price (Rs. 21.8 lakh) is much higher than its principal.
- Rates are annually compounded zero rates.
- DV01 is for a +1 bp shock and is measured as a fall in price.
- A fuller version would use a proper bootstrapped yield curve instead of a straight line.

---

## How to Use

1. Download `Project_2.xlsx` and open it in Excel.

