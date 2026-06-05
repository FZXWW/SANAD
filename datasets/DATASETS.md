# SANAD INVEST AI — Dataset Documentation

> **Project:** SANAD INVEST AI  
> **Prepared by:** SANAD Team  
> **Last Updated:** April 2026  
> **Total Datasets:** 22 CSV files across 4 product families  
> **Total Size:** ~3.3 MB  
> **Data Source:** Yahoo Finance via `yfinance` Python library  
> **Coverage Period:** 2019-01-01 → 2026-04-24 (where available)
> **New product family:** Deposits are represented by `SA_Deposit_Products.csv`.
> Deposit rows are sourced from official Saudi bank product/pricing pages when public tables are available.
> Some rows are illustrative/indicative examples because banks publish them as examples and state that rates may change.

---

## Column Schema (All Files)

Every CSV file shares the same column structure:

| Column    | Type    | Description                                      |
|-----------|---------|--------------------------------------------------|
| `Date`    | date    | Trading date (YYYY-MM-DD format)                 |
| `Open`    | float   | Price at market open                             |
| `High`    | float   | Highest price during the trading day             |
| `Low`     | float   | Lowest price during the trading day              |
| `Close`   | float   | Adjusted closing price (split & dividend adjusted)|
| `Volume`  | integer | Total shares/units traded during the day         |
| `Ticker`  | string  | Official exchange ticker symbol                  |
| `Company` / `Fund` | string | Human-readable name label              |

> **Note:** Prices are **auto-adjusted** for stock splits and dividends using `yfinance auto_adjust=True`.

---

## Market 1 — Saudi Stock Market (Tadawul)

**Exchange:** Saudi Exchange (Tadawul) — `www.saudiexchange.sa`  
**Currency:** Saudi Riyal (SAR)  
**Source:** Yahoo Finance Historical Data — tickers ending in `.SR`  
**Selection Criteria:** Top 7 companies by market capitalization and sector importance as of 2025, covering Vision 2030 key sectors  

---

### 1.1 SA_Stock_Aramco.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Saudi Arabian Oil Company (Saudi Aramco)   |
| **Ticker**     | 2222.SR                                    |
| **Sector**     | Energy / Oil & Gas                         |
| **Rows**       | 1,589                                      |
| **Date Range** | 2019-12-11 → 2026-04-23                   |
| **Notes**      | Aramco IPO was December 2019, hence shorter history than others. World's largest oil company by revenue. |

---

### 1.2 SA_Stock_AlRajhi.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Al Rajhi Bank                              |
| **Ticker**     | 1120.SR                                    |
| **Sector**     | Banking / Islamic Finance                  |
| **Rows**       | 1,834                                      |
| **Date Range** | 2019-01-02 → 2026-04-23                   |
| **Notes**      | World's largest Islamic bank by assets. Core holding in any Saudi portfolio. |

---

### 1.3 SA_Stock_SABIC.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Saudi Basic Industries Corporation (SABIC) |
| **Ticker**     | 2010.SR                                    |
| **Sector**     | Petrochemicals / Materials                 |
| **Rows**       | 1,833                                      |
| **Date Range** | 2019-01-02 → 2026-04-23                   |
| **Notes**      | One of the world's largest petrochemical companies. Majority owned by Saudi Aramco since 2020. |

---

### 1.4 SA_Stock_SNB.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Saudi National Bank (SNB)                  |
| **Ticker**     | 1180.SR                                    |
| **Sector**     | Banking                                    |
| **Rows**       | 1,833                                      |
| **Date Range** | 2019-01-02 → 2026-04-23                   |
| **Notes**      | Largest bank in Saudi Arabia by assets after the merger of NCB and Samba Financial Group in 2021. |

---

### 1.5 SA_Stock_STC.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Saudi Telecom Company (STC)                |
| **Ticker**     | 7010.SR                                    |
| **Sector**     | Telecommunications / Technology            |
| **Rows**       | 1,834                                      |
| **Date Range** | 2019-01-02 → 2026-04-23                   |
| **Notes**      | Saudi Arabia's largest telecom operator. Leading 5G rollout across the Kingdom and expanding regionally. |

---

### 1.6 SA_Stock_Maaden.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Saudi Arabian Mining Company (Ma'aden)     |
| **Ticker**     | 1211.SR                                    |
| **Sector**     | Mining / Metals                            |
| **Rows**       | 1,833                                      |
| **Date Range** | 2019-01-02 → 2026-04-23                   |
| **Notes**      | Saudi Arabia's national mining champion. Produces gold, phosphate, aluminum, and other minerals. Aligned with Vision 2030 diversification. |

