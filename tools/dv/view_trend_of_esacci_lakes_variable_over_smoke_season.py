r"""
view_trend_of_esacci_lakes_variable_over_smoke_season.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import argparse
import sys

from pathlib  import Path

# Related Third-party Imports
import matplotlib.pyplot as plt
import numpy             as np
import pandas            as pd

# Local Application/Library Specific Imports
from lib.dataframe.utils              import filter_df_by_column_bounds
from lib.esacci_lakes.utils.dataframe import (
    drop_hylak_field_columns_from_df,
    merge_dfs_on_esacci_lakes_id
)
from lib.esacci_lakes.utils.proc      import (
    add_argument_esacci_lakes_variable,
    add_argument_hylak_field,
    add_argument_esacci_lakes_hylak_fields_csv_path,
    argument_esacci_lakes_variable_is_in_esacci_lakes_variables,
    argument_hylak_field_is_in_hylak_fields,
    argument_esacci_lakes_hylak_fields_csv_path_exists,
    read_esacci_lakes_hylak_fields_csv
)
from lib.esacci_lakes.vars            import (
    ESACCI_LAKES_VARIABLES,
    HYLAK_FIELDS
)
from lib.plot.utils                   import (
    force_ax_xtick_visibility,
    save_figure
)
from lib.proc.vars                    import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)
from lib.time.utils                   import get_program_time

PROG  = "view_trend_of_esacci_lakes_variable_over_smoke_season.py"
TIME  = get_program_time()
FORMS = [
    "Absolute",
    "Anomaly"
]


# Argument functions
# ==================================================================================================
def add_argument_esacci_lakes_variable_over_high_smoke_season_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_variable_over_high_smoke_season_csv_path`
    argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `esacci_lakes_variable_over_high_smoke_season_csv_path` is
    of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_variable_over_high_smoke_season_csv_path",
        type = Path,
        help = """path to some csv file produced by comp_esacci_lakes_variable_over_smoke_season.py"""
    )


def argument_esacci_lakes_variable_over_high_smoke_season_csv_path_exists(
    esacci_lakes_variable_over_high_smoke_season_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_variable_over_high_smoke_season_csv_path`.

    Parameters
    ----------
    esacci_lakes_variable_over_high_smoke_season_csv_path : :class:`pathlib.Path`
        The argument
        `esacci_lakes_variable_over_high_smoke_season_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `esacci_lakes_variable_over_high_smoke_season_csv_path`
    exists. `False` otherwise.
    """
    if esacci_lakes_variable_over_high_smoke_season_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument esacci_lakes_variable_over_high_smoke_season_csv_path: no such file or directory: {esacci_lakes_variable_over_high_smoke_season_csv_path}""")

    return False


def read_esacci_lakes_variable_over_high_smoke_season_csv(
    esacci_lakes_variable_over_high_smoke_season_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_variable_over_high_smoke_season_csv_path` into a
    dataframe.

    Parameters
    ----------
    esacci_lakes_variable_over_high_smoke_season_csv_path : :class:`pathlib.Path`
        The path to some csv file as produced by
        comp_esacci_lakes_variable_over_smoke_season.py

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_variable_over_high_smoke_season_csv_path,
        index_col = "esacci_lakes_id"
    )


def add_argument_esacci_lakes_variable_over_low_smoke_season_csv_path(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `esacci_lakes_variable_over_low_smoke_season_csv_path`
    argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `esacci_lakes_variable_over_low_smoke_season_csv_path` is
    of type :class:`pathlib.Path`.
    """
    parser.add_argument(
        "esacci_lakes_variable_over_low_smoke_season_csv_path",
        type = Path,
        help = """path to some csv file produced by comp_esacci_lakes_variable_over_smoke_season.py"""
    )


