# IEG Project – Integrated Energy Grids

DTU Course 46770 – February 2026

This repository contains coursework for the Integrated Energy Grids project, including assignment 1 from Group 5. The Python script main contains code for tasks a and c, whereas part_b and part_d script is exclusively for task b and d respectively.

## 📋 Project Overview

In this project, you'll develop a comprehensive energy system model for a chosen country or region, optimizing renewable and non-renewable generation capacities while considering interconnections with neighboring systems and energy storage technologies.

---

## 📝 Assignment 1 – System Optimization & Network Analysis

**Deadline:** May 01, 2026, 23:55  
**Format:** Group report (4 students)  
**Submission:** DTULearn

### Prerequisites
- Review the PyPSA tutorial before starting

### Tasks

Part 1:

a) Single country optimal capacity mix for renewable and non-renewable generators; dispatch time series, annual electricity mix, and duration curves.
b) Sensitivity of results to interannual variability in solar and wind generation across multiple weather years.
c) Storage technology integration; impact on optimal system configuration and balancing strategies across intraday and seasonal timescales.
d) Multi-country network with HVDC interconnectors and at least one closed cycle; linearised AC power flow (DC approximation) optimisation.
e) Manual calculation of incidence matrix and PTDF matrix; verification of power flows against PyPSA results for the first time step.

Part 2:

f) Single-country sensitivity of optimal capacity mix to CO2 constraints, benchmarked against national historical emissions.
g) Multi-country model with gas pipeline transport (H2 or CH4); comparison of electricity vs. gas network energy flows.
h) CO2 shadow price analysis for a selected decarbonisation target; comparison against real-world ETS and national carbon tax levels.
i) Sector coupling: co-optimisation of electricity and heating sectors.
j) Sensitivity analysis on gas price (30–120 €/MWh) and offshore wind capital cost reductions (−20% to −60%) across 12 scenarios.

---

## 🛠️ Tools & Resources

- **Modeling Framework:** [PyPSA](https://pypsa.io/)
- **Documentation:** Official PyPSA tutorials and documentation
- **Data Sources:** Real grid data for transmission capacities and technology costs

## 📂 Repository Structure

```
IEG Project/
├── README.md                          (this file)
├── Assignment_1/                      (Part 1 materials)
│   ├── models/                        (PyPSA models)
│   ├── analysis/                      (Analysis scripts)
│   └── report/                        (Final report)
└── Assignment_2/                      (Part 2 materials)
```

---

## 📌 Notes

- All cost and technological assumptions must be referenced
- Ensure reproducibility of results
- Include clear visualizations and explanations
- For section 1e, document manual calculations clearly for verification
1
