
# Closing Nigeria's Flood Data Gap
### A Collective Intelligence Approach for Rapid Response and Risk Reduction

Policy brief and supporting data analysis on Nigeria's 2022 flood crisis, evaluating three policy solutions to the country's flood data gap and recommending a community generated collective intelligence (CI) platform for real time flood reporting.

**Author:** Abiola Ajao

## Project Overview

Nigeria's 2022 floods, worsened by heavy rainfall and the release from Cameroon's Lagdo Dam, resulted in 662 deaths, 3,174 injuries, and over 2.4 million displaced persons nationwide. This project analyzes NEMA's 2022 flood impact data and uses the findings to support a policy brief that evaluates three alternative solutions to Nigeria's flood data gap using Graham Smith's (2009) democratic goods framework: inclusion, considered judgment, popular control, transparency, efficiency, and transferability.

The three solutions evaluated are:

1. Expanding hydrological sensor networks
2. Infrastructure focused mitigation (drainage, levees, embankments)
3. A community generated CI flood data platform (recommended solution)

The brief recommends a phased rollout of the CI platform in Lagos, Bayelsa, and Rivers states, modeled on Kenya's Ushahidi platform.

## Repository Contents

| File | Description |
|---|---|
| `Flood_Data_Analysis.ipynb` | Jupyter notebook that cleans, aggregates, and visualizes the NEMA flood dataset by state and LGA |
| `nema-flood-data-06102022.xlsx` | Raw NEMA 2022 flood impact dataset, sourced from HDX |
| `Policy_Brief_Final_Report_Submission.pdf` | Final policy brief document |
| `README.md` | This file |

## Data Source

The dataset used in the notebook is NEMA's 2022 flood affected geographical areas data, downloaded from the Humanitarian Data Exchange (HDX):

https://data.humdata.org/dataset/nigeria-nema-flood-affected-geographical-areas-north-east-nigeria-flood-affected-geographical-areas/resource/833fe41d-1b92-4ca8-bfa0-8b483ed81690

One note on this: the HDX dataset page is titled "North East Nigeria Flood Affected Geographical Areas," but the actual worksheet used (`2022 NEMA Flood Data`) contains records from states across the country, including Abia, Anambra, Yobe, Taraba, and others, not just the North East zone. The title on HDX looks like a labeling artifact rather than a scope restriction, since the state and LGA columns in the file itself go well beyond North East Nigeria. Worth keeping in mind if this dataset is cited or reused elsewhere, since a reader relying on the title alone would undercount its actual coverage.

The workbook has two sheets: `Sheet1` and `2022 NEMA Flood Data`. The notebook reads from the second sheet, which has six columns: `STATE`, `LGA`, `COMMUNITY`, `DATE OF OCCURRENCE`, `PERSONS AFFECTED`, and `DISPLACED PERSONS`, across roughly 840 rows.

## Methodology

The notebook, built and run in Google Colab, performs the following steps using `pandas` and `matplotlib`:

1. Loads the `2022 NEMA Flood Data` sheet from the Excel workbook
2. Cleans the `PERSONS AFFECTED` and `DISPLACED PERSONS` columns, coercing non-numeric entries (such as `-`) to zero
3. Aggregates persons affected and displaced by state, and separately by LGA
4. Sorts and selects the top 10 states and top 10 LGAs by persons affected
5. Produces grouped bar charts for both breakdowns (Figures 3 and 4 in the policy brief)
6. Summarizes totals and highlights the top 3 LGAs by impact

## Key Findings

- Ogbaru LGA recorded the highest impact: 289,432 persons affected and 204,139 displaced
- Anambra West followed with 240,351 affected and 187,278 displaced
- Anambra East recorded 106,154 affected and 98,672 displaced
- Across all LGAs in the dataset, roughly 1,573,498 persons were affected and 866,939 displaced
- Anambra State dominates the state level breakdown, with affected numbers far exceeding every other state in the dataset

## Running the Notebook

```bash
pip install pandas matplotlib openpyxl
jupyter notebook Flood_Data_Analysis.ipynb
```

Make sure `nema-flood-data-06102022.xlsx` is in the same directory as the notebook, or update the file path in the first code cell.

## Policy Recommendation Summary

The brief recommends a community generated CI flood data platform over sensor expansion or infrastructure mitigation, citing higher scores across inclusion, popular control, transparency, and efficiency. The proposed rollout uses SMS, USSD, WhatsApp, and community focal points to feed geotagged, locally verified reports into a NEMA managed public dashboard, at an estimated pilot cost under $1 million across Lagos, Bayelsa, and Rivers states.

## References

Full citation list is included in the policy brief PDF, covering NEMA, NBS, UNDP, World Bank, World Weather Attribution, JICA, and academic sources on flood governance and CI platforms including Ushahidi.
