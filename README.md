## Introduction

### Scope
The objective of this project is to produce, for each day in September 1992–December 2023, a dataset comprising mean, median, variance, minimum, and maximum values for each of the Lakes Essential Climate Variables in `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR', 'phycocyanin', 'lake_surface_water_temperature', 'lake_surface_water_extent']` wherein each record corresponds to a single lake within the candidate set.

> [!note]
> This project depends upon data sourced from the [ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 3.0](https://catalogue.ceda.ac.uk/uuid/a56dba09df8a42ec9fba8b8c7a5e1f69/).

### The Candidate Set
The candidate set is identified by filtering the [lakescci_v2.1_metadata.csv](https://climate.esa.int/documents/2607/lakescci_v2.1.0_metadata.csv) file to retain only those records whose `country` field contains either `Canada` or `United States`:

```RBQL
SELECT * WHERE like(a4, '%United States%') || like(a4, '%Canada%')
```

The candidate set comprises 667 North American lakes.

> [!note]
> Although the lakescci_v2.1_metadata.csv file was published alongside the [ESA Lakes Climate Change Initiative (Lakes_cci): Lake products, Version 2.1](https://catalogue.ceda.ac.uk/uuid/7fc9df8070d34cacab8092e45ef276f1/), its use extends to Version 3.0.

## Code

### Introduction
The project repository can be found [here](https://github.com/williamcdavies/WFSEL/tree/main). The program entry point is [main.py](https://github.com/williamcdavies/WFSEL/blob/main/main.py).

> [!note]
> main.py is atomic. It produces a single output from a minimum working set of inputs. For workflows that require multiple outputs, batch processing is recommended.

### main.py

#### Description
The purpose of main.py is to produce a .csv file containing mean, median, variance, maximum, and minimum values for each Lakes ECV in `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR', 'phycocyanin', 'lake_surface_water_temperature', 'lake_surface_water_extent']` for each lake within the candidate set given an ESA Lakes_cci v3.0 dataset, ESA_CCI_static_lake_mask.nc, lakescci_v2.1_metadata.csv, and an output destination.

#### Strategy
1. Open the ESA Lakes CCI v3.0 dataset as an `xarray.DataSet`
2. Open the ESA_CCI_static_lake_mask.nc dataset as an `xarray.DataSet `
3. Open the lakescci_v2.1_metadata.csv file as a `pandas.DataFrame`
4. For each row in lakescci_v2.1_metadata.csv:
    1. Use `lat_max_box`, `lat_min_box`, `lon_max_box`, and `lon_min_box` to define the lake's bounding box
    2. Clip the ESA Lakes CCI v3.0 DataSet to the lake's bounding box
    3. Clip the ESA_CCI_static_lake_mask.nc DataSet to the lake's bounding box
    4. Create a lake geometry mask using the ESA_CCI_static_lake_mask DataSet
    5. For each Lakes ECV in `['chla', 'tsm', 'acdom440', 'Kd490', 'KdPAR', 'phycocyanin', 'lake_surface_water_temperature', 'lake_surface_water_extent']`:
        1. Apply the geometry mask against the clipped Lakes CCI v3.0 DataSet to extract the Lakes ECV values within the lake
        2. Calculate the `numpy.nanmean`, `numpy.nanmedian`, `numpy.nanvar`, `numpy.nanmax`, and `numpy.nanmin` of the extracted values
        3. Write the statistics to the output destination

#### Input
main.py takes four arguments:
1. `lakes_cci_merg_prod_nc_path`: The path to an [ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-YYYYMMDD-fv3.0.0.nc](https://dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/merged_product/) file
2. `lakes_cci_stat_mask_nc_path`: The path to the [ESA_CCI_static_lake_mask.nc](https://dap.ceda.ac.uk/neodc/esacci/lakes/data/lake_products/L3S/v3.0/ESA_CCI_static_lake_mask.nc) file
3. `csv_path`: The path to the lakescci_v2.1_metadata.csv file.
4. `dst_path`: The destination path.

> [!note]
> `dst_path` must point to a .csv file.

> [!note]
> main.py is compatible with any subset of lakescci_v2.1.0_metadata.csv.

> [!example]
> ```sh
> >>> python main.py ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-20230101-fv3.0.0.nc ESA_CCI_static_lake_mask.nc lakescci_v2.1.0_metadata_filtered ./ESACCI-LAKES-L3S-OUTPUT-20230101-fv3.0.0.csv
> ```

#### Output
A 668x41 .csv file with the following structure:

| id       | chla_mean | chla_median | chla_var  | chla_max  | chla_min  | $\cdots$ | lake_surface_water_extent_min |
|:-------- |:--------- |:----------- |:--------- |:--------- |:--------- |:-------- |:----------------------------- |
| 1        | `float64` | `float64`   | `float64` | `float64` | `float64` | $\cdots$ | `float64`                     |
| $\vdots$ | $\vdots$  | $\vdots$    | $\vdots$  | $\vdots$  | $\vdots$  | $\ddots$ | $\vdots$                      |
| 667      | `float64` | `float64`   | `float64` | `float64` | `float64` | $\cdots$ | `float64`                     |

#### Dependencies
main.py  depends upon `Python >= 3.14` and the following packages:
- [`numpy  >= 2.5.0`](https://pypi.org/project/geopandas/)
- [`pandas >= 3.0.3`](https://pypi.org/project/netCDF4/)
- [`tqdm   >= 4.68.3`](https://pypi.org/project/rasterio/)
- [`xarray >= 2026.4.0`](https://pypi.org/project/xarray/)

> [!note]
> This list specifies program dependencies for main.py. For a list of repository dependencies, see [pyproject.toml](https://github.com/williamcdavies/WFSEL/blob/main/pyproject.toml). For a complete list of repository dependencies and sub-dependencies, see [requirements.txt](https://github.com/williamcdavies/WFSEL/blob/main/requirements.txt).

