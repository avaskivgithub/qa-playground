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
3. **Create Excel macros** that generate an `investment` sheet with the following grid 📊
![Example of the Investmet sheet](images/TestPertfolioScreenshot.png)

⚙️ User Interaction
- Users can **change Investment and %**, **Start Date**, and **End Date** to see how gains differ.  
- The formulas in the excel (inserted by macros) dynamically update calculations based on user input.

📈 For reference, a chart is generated that shows the **historical data for all shares in the portfolio** to visualiz the performance trends across the selected date range.

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