def argument_esacci_lakes_variable_over_low_smoke_season_csv_path_exists(
    esacci_lakes_variable_over_low_smoke_season_csv_path: Path,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `esacci_lakes_variable_over_low_smoke_season_csv_path`.

    Parameters
    ----------
    esacci_lakes_variable_over_low_smoke_season_csv_path : :class:`pathlib.Path`
        The argument
        `esacci_lakes_variable_over_low_smoke_season_csv_path`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `esacci_lakes_variable_over_low_smoke_season_csv_path`
    exists. `False` otherwise.
    """
    if esacci_lakes_variable_over_low_smoke_season_csv_path.exists():
        return True

    if loud:
        print(f"""error: argument esacci_lakes_variable_over_low_smoke_season_csv_path: no such file or directory: {esacci_lakes_variable_over_low_smoke_season_csv_path}""")

    return False


def read_esacci_lakes_variable_over_low_smoke_season_csv(
    esacci_lakes_variable_over_low_smoke_season_csv_path: Path
) -> pd.DataFrame:
    """
    Reads `esacci_lakes_variable_over_low_smoke_season_csv_path` into a
    dataframe.

    Parameters
    ----------
    esacci_lakes_variable_over_low_smoke_season_csv_path : :class:`pathlib.Path`
        The path to some csv file as produced by
        comp_esacci_lakes_variable_over_smoke_season.py

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return pd.read_csv(
        esacci_lakes_variable_over_low_smoke_season_csv_path,
        index_col = "esacci_lakes_id"
    )


def add_argument_form(
    parser: argparse.ArgumentParser
) -> None:
    """
    Adds a `form` argument to a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    parser : :class:`argparse.ArgumentParser`
        The parser

    Returns
    -------
    None

    Notes
    -----
    Argument `form` is of type :class:`str`.
    """
    parser.add_argument(
        "-f", "--form",
        default = "Absolute",
        type    = str,
        choices = FORMS,
        help    = """the form of the input data. default=Absolute"""
    )


def argument_form_is_in_forms(
    form: str,
    *,
    loud: bool = False
) -> bool:
    """
    Validates `form`.

    Parameters
    ----------
    form : :class:`str`
        The argument `form`

    loud : :class:`bool`
        If `True`, prints an error message to stdout. default=False

    Returns
    -------
    `True` if `form` is in `FORMS`. `False` otherwise.
    """
    if form in FORMS:
        return True

    if loud:
        print(f"""error: argument form: not in {FORMS}: {form}""")

    return False


def build_parser(
    prog: str
) -> argparse.ArgumentParser:
    """
    Builds a :class:`argparse.ArgumentParser`.

    Parameters
    ----------
    prog : :class:`str`
        The program name

    Returns
    -------
    A :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog        = prog,
        usage       = "%(prog)s [options]",
        description = """"""
    )

    # Positional arguments
    add_argument_esacci_lakes_variable(parser)
    add_argument_esacci_lakes_variable_over_high_smoke_season_csv_path(parser)
    add_argument_esacci_lakes_variable_over_low_smoke_season_csv_path(parser)
    add_argument_hylak_field(parser)
    add_argument_esacci_lakes_hylak_fields_csv_path(parser)

    # Optional arguments
    add_argument_form(parser)

    return parser


def arguments_are_valid(
    args: argparse.Namespace
) -> bool:
    """
    Validates `args`.

    Returns
    -------
    `True` if all arguments are successfully validated. `False`
    otherwise.
    """
    if not argument_esacci_lakes_variable_is_in_esacci_lakes_variables(
        args.esacci_lakes_variable,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_variable_over_high_smoke_season_csv_path_exists(
        args.esacci_lakes_variable_over_high_smoke_season_csv_path,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_variable_over_low_smoke_season_csv_path_exists(
        args.esacci_lakes_variable_over_low_smoke_season_csv_path,
        loud = True
    ):
        return False

    if not argument_hylak_field_is_in_hylak_fields(
        args.hylak_field,
        loud = True
    ):
        return False

    if not argument_esacci_lakes_hylak_fields_csv_path_exists(
        args.esacci_lakes_hylak_fields_csv_path,
        loud = True
    ):
        return False

    if not argument_form_is_in_forms(
        args.form,
        loud = True
    ):
        return False

    return True


# ==================================================================================================


# Data functions
# ==================================================================================================
def convert_lakes_df_units_from_kelvin_to_celsius(
    lakes_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Converts `lakes_df`'s units from Kelvin to Celsius.

    Parameters
    ----------
    lakes_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.DataFrame`.
    """
    return lakes_df - 273.15


def get_lakes_df_week_number_ser_pairs(
    lakes_df: pd.DataFrame
) -> list[tuple[int, pd.Series]]:
    """
    Returns `lakes_df`'s week columns as (week number, series) pairs.

    Parameters
    ----------
    lakes_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A list of (week number, series) pairs.
    """
    prefix = "w_"
    pairs  = []

    for label_, ser in lakes_df.filter(like = prefix).items():
        n = int(label_.removeprefix(prefix)) # type: ignore

        if (
            n < -3
            or n > 20
        ):
            continue

        pairs.append((n, ser))

    return pairs


def get_lower_bounds_lakes_df(
    df:          pd.DataFrame,
    hylak_field: str
) -> pd.DataFrame:
    """
    Returns `df` filtered to lakes at or below `hylak_field`'s lower
    bound, with all `HYLAK_FIELDS` columns dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    hylak_field : :class:`str`
        The HydroLAKES field id

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Raises
    ------
    ValueError
        If `hylak_field`'s `lower_bound` is `None`.
    """
    if HYLAK_FIELDS[hylak_field].lower_bound is None:
        raise ValueError(f"expected `hylak_field` `{hylak_field}` to have a non-`None` `lower_bound`")

    filtered_df = filter_df_by_column_bounds(
        df     = df,
        column = hylak_field,
        lower  = None,
        upper  = HYLAK_FIELDS[hylak_field].lower_bound
    )

    return drop_hylak_field_columns_from_df(filtered_df)


def get_middle_bounds_lakes_df(
    df:          pd.DataFrame,
    hylak_field: str
) -> pd.DataFrame:
    """
    Returns `df` filtered to lakes between `hylak_field`'s lower and
    upper bounds, with all `HYLAK_FIELDS` columns dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    hylak_field : :class:`str`
        The HydroLAKES field id

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Raises
    ------
    ValueError
        If `hylak_field`'s `lower_bound` or `upper_bound` is `None`.
    """
    if HYLAK_FIELDS[hylak_field].lower_bound is None:
        raise ValueError(f"expected `hylak_field` `{hylak_field}` to have a non-`None` `lower_bound`")

    if HYLAK_FIELDS[hylak_field].upper_bound is None:
        raise ValueError(f"expected `hylak_field` `{hylak_field}` to have a non-`None` `upper_bound`")

    filtered_df = filter_df_by_column_bounds(
        df     = df,
        column = hylak_field,
        lower  = HYLAK_FIELDS[hylak_field].lower_bound,
        upper  = HYLAK_FIELDS[hylak_field].upper_bound
    )

    return drop_hylak_field_columns_from_df(filtered_df)


def get_upper_bounds_lakes_df(
    df:          pd.DataFrame,
    hylak_field: str
) -> pd.DataFrame:
    """
    Returns `df` filtered to lakes at or above `hylak_field`'s upper
    bound, with all `HYLAK_FIELDS` columns dropped.

    Parameters
    ----------
    df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    hylak_field : :class:`str`
        The HydroLAKES field id

    Returns
    -------
    A :class:`pandas.DataFrame`.

    Raises
    ------
    ValueError
        If `hylak_field`'s `upper_bound` is `None`.
    """
    if HYLAK_FIELDS[hylak_field].upper_bound is None:
        raise ValueError(f"expected `hylak_field` `{hylak_field}` to have a non-`None` `upper_bound`")

    filtered_df = filter_df_by_column_bounds(
        df     = df,
        column = hylak_field,
        lower  = HYLAK_FIELDS[hylak_field].upper_bound,
        upper  = None
    )

    return drop_hylak_field_columns_from_df(filtered_df)


def get_lakes_medians_ser(
    lakes_df: pd.DataFrame
) -> pd.Series:
    """
    Returns `lakes_df`'s week columns' medians.

    Parameters
    ----------
    lakes_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    Returns
    -------
    A :class:`pandas.Series`.
    """
    return pd.Series(
        {
            n: ser.median()
            for n, ser
            in get_lakes_df_week_number_ser_pairs(lakes_df)
        }
    )


# ==================================================================================================


# Plot functions
# ==================================================================================================
def plot_lakes_df_scatterplot(
    ax:       plt.Axes, # type: ignore
    lakes_df: pd.DataFrame,
    *,
    color: str,
    label: str | None = None
) -> None:
    """
    Plots a scatterplot of `lakes_df`'s week columns onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    lakes_df : :class:`pandas.DataFrame`
        The :class:`pandas.DataFrame`

    color : :class:`str`
        The point color

    label : :class:`str` | `None`
        The legend label

    Returns
    -------
    None
    """
    for n, ser in get_lakes_df_week_number_ser_pairs(lakes_df):
        ax.scatter(
            x          = [n] * len(ser),
            y          = ser,
            label      = label,
            color      = color,
            edgecolors = "none",
            alpha      = 0.1
        )


def plot_lakes_df_lineplot(
    ax:         plt.Axes, # type: ignore
    median_ser: pd.Series,
    *,
    color: str,
    label: str | None = None
) -> None:
    """
    Plots a line of `median_ser`'s values onto `ax`.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    median_ser : :class:`pandas.Series`
        A series of medians

    color : :class:`str`
        The line color

    label : :class:`str` | `None`
        The legend label

    Returns
    -------
    None
    """
    ax.plot(
        median_ser.index,
        median_ser,
        label  = label,
        color  = color,
        marker = "o"
    )


def plot_on_upper_bounds_lakes_ax(
    upper_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    upper_high_lakes_df:          pd.DataFrame,
    upper_low_lakes_df:           pd.DataFrame,
    upper_high_lakes_medians_ser: pd.Series,
    upper_low_lakes_medians_ser:  pd.Series
) -> None:
    """
    Plots `upper_high_lakes_df`, `upper_low_lakes_df`,
    `upper_high_lakes_medians_ser`, and `upper_low_lakes_medians_ser`
    onto `upper_bounds_lakes_ax`.

    Parameters
    ----------
    upper_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    upper_high_lakes_df : :class:`pandas.DataFrame`
        Upper-bounds-depth lakes during a high smoke season

    upper_low_lakes_df : :class:`pandas.DataFrame`
        Upper-bounds-depth lakes during a low smoke season

    upper_high_lakes_medians_ser : :class:`pandas.Series`
        `upper_high_lakes_df`'s weekly medians, as returned by
        `get_lakes_medians_ser`

    upper_low_lakes_medians_ser : :class:`pandas.Series`
        `upper_low_lakes_df`'s weekly medians, as returned by
        `get_lakes_medians_ser`

    Returns
    -------
    None
    """
    plot_lakes_df_scatterplot(
        upper_bounds_lakes_ax,
        upper_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        upper_bounds_lakes_ax,
        upper_high_lakes_medians_ser,
        color = "#FF0000",
        label = "High Smoke Season (Median)"
    )

    plot_lakes_df_scatterplot(
        upper_bounds_lakes_ax,
        upper_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        upper_bounds_lakes_ax,
        upper_low_lakes_medians_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Median)"
    )