---

### 1.7 SA_Stock_ACWA.csv
| Property       | Value                                       |
|----------------|---------------------------------------------|
| **Company**    | ACWA Power International                    |
| **Ticker**     | 2082.SR                                     |
| **Sector**     | Utilities / Renewable Energy                |
| **Rows**       | 1,083                                       |
| **Date Range** | 2021-10-07 → 2026-04-23                    |
| **Notes**      | Leading developer of renewable energy and water desalination plants. IPO was October 2021. Key Vision 2030 green energy player. Shorter history due to recent listing. |

---

## Market 2 — Saudi Investment Funds

**Exchange:** Tadawul-listed ETFs + US-listed Saudi-focused ETFs  
**Currency:** SAR (Tadawul-listed) / USD (US-listed)  
**Source:** Yahoo Finance Historical Data  
**Selection Criteria:** Top ETFs and index funds with primary Saudi Arabia exposure, covering both locally listed and internationally listed products  

---

### 2.1 SA_Fund_Alawwal_MT30.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | Alawwal MSCI Tadawul 30 ETF                      |
| **Ticker**     | 9410.SR                                          |
| **Type**       | Exchange-Traded Fund (ETF) — Tadawul listed      |
| **Tracks**     | MSCI Tadawul 30 Index (top 30 Tadawul companies) |
| **Rows**       | 369                                              |
| **Date Range** | 2024-10-30 → 2026-04-23                         |
| **Notes**      | Managed by Alawwal Invest / SAB Invest. Passive index fund targeting the 30 largest and most liquid Tadawul stocks. |

---

### 2.2 SA_Fund_Albilad_MSCI_Saudi.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | Albilad MSCI Saudi Equity ETF                    |
| **Ticker**     | 9412.SR                                          |
| **Type**       | Exchange-Traded Fund (ETF) — Tadawul listed      |
| **Tracks**     | MSCI Saudi Arabia Index                          |
| **Rows**       | 126                                              |
| **Date Range** | 2025-10-22 → 2026-04-23                         |
| **Notes**      | Managed by Albilad Capital. Shariah-compliant. Newest ETF in the dataset with the shortest history. |

---

### 2.3 SA_Fund_Jadwa_Saudi_Equity.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | Jadwa Saudi Equity ETF                           |
| **Ticker**     | 9411.SR                                          |
| **Type**       | Exchange-Traded Fund (ETF) — Tadawul listed      |
| **Tracks**     | Saudi equity market broad index                  |
| **Rows**       | 369                                              |
| **Date Range** | 2024-10-30 → 2026-04-23                         |
| **Notes**      | Managed by Jadwa Investment. Focuses on large-cap Saudi equities. Shariah-compliant structure. |

---

### 2.4 SA_Fund_iShares_MSCI_Saudi_KSA.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | iShares MSCI Saudi Arabia ETF                    |
| **Ticker**     | KSA                                              |
| **Exchange**   | NYSE Arca (US-listed)                            |
| **Type**       | Exchange-Traded Fund (ETF)                       |
| **Tracks**     | MSCI Saudi Arabia IMI 25/50 Index                |
| **Rows**       | 1,838                                            |
| **Date Range** | 2019-01-02 → 2026-04-24                         |
| **Notes**      | Managed by BlackRock. Largest Saudi-focused ETF globally with over $750M in AUM. Gives international investors exposure to Saudi equities. Longest history in this group. |

---

### 2.5 SA_Fund_Franklin_FTSE_Saudi.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | Franklin FTSE Saudi Arabia ETF                   |
| **Ticker**     | FLSA                                             |
| **Exchange**   | NYSE Arca (US-listed)                            |
| **Type**       | Exchange-Traded Fund (ETF)                       |
| **Tracks**     | FTSE Saudi Arabia Capped Index                   |
| **Rows**       | 1,838                                            |
| **Date Range** | 2019-01-02 → 2026-04-24                         |
| **Notes**      | Managed by Franklin Templeton. Low-cost passive ETF providing broad Saudi market exposure. Competes directly with KSA ETF. |

---

### 2.6 SA_Fund_TASI_Index.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | Tadawul All Share Index (TASI)                   |
| **Ticker**     | ^TASI.SR                                         |
| **Type**       | Market Index (not investable directly)           |
| **Represents** | All listed companies on the Saudi Exchange       |
| **Rows**       | 1,803                                            |
| **Date Range** | 2019-01-02 → 2026-04-23                         |
| **Notes**      | The primary benchmark index of the Saudi stock market. Used as the market reference and for performance comparison. Equivalent to the S&P 500 for Saudi Arabia. |

