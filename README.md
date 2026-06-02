# WFEL
General repository for the Wildfire Engineering Laboratory @ Universtiy of Nevada, Reno

## 1.0

### Introduction

### Scope
The objective of this project is to produce, for each of the variables grouped under the Lakes ECV, a dataset comprising monthly mean values spanning September 1992 – December 2023, wherein each record corresponds to a single lake within the candidate set.

> [!note]
> This project relies upon data sourced from the [ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0](https://catalogue.ceda.ac.uk/uuid/a56dba09df8a42ec9fba8b8c7a5e1f69/).

#### Candidate Set Selection
 Candidate lakes are identified by filtering the [lakescci_v2.1_metadata](https://climate.esa.int/documents/2607/lakescci_v2.1.0_metadata.csv) file to retain only those records whose `country` field contains either `Canada` or `United States`:

```RBQL
SELECT * WHERE like(a4, '%United States%') || like(a4, '%Canada%')
```

The resulting candidate set comprises 667 lakes.

> [!note]
> Although the [lakescci_v2.1_metadata](https://climate.esa.int/documents/2607/lakescci_v2.1.0_metadata.csv) file was published alongside the [ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 2.1](https://catalogue.ceda.ac.uk/uuid/7fc9df8070d34cacab8092e45ef276f1/), its use extends to [Version 3.0](https://catalogue.ceda.ac.uk/uuid/a56dba09df8a42ec9fba8b8c7a5e1f69/).