def plot_on_middle_bounds_lakes_ax(
    middle_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    middle_high_lakes_df:          pd.DataFrame,
    middle_low_lakes_df:           pd.DataFrame,
    middle_high_lakes_medians_ser: pd.Series,
    middle_low_lakes_medians_ser:  pd.Series
) -> None:
    """
    Plots `middle_high_lakes_df`, `middle_low_lakes_df`,
    `middle_high_lakes_medians_ser`, and `middle_low_lakes_medians_ser`
    onto `middle_bounds_lakes_ax`.

    Parameters
    ----------
    middle_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    middle_high_lakes_df : :class:`pandas.DataFrame`
        Middle-bounds-depth lakes during a high smoke season

    middle_low_lakes_df : :class:`pandas.DataFrame`
        Middle-bounds-depth lakes during a low smoke season

    middle_high_lakes_medians_ser : :class:`pandas.Series`
        `middle_high_lakes_df`'s weekly medians, as returned by
        `get_lakes_medians_ser`

    middle_low_lakes_medians_ser : :class:`pandas.Series`
        `middle_low_lakes_df`'s weekly medians, as returned by
        `get_lakes_medians_ser`

    Returns
    -------
    None
    """
    plot_lakes_df_scatterplot(
        middle_bounds_lakes_ax,
        middle_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        middle_bounds_lakes_ax,
        middle_high_lakes_medians_ser,
        color = "#FF0000",
        label = "High Smoke Season (Median)"
    )

    plot_lakes_df_scatterplot(
        middle_bounds_lakes_ax,
        middle_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        middle_bounds_lakes_ax,
        middle_low_lakes_medians_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Median)"
    )


