# 🏦 FabricPulse – Hybrid Batch & Real-Time Financial Data Platform

FabricPulse is an end-to-end data engineering project built using **Microsoft Fabric**, focused on designing and operating a **hybrid batch and real-time financial data platform**.

The project emphasizes **data ingestion, modeling, orchestration, and real-time analytics**, rather than BI dashboarding, to reflect real-world data engineering responsibilities.

---

## 🧠 Project Overview

FabricPulse processes financial data from two distinct ingestion paths:

- **Batch ingestion** of structured financial datasets (customers, accounts, instruments, transactions)
- **Streaming ingestion** of real-time transaction events

Batch data is processed using a **Medallion (Bronze–Silver–Gold) Lakehouse architecture** and modeled into analytical tables.  
Streaming data is ingested via **Eventstream** and analyzed in near real time using **Eventhouse (KQL)** dashboards, while also being persisted to the Lakehouse for historical tracking.

---

## 🏗️ Architecture

### Batch Processing Flow

```
CSV Files
↓
Bronze Layer (Raw Delta Tables)
↓
Silver Layer (Data Cleaning & Validation)
↓
Gold Layer (Dimensional & Analytical Tables)
```


### Real-Time Processing Flow

```
Event Generator
↓
Eventstream
↙ ↘
Eventhouse Lakehouse
(Real-Time) (Historical Storage)
```


---

## ⚙️ Tech Stack

### Platform
- Microsoft Fabric
- Fabric Lakehouse
- Fabric Eventstream
- Eventhouse (KQL Database)
  - Monitoring Hub

### Processing & Modeling
- Apache Spark (PySpark)
- Delta Lake
- Medallion Architecture (Bronze / Silver / Gold)
- Dimensional Modeling (Star Schema)

### Orchestration & Ops
- Fabric Data Pipelines (Notebook Automation)
- External Git Repository (exported notebooks & assets)

---

## 🧱 Data Modeling

### Gold Layer

**Dimensions**
- `dim_customers`
- `dim_accounts`
- `dim_instruments`
- `dim_date`

**Fact Tables**
- `fact_transactions`

Surrogate keys are used for all dimensions to:
- Improve join performance
- Decouple analytical models from source-system identifiers
- Ensure long-term schema stability

---

## ⚡ Real-Time Analytics

- Transaction events are generated and ingested via **Eventstream**
- Events are routed to:
  - **Eventhouse (KQL Database)** for low-latency querying and live dashboards
  - **Lakehouse** for long-term persistence and batch reconciliation
- Real-time dashboards are implemented using **KQL**, focusing on:
  - Transaction volume trends
  - Inbound vs outbound flows
  - Instrument-level activity
  - High-frequency account behavior

---

## 🔍 Key Engineering Features

- Hybrid batch + streaming architecture
- Data quality validation and referential integrity checks
- Clean separation between raw, refined, and analytical layers
- Automated execution of Spark notebooks
- Real-time analytics without BI refresh cycles
- Production-style modeling and governance practices

---

## 🚧 Limitations & Future Enhancements

- Incremental batch ingestion and CDC
- Slowly Changing Dimensions (SCD Type 2)
- Unified batch + streaming analytical views
- Real-time alerting rules on KQL dashboards
- Native CI/CD once Fabric Git integration is enabled
- Power BI Dashboard integration

---

## 📌 Final Notes

FabricPulse focuses on **data engineering fundamentals**: ingestion, transformation, modeling, orchestration, and real-time processing — without relying on BI tools — making it a strong representation of production-grade data platform design.
