# 📈 Portfolio Gain Calculator

## 📝 Overview
In this example, the gains (from a made-up portfolio) are calculated for a given test date range.  
Basically that what you would see with your investment account.

---

## 🚀 Scenario and Steps
The scenario assumes an investment of **$1000 into few stocks** at the start of **2025**, sold at the end of the year (**Dec 2025**).

### Steps:
1. **Read active stock historical data** using Yahoo Finance via python script.  
2. **Save results into Excel**, where each stock’s historical data is stored in its own sheet named after the stock symbol.  
3. **Create Excel macros** that generate an `investment` sheet with the following grid:

---

## 📊 Investment Sheet Example

| Investment and % | Shares Name | Start Date | End Date   | Buy Price Per Share | Sell Price Per Share | Purchase Total | Proceeds From Sale | Gain/Loss (Proceeds - Purchase) | Gain/Loss % |
|------------------|-------------|------------|------------|---------------------|----------------------|----------------|--------------------|---------------------------------|-------------|
| 100000           |             |            |            |                     |                      |                |                    |                                 |             |
| 50.00%           | NVDA        | 2025-01-02 | 2025-11-28 | 135.9628052         | 179.0000254          | 367.7476345    | 65826.83591        | 15826.83591                      | 15.83%      |
| 50.00%           | VTI         | 2025-01-02 | 2025-11-28 | 288.7520661         | 335.3999939          | 173.1589342    | 58077.50546        | 8077.505465                      | 8.08%       |
|                  |             |            |            |                     |                      |                | **Total Gain**     | **23904.34138**                  | **23.90%**  |
|                  |             |            |            |                     |                      |                | **Total Sum**      | **123904.3414**                  |             |

---

## 📈 Chart Reference
For reference, a chart is generated that shows the **historical data for all shares in the portfolio** to visualiz the performance trends across the selected date range.

---

## ⚙️ User Interaction
- Users can **change Investment and %**, **Start Date**, and **End Date** to see how gains differ.  
- The formulas in the excel (inserted by macros) dynamically update calculations based on user input.

---

## ✅ Key Features
- Automated retrieval of stock data via Yahoo Finance using python script.  
- Organized Excel sheets per stock symbol using python script.  
- Macro-driven `investment` sheet with gain/loss calculations.  
- Chart for portfolio performance visualization.  
- Flexible inputs for investment amount and date ranges.

---

## 📌 Future Improvements
- Add prediction ability based on the **historical data for all shares in the portfolio**.  