def plot_on_lower_bounds_lakes_ax(
    lower_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    lower_high_lakes_df:          pd.DataFrame,
    lower_low_lakes_df:           pd.DataFrame,
    lower_high_lakes_medians_ser: pd.Series,
    lower_low_lakes_medians_ser:  pd.Series
) -> None:
    """
    Plots `lower_high_lakes_df`, `lower_low_lakes_df`,
    `lower_high_lakes_medians_ser`, and `lower_low_lakes_medians_ser`
    onto `lower_bounds_lakes_ax`.

    Parameters
    ----------
    lower_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to plot onto

    lower_high_lakes_df : :class:`pandas.DataFrame`
        Lower-bounds-depth lakes during a high smoke season

    lower_low_lakes_df : :class:`pandas.DataFrame`
        Lower-bounds-depth lakes during a low smoke season

    lower_high_lakes_medians_ser : :class:`pandas.Series`
        `lower_high_lakes_df`'s weekly medians, as returned by
        `get_lakes_medians_ser`

    lower_low_lakes_medians_ser : :class:`pandas.Series`
        `lower_low_lakes_df`'s weekly medians, as returned by
        `get_lakes_medians_ser`

    Returns
    -------
    None
    """
    plot_lakes_df_scatterplot(
        lower_bounds_lakes_ax,
        lower_high_lakes_df,
        color = "#FF0000"
    )
    plot_lakes_df_lineplot(
        lower_bounds_lakes_ax,
        lower_high_lakes_medians_ser,
        color ="#FF0000",
        label = "High Smoke Season (Median)"
    )

    plot_lakes_df_scatterplot(
        lower_bounds_lakes_ax,
        lower_low_lakes_df,
        color = "#0000FF"
    )
    plot_lakes_df_lineplot(
        lower_bounds_lakes_ax,
        lower_low_lakes_medians_ser,
        color = "#0000FF",
        label = "Low Smoke Season (Median)"
    )


