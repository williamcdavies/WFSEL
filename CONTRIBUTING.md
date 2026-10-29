## Style Guide: Python
If anything is not explicitly documented by this style guide refer back to [PEP8](https://peps.python.org/pep-0008/).

### File Headers
File headers should be of the following format:

```python
"""
Filename:   <filename>
Author:     <author>
Modified:   <date>
"""
```

The filename field should include the file's extension. If the file belongs to a module, the filename field should be written as a dot-separated module path, e.g. `wfsel.exit_codes.py`. The author field should match the author name field under `[project]` in `pyproject.toml`. The modified field should be of the format `DD/MM/YY`. The file header should be followed by exactly one newline.

> Example
> 
> ```python
> """
> Filename:   wfsel.exit_codes.py
> Author:     William Chuter-Davies
> Modified:   27/10/26
> """
> ```

### Imports
Imports fall under the following three categories:
1. Standard Library Imports
2. Related Third-party Imports
3. Local Application/Library Specific Imports

These categories should be explicitly documented:

```python
# Standard Library Imports

# Related Third-party Imports

# Local Application/Library Specific Imports
```

Imports should be ordered alphabetically within each category. `import X` style imports should be separated from `from X import Y` style imports by exactly one newline. Categories with no imports should not be included.

### Classes

#### Dataclasses
Dataclasses should be of the following template:

```python
@dataclass(kw_only = True)
class <class_name>:
    """Encapsulate a <class_name>."""

    <parameter_name>:   <parameter_type>
    <parameter_name>:   <parameter_type>
    <parameter_name>:   <parameter_type>
```

### Functions

### Internal Functions
Internal functions are functions defined within another function's body. Internal functions should be prefixed with an underscore.

#### Argument Functions
Argument functions should be of the following template:

```python
def add_argument_<argument_name>(
    parser: ArgumentParser,
) -> None:
    """
    Add a "<argument_name>" argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser
    """
    parser.add_argument(
        "<argument_name>",
        type = <argument_type>
    )
```

##### Optional Argument Functions
Either `required = True` or `required = False` should be passed to the `add_argument` call within an optional argument function.

#### Reader Functions
Reader functions should be of the following template:

```python
def read_<file_name>_<file_extension>(
    <file_name>_<file_extension>_path: Path,
) -> pd.DataFrame:
    """
    Read "<file_name>.<file_extension>" (or similar) into a dataframe.

    Parameters
    ----------
    <file_name>_<file_extension>_path : Path
        The path to "<file_name>.<file_extension>" (or similar)

    Returns
    -------
    pd.DataFrame
        A dataframe
    """
    df  = pd.read_csv(
            <file_name>_<file_extension>_path,
            index_col = "id",
        )

    return df
```

### Docstrings
Class- and function-level docstrings should be in numpy format. The primary description of a class or function should be a single sentence. If it cannot be reasonably stated in a single sentence, the class or function may be too complex.

Shorthand should not be used within a docstring. Write "directory", not "dir", "column", not "col", and "dataframe", not "df", etc.

#### Parameters
Parameter descriptions should start with "The".

If the parameter name ends with a type suffix, e.g. "df", "ser", "ds", "da", etc., the description of that parameter should end with the full name of that type, e.g. "dataframe", "series", "dataset", "dataarray", etc.

##### Common Parameters

###### Abstract Parameters
```python
"""
ax : Axes
    The axes
connection : psycopg.Connection
    The connection
df : pd.DataFrame
    The dataframe
fig : Figure
    The figure
gdf : gpd.GeoDataFrame
    The geodataframe
ser : pd.Series
    The series
"""
```

###### Argument Parameters
```python
"""
arguments : Namespace
    The arguments
parser : ArgumentParser
    The parser
"""
```

###### ESA CCI Lakes Parameters
```python
"""
distinct_labels_ser : pd.Series[int]
    The distinct labels series
esacci_lakes_counts_of_distinct_start_days_by_year_df : pd.DataFrame
    The ESA CCI Lakes counts of distinct start days by year
    dataframe
esacci_lakes_counts_of_distinct_start_days_by_year_df_long : pd.DataFrame
    The unpivoted ESA CCI Lakes counts of distinct start days by
    year dataframe
esacci_lakes_id : int
    The ESA CCI Lakes id
esacci_lakes_merged_product_dir_path : Path
    The ESA CCI Lakes merged product directory path
esacci_lakes_merged_product_ds : xr.Dataset
    The ESA CCI Lakes merged product dataset
esacci_lakes_metadata_df : pd.DataFrame
    The ESA CCI Lakes metadata dataframe
esacci_lakes_static_lake_mask_ds : xr.Dataset
    The ESA CCI Lakes static lake mask dataset
observations : list[pd.Series[float]]
    The list of observations series
observations_ser : pd.Series[float]
    The observations series
"""
```

###### IO Parameters 
```python
"""
dir_path : Path
    The directory path
output_file_path : Path
    The output file path
"""
```

#### Returns
Return descriptions should start with "A" or "An".

### Formatting

#### Tab-alignment
Where consecutive lines share a common structure, the right-hand side of each line should be aligned to a common column using tabs. This applies to, but is not limited to: type hints in dataclass fields, `as` aliases in import statements, `=` assignments, and keyword arguments.

### Scripts
Scripts should be of the following template:

```python
"""
Filename:   <filename>
Author:     <author>
Modified:   <date>
"""

# <imports>

PROG    = "<filename>"
DESC    = "<description>"


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    ...


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    ...


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main(
) -> int:
    ...


if __name__ == "__main__":
    sys.exit(main())

```

#### `build_parser`
`build_parser` should wrap `wfsel.utils.argparse_utils.build_parser`. It should construct an `ArgumentParser` from `PROG`, `DESC`, and `usage = "%(prog)s [options]"`, pass it to `wfsel.utils.argparse_utils.build_parser` alongside the script’s positional and optional argument functions, and return the result.

`build_parser` should have the following docstring:

```python
"""
Wrap _build_parser.

Returns
-------
ArgumentParser
    A parser
"""
```

#### `arguments_are_valid`
`arguments_are_valid` should wrap `wfsel.utils.argparse_utils.arguments_are_valid`. It should construct an argument name to validator mapping, pass it to `wfsel.utils.argparse_utils.arguments_are_valid`, and return the result.

`arguments_are_valid` should have the following docstring:

```python
"""
Wrap _arguments_are_valid.

Parameters
----------
arguments : Namespace
    The arguments

Returns
-------
bool
    True if all arguments are valid, False otherwise
"""
```

#### `main`
The first four lines of `main` should be:

```python
args = build_parser().parse_args()

if not arguments_are_valid(args):
    return EXIT_FAILURE
```

`EXIT_FAILURE` and `EXIT_SUCCESS` can be sourced from `wfsel.exit_codes`.

`main` should have the following docstring:

```python
"""
Run program.

Returns
-------
int
    0 if program runs successfully, 1 otherwise
"""
```