---

### 2.7 SA_Fund_VanEck_Gulf.csv
| Property       | Value                                            |
|----------------|--------------------------------------------------|
| **Fund**       | VanEck Gulf States Index ETF                     |
| **Ticker**     | GULF                                             |
| **Exchange**   | NYSE Arca (US-listed)                            |
| **Type**       | Exchange-Traded Fund (ETF)                       |
| **Tracks**     | Gulf States broad equity index (GCC region)      |
| **Rows**       | 365                                              |
| **Date Range** | 2019-01-02 → 2020-06-12                         |
| **Notes**      | Managed by VanEck. Provides exposure to Gulf Cooperation Council (GCC) countries including Saudi Arabia, UAE, Qatar, and Kuwait. **This ETF was delisted in mid-2020**, so data only covers 2019–2020. Included for historical GCC regional context. |

---

## Market 3 — US Stock Market (S&P 500 / NASDAQ)

**Exchange:** NASDAQ / NYSE  
**Currency:** US Dollar (USD)  
**Source:** Yahoo Finance Historical Data  
**Selection Criteria:** Top 7 US companies by market capitalization as of 2025 (the Magnificent Seven), representing the most globally influential and actively traded US equities  

---

### 3.1 US_Stock_Apple.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Apple Inc.                                 |
| **Ticker**     | AAPL                                       |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | Technology / Consumer Electronics          |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | World's largest company by market cap. Products include iPhone, Mac, iPad, Apple Watch, and services (App Store, iCloud, Apple TV+). |

---

### 3.2 US_Stock_Microsoft.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Microsoft Corporation                      |
| **Ticker**     | MSFT                                       |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | Technology / Cloud Computing               |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | Dominant in enterprise software (Windows, Office 365, Azure cloud). Major investor in OpenAI. One of the most stable growth stocks in the index. |

---

### 3.3 US_Stock_NVIDIA.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | NVIDIA Corporation                         |
| **Ticker**     | NVDA                                       |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | Technology / Semiconductors / AI           |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | World's leading GPU and AI chip manufacturer. Explosive growth driven by AI/LLM demand. Among the most volatile and highest-growth stocks in the dataset. |

---

### 3.4 US_Stock_Amazon.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Amazon.com Inc.                            |
| **Ticker**     | AMZN                                       |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | E-Commerce / Cloud Computing               |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | World's largest e-commerce platform and second-largest cloud provider (AWS). Highly diversified across retail, logistics, streaming (Prime Video), and AI. |

---

### 3.5 US_Stock_Alphabet.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Alphabet Inc. (Google)                     |
| **Ticker**     | GOOGL                                      |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | Technology / Digital Advertising / AI      |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | Parent company of Google, YouTube, and Google Cloud. Dominates global search advertising. Heavily investing in AI (Gemini models, DeepMind). |

---

### 3.6 US_Stock_Meta.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Meta Platforms Inc.                        |
| **Ticker**     | META                                       |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | Technology / Social Media                  |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | Owner of Facebook, Instagram, WhatsApp, and Threads. Pivoted toward AI and the metaverse. Notable 2022 crash and 2023–2026 recovery makes it an interesting volatility case study. |

---

### 3.7 US_Stock_Tesla.csv
| Property       | Value                                      |
|----------------|--------------------------------------------|
| **Company**    | Tesla Inc.                                 |
| **Ticker**     | TSLA                                       |
| **Exchange**   | NASDAQ                                     |
| **Sector**     | Electric Vehicles / Clean Energy           |
| **Rows**       | 1,838                                      |
| **Date Range** | 2019-01-02 → 2026-04-24                   |
| **Notes**      | World's most recognized electric vehicle brand. Also operates energy storage and solar businesses. Among the most volatile stocks in the dataset — extreme highs and lows between 2019–2026. |

---

## Data Source Details

| Property             | Details                                              |
|----------------------|------------------------------------------------------|
| **Primary Source**   | Yahoo Finance                                        |
| **Access Method**    | `yfinance` Python library (open-source)              |
| **Library Version**  | yfinance (latest as of April 2026)                   |
| **Download Script**  | Custom Python script — runs in the project notebook  |
| **Adjustment**       | `auto_adjust=True` — prices adjusted for splits & dividends |
| **Frequency**        | Daily (business days only, no weekends/holidays)     |
| **Official Source**  | https://finance.yahoo.com                            |

