## Style Guide: Python
If anything is not explicitly documented by this style guide refer back to [PEP8](https://peps.python.org/pep-0008/).

### File Headers
File headers should be of the following format:

```python
"""
Filename:   <filename>
Author:     <author>
"""
```

The filename field should include the file's extension. If the file belongs to a module, the filename field should be written as a dot-separated module path, e.g. `wfsel.exit_codes.py`. The author field should match the author name field under `[project]` in `pyproject.toml`. The file header should be followed by exactly one newline.

> Example
> 
> ```python
> """
> Filename:   wfsel.exit_codes.py
> Author:     William Chuter-Davies
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

#### Internal Functions
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

`metavar = <metavar>` shoould be passed to the `add_argument` call for all arguments that accept a value.

#### Calling Functions
Function calls should not be nested, except in which the assignment of an intermediate variable would not aid debugging, e.g. `sys.exit(main())`.

> Example
>
> ```python
> # correct
> file_paths          = dir_path.glob(f"**/*.{extension}")
> sorted_file_paths   = sorted(file_paths)
>
> # incorrect
> sorted_file_paths = sorted(dir_path.glob(f"**/*.{extension}"))
> ```

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
            index_col = <index_col>,
        )

    return df
```

### Docstrings
Class- and function-level docstrings should be in numpy format. The primary description of a class or function should be a single sentence. If it cannot be reasonably stated in a single sentence, the class or function may be too complex.

Shorthand should not be used within a docstring. Write "directory", not "dir", "column", not "col", and "dataframe", not "df", etc.

#### Parameters
Parameter descriptions should start with "The".

If the parameter name ends with a type suffix, e.g. "df", "ser", "ds", "da", etc., the description of that parameter should end with the full name of that type, e.g. "dataframe", "series", "dataset", "dataarray", etc.

#### Returns
Return descriptions should start with "A" or "An".

### Scripts
Scripts should be of the following template:

```python
"""
Filename:   <filename>
Author:     <author>
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

### Naming

#### Suffixes
Variable suffixes should be used for complex types or in such instances where the type of a variable cannot be inferred from context.

> example
> ```python
> observations_ser        # pd.Series[float]          — type not clear from name alone
> observations_ser_list   # list[pd.Series[float]]    — type not clear from name alone
> years                   # list[int]                 — pluralisation is sufficient
> ```

The following suffixes are expected and should be used:

| Suffix | Type                       |
|:------ |:-------------------------- |
| `df`   | `pandas.DataFrame`         |
| `ser`  | `pandas.Series`            |
| `gdf`  | `geopandas.GeoDataFrame`   |
| `ds`   | `xarray.Dataset`           |
| `da`   | `xarray.DataArray`         |
| `ax`   | `matplotlib.Axes.Axes`     |
| `fig`  | `matplotlib.Figure.Figure` |