def set_upper_bounds_lakes_ax_properties(
    upper_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    form:                  str
) -> None:
    """
    Sets `upper_bounds_lakes_ax`'s properties.

    Parameters
    ----------
    upper_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    hylak_field_upper_bound         = HYLAK_FIELDS[hylak_field].upper_bound
    hylak_field_upper_bound_display = hylak_field_upper_bound / hylak_field_display_scale # type: ignore
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    upper_bounds_lakes_ax.set_title(f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} >= {hylak_field_upper_bound_display:g} {hylak_field_display_units}""")
    upper_bounds_lakes_ax.set_xlabel("Week relative to start of smoke season")
    upper_bounds_lakes_ax.set_ylabel(f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""")
    upper_bounds_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(upper_bounds_lakes_ax)


def set_middle_bounds_lakes_ax_properties(
    middle_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    form:                  str
) -> None:
    """
    Sets `middle_bounds_lakes_ax`'s properties.

    Parameters
    ----------
    middle_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_lower_bound         = HYLAK_FIELDS[hylak_field].lower_bound
    hylak_field_upper_bound         = HYLAK_FIELDS[hylak_field].upper_bound
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    hylak_field_lower_bound_display = hylak_field_lower_bound / hylak_field_display_scale # type: ignore
    hylak_field_upper_bound_display = hylak_field_upper_bound / hylak_field_display_scale # type: ignore
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    middle_bounds_lakes_ax.set_title(f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} between {hylak_field_lower_bound_display:g} {hylak_field_display_units} and {hylak_field_upper_bound_display:g} {hylak_field_display_units}""")
    middle_bounds_lakes_ax.set_xlabel("Week relative to start of smoke season")
    middle_bounds_lakes_ax.set_ylabel(f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""")
    middle_bounds_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(middle_bounds_lakes_ax)