---

## Dataset Summary Table

| # | File | Market | Ticker | Rows | Date From | Date To |
|---|------|--------|--------|------|-----------|---------|
| 1 | SA_Stock_Aramco.csv | Saudi Stocks | 2222.SR | 1,589 | 2019-12-11 | 2026-04-23 |
| 2 | SA_Stock_AlRajhi.csv | Saudi Stocks | 1120.SR | 1,834 | 2019-01-02 | 2026-04-23 |
| 3 | SA_Stock_SABIC.csv | Saudi Stocks | 2010.SR | 1,833 | 2019-01-02 | 2026-04-23 |
| 4 | SA_Stock_SNB.csv | Saudi Stocks | 1180.SR | 1,833 | 2019-01-02 | 2026-04-23 |
| 5 | SA_Stock_STC.csv | Saudi Stocks | 7010.SR | 1,834 | 2019-01-02 | 2026-04-23 |
| 6 | SA_Stock_Maaden.csv | Saudi Stocks | 1211.SR | 1,833 | 2019-01-02 | 2026-04-23 |
| 7 | SA_Stock_ACWA.csv | Saudi Stocks | 2082.SR | 1,083 | 2021-10-07 | 2026-04-23 |
| 8 | SA_Fund_Alawwal_MT30.csv | Saudi Funds | 9410.SR | 369 | 2024-10-30 | 2026-04-23 |
| 9 | SA_Fund_Albilad_MSCI_Saudi.csv | Saudi Funds | 9412.SR | 126 | 2025-10-22 | 2026-04-23 |
| 10 | SA_Fund_Jadwa_Saudi_Equity.csv | Saudi Funds | 9411.SR | 369 | 2024-10-30 | 2026-04-23 |
| 11 | SA_Fund_iShares_MSCI_Saudi_KSA.csv | Saudi Funds | KSA | 1,838 | 2019-01-02 | 2026-04-24 |
| 12 | SA_Fund_Franklin_FTSE_Saudi.csv | Saudi Funds | FLSA | 1,838 | 2019-01-02 | 2026-04-24 |
| 13 | SA_Fund_TASI_Index.csv | Saudi Funds | ^TASI.SR | 1,803 | 2019-01-02 | 2026-04-23 |
| 14 | SA_Fund_VanEck_Gulf.csv | Saudi Funds | GULF | 365 | 2019-01-02 | 2020-06-12 |
| 15 | US_Stock_Apple.csv | US Stocks | AAPL | 1,838 | 2019-01-02 | 2026-04-24 |
| 16 | US_Stock_Microsoft.csv | US Stocks | MSFT | 1,838 | 2019-01-02 | 2026-04-24 |
| 17 | US_Stock_NVIDIA.csv | US Stocks | NVDA | 1,838 | 2019-01-02 | 2026-04-24 |
| 18 | US_Stock_Amazon.csv | US Stocks | AMZN | 1,838 | 2019-01-02 | 2026-04-24 |
| 19 | US_Stock_Alphabet.csv | US Stocks | GOOGL | 1,838 | 2019-01-02 | 2026-04-24 |
| 20 | US_Stock_Meta.csv | US Stocks | META | 1,838 | 2019-01-02 | 2026-04-24 |
| 21 | US_Stock_Tesla.csv | US Stocks | TSLA | 1,838 | 2019-01-02 | 2026-04-24 |

---

## Important Notes

1. **Shorter Histories:** Aramco (IPO Dec 2019), ACWA Power (IPO Oct 2021), and Albilad MSCI ETF (listed Oct 2025) have fewer rows due to their recent listings — this is expected and not a data error.

2. **VanEck Gulf (GULF) Delisted:** This ETF was delisted in June 2020. Its data is limited to 2019–2020 and should only be used for historical GCC regional context, not as a current active fund.

3. **Tadawul-listed ETFs (9410, 9411, 9412):** These are relatively new products with limited history (starting late 2024). For longer time series in Saudi funds, prefer KSA or FLSA.

4. **Price Adjustment:** All Close prices are adjusted for stock splits and dividends. This means historical prices may differ from raw historical quotes seen on chart platforms.

5. **Currency:** Saudi-listed assets are priced in **SAR**. US-listed assets (KSA, FLSA, GULF, and all US stocks) are priced in **USD**. Do not mix currencies directly in a model without normalization.