def set_lower_bounds_lakes_ax_properties(
    lower_bounds_lakes_ax: plt.Axes, # type: ignore
    *,
    esacci_lakes_variable: str,
    hylak_field:           str,
    form:                  str
) -> None:
    """
    Sets `lower_bounds_lakes_ax`'s properties.

    Parameters
    ----------
    lower_bounds_lakes_ax : :class:`matplotlib.axes.Axes`
        The axes to set properties on

    esacci_lakes_variable : :class:`str`
        The ESA CCI Lakes variable id

    hylak_field : :class:`str`
        The HydroLAKES field id

    form : :class:`str`
        The form of the input data. One of `FORMS`

    Returns
    -------
    None
    """
    esacci_lakes_variable_long_name = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name
    esacci_lakes_variable_units     = ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units
    hylak_field_long_name           = HYLAK_FIELDS[hylak_field].long_name
    hylak_field_lower_bound         = HYLAK_FIELDS[hylak_field].lower_bound
    hylak_field_display_units       = HYLAK_FIELDS[hylak_field].display_units or HYLAK_FIELDS[hylak_field].units
    hylak_field_display_scale       = HYLAK_FIELDS[hylak_field].display_scale or HYLAK_FIELDS[hylak_field].scale
    hylak_field_lower_bound_display = hylak_field_lower_bound / hylak_field_display_scale # type: ignore
    form_qualifier                  = "" if form == "Absolute" else f" {form}"

    lower_bounds_lakes_ax.set_title(f"""Weekly {esacci_lakes_variable_long_name}{form_qualifier} for lakes with {hylak_field_long_name} <= {hylak_field_lower_bound_display:g} {hylak_field_display_units}""")
    lower_bounds_lakes_ax.set_xlabel("Week relative to start of smoke season")
    lower_bounds_lakes_ax.set_ylabel(f"""{esacci_lakes_variable_long_name} ({esacci_lakes_variable_units}){form_qualifier}""")
    lower_bounds_lakes_ax.set_xticks(np.arange(-3, 21).tolist())

    force_ax_xtick_visibility(lower_bounds_lakes_ax)


# ==================================================================================================


def write_lakes_df_to_csv(
    lakes_df: pd.DataFrame,
    prog:     str,
    time:     str,
    name:     str
) -> None:
    """
    Writes `lakes_df` to `{prog}/`.

    Parameters
    ----------
    lakes_df : :class:`pandas.DataFrame`
        The dataframe

    prog : :class:`str`
        The program name

    time : :class:`str`
        The program time

    name : :class:`str`
        The output file name

    Returns
    -------
    None
    """
    fdir = Path(f"data/dv/{prog}_{time}")

    fdir.mkdir(
        parents  = True,
        exist_ok = True
    )

    lakes_df.to_csv(fdir / (name + ".csv"))


def main(
) -> int:
    """
    Orchestration layer.
    """
    args = build_parser(PROG).parse_args()

    if not arguments_are_valid(args):
        return RETURN_FAILURE

    variable_over_high_smoke_season_df = read_esacci_lakes_variable_over_high_smoke_season_csv(args.esacci_lakes_variable_over_high_smoke_season_csv_path)
    variable_over_low_smoke_season_df  = read_esacci_lakes_variable_over_low_smoke_season_csv(args.esacci_lakes_variable_over_low_smoke_season_csv_path)
    hylak_fields_df                    = read_esacci_lakes_hylak_fields_csv(args.esacci_lakes_hylak_fields_csv_path)

    if (
        args.form == "Absolute"
        and args.esacci_lakes_variable == "lake_surface_water_temperature"
    ):
        variable_over_high_smoke_season_df = convert_lakes_df_units_from_kelvin_to_celsius(variable_over_high_smoke_season_df)
        variable_over_low_smoke_season_df  = convert_lakes_df_units_from_kelvin_to_celsius(variable_over_low_smoke_season_df)

    variable_over_high_smoke_season_hylak_fields_df = merge_dfs_on_esacci_lakes_id(
        variable_over_high_smoke_season_df,
        hylak_fields_df
    )
    variable_over_low_smoke_season_hylak_fields_df  = merge_dfs_on_esacci_lakes_id(
        variable_over_low_smoke_season_df,
        hylak_fields_df
    )

    upper_high_lakes_df  = get_upper_bounds_lakes_df(
        variable_over_high_smoke_season_hylak_fields_df,
        args.hylak_field
    )
    upper_low_lakes_df   = get_upper_bounds_lakes_df(
        variable_over_low_smoke_season_hylak_fields_df,
        args.hylak_field
    )
    middle_high_lakes_df = get_middle_bounds_lakes_df(
        variable_over_high_smoke_season_hylak_fields_df,
        args.hylak_field
    )
    middle_low_lakes_df  = get_middle_bounds_lakes_df(
        variable_over_low_smoke_season_hylak_fields_df,
        args.hylak_field
    )
    lower_high_lakes_df  = get_lower_bounds_lakes_df(
        variable_over_high_smoke_season_hylak_fields_df,
        args.hylak_field
    )
    lower_low_lakes_df   = get_lower_bounds_lakes_df(
        variable_over_low_smoke_season_hylak_fields_df,
        args.hylak_field
    )

    upper_high_lakes_medians_ser  = get_lakes_medians_ser(upper_high_lakes_df)
    upper_low_lakes_medians_ser   = get_lakes_medians_ser(upper_low_lakes_df)
    middle_high_lakes_medians_ser = get_lakes_medians_ser(middle_high_lakes_df)
    middle_low_lakes_medians_ser  = get_lakes_medians_ser(middle_low_lakes_df)
    lower_high_lakes_medians_ser  = get_lakes_medians_ser(lower_high_lakes_df)
    lower_low_lakes_medians_ser   = get_lakes_medians_ser(lower_low_lakes_df)

    fig, (
        upper_bounds_lakes_ax,
        middle_bounds_lakes_ax,
        lower_bounds_lakes_ax
    ) = plt.subplots(
        nrows   = 3,
        ncols   = 1,
        sharex  = True,
        sharey  = True,
        figsize = (12.8, 14.4)
    )
    plt.subplots_adjust(hspace = 0.25)

    plot_on_upper_bounds_lakes_ax(
        upper_bounds_lakes_ax,
        upper_high_lakes_df          = upper_high_lakes_df,
        upper_low_lakes_df           = upper_low_lakes_df,
        upper_high_lakes_medians_ser = upper_high_lakes_medians_ser,
        upper_low_lakes_medians_ser  = upper_low_lakes_medians_ser
    )
    plot_on_middle_bounds_lakes_ax(
        middle_bounds_lakes_ax,
        middle_high_lakes_df          = middle_high_lakes_df,
        middle_low_lakes_df           = middle_low_lakes_df,
        middle_high_lakes_medians_ser = middle_high_lakes_medians_ser,
        middle_low_lakes_medians_ser  = middle_low_lakes_medians_ser
    )
    plot_on_lower_bounds_lakes_ax(
        lower_bounds_lakes_ax,
        lower_high_lakes_df          = lower_high_lakes_df,
        lower_low_lakes_df           = lower_low_lakes_df,
        lower_high_lakes_medians_ser = lower_high_lakes_medians_ser,
        lower_low_lakes_medians_ser  = lower_low_lakes_medians_ser
    )

    set_upper_bounds_lakes_ax_properties(
        upper_bounds_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        form                  = args.form
    )
    set_middle_bounds_lakes_ax_properties(
        middle_bounds_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        form                  = args.form
    )
    set_lower_bounds_lakes_ax_properties(
        lower_bounds_lakes_ax,
        esacci_lakes_variable = args.esacci_lakes_variable,
        hylak_field           = args.hylak_field,
        form                  = args.form
    )

    upper_bounds_lakes_ax.legend()
    middle_bounds_lakes_ax.legend()
    lower_bounds_lakes_ax.legend()

    save_figure(
        fig,
        PROG,
        TIME,
        "figure"
    )

    write_lakes_df_to_csv(
        upper_high_lakes_df,
        PROG,
        TIME,
        "upper_high_lakes"
    )
    write_lakes_df_to_csv(
        upper_low_lakes_df,
        PROG,
        TIME,
        "upper_low_lakes"
    )
    write_lakes_df_to_csv(
        middle_high_lakes_df,
        PROG,
        TIME,
        "middle_high_lakes"
    )
    write_lakes_df_to_csv(
        middle_low_lakes_df,
        PROG,
        TIME,
        "middle_low_lakes"
    )
    write_lakes_df_to_csv(
        lower_high_lakes_df,
        PROG,
        TIME,
        "lower_high_lakes"
    )
    write_lakes_df_to_csv(
        lower_low_lakes_df,
        PROG,
        TIME,
        "lower_low_lakes"
    )

    return RETURN_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
