r"""
variable_windows.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import ast
import sys

from argparse   import (
                    ArgumentParser,
                    Namespace,
                )
from pathlib    import Path

# Related Third-party Imports
import pandas as pd

# Local Application/Library Specific Imports
from wfsel.exit_codes                       import (
                                                EXIT_FAILURE,
                                                EXIT_SUCCESS,
                                            )
from wfsel.io.arguments                     import add_argument_output
from wfsel.io.writers                       import to_csv
from wfsel.sources.esacci_lakes.arguments   import (
                                                add_argument_esacci_lakes_metadata_csv_path,
                                                add_argument_esacci_lakes_hylak_field_values_csv_path,
                                            )
from wfsel.sources.esacci_lakes.readers     import (
                                                read_esacci_lakes_metadata_csv,
                                                read_esacci_lakes_hylak_field_values_csv,
                                            )
from wfsel.utils.argparse_utils             import (
                                                arguments_are_valid as _arguments_are_valid,
                                                build_parser        as _build_parser,
                                                argument_is_file,
                                            )

PROG        = "variable_windows.py"
DESC        = ""
GROUPS      = [
                "lower",
                "middle",
                "upper",
              ]
LOWER_BOUND = 0.5e9
UPPER_BOUND = 5e9


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def add_argument_group_high_lakes_csv_path(
    parser: ArgumentParser,
    *,
    group: str,
) -> None:
    parser.add_argument(
        f"{group}_high_lakes_csv_path",
        type = Path,
        help = f"path to the {group}-volume high-smoke-season lakes csv file",
    )


def add_argument_group_low_lakes_csv_path(
    parser: ArgumentParser,
    *,
    group: str,
) -> None:
    parser.add_argument(
        f"{group}_low_lakes_csv_path",
        type = Path,
        help = f"path to the {group}-volume low-smoke-season lakes csv file",
    )


def add_argument_group_summary_csv_path(
    parser: ArgumentParser,
    *,
    group: str,
) -> None:
    parser.add_argument(
        f"{group}_summary_csv_path",
        type = Path,
        help = f"path to the {group}-volume summary csv file",
    )


def build_parser(
) -> ArgumentParser:
    parser  = ArgumentParser(
                prog        = PROG,
                description = DESC,
                usage       = "%(prog)s [options]",
            )
    parser  = _build_parser(
                parser,
                positional_arguments    = [
                    add_argument_esacci_lakes_metadata_csv_path,
                    add_argument_esacci_lakes_hylak_field_values_csv_path,
                ],
                optional_arguments      = [
                    add_argument_output,
                ],
            )

    for group in GROUPS:
        add_argument_group_high_lakes_csv_path(parser, group=group)
        add_argument_group_low_lakes_csv_path(parser, group=group)
        add_argument_group_summary_csv_path(parser, group=group)

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    argument_name_to_validator  = {
                                    "esacci_lakes_metadata_csv_path":               argument_is_file,
                                    "esacci_lakes_hylak_field_values_csv_path":     argument_is_file,
                                    **{
                                        f"{group}_{suffix}": argument_is_file
                                        for group in GROUPS
                                        for suffix in (
                                            "high_lakes_csv_path",
                                            "low_lakes_csv_path",
                                            "summary_csv_path",
                                        )
                                    },
                                }

    boolean = _arguments_are_valid(
                arguments,
                argument_name_to_validator,
            )

    return boolean


# ----------------------------------------------------------------------
# read functions
# ----------------------------------------------------------------------
def read_lakes_csv(
    path: Path,
) -> pd.DataFrame:
    return pd.read_csv(
        path,
        index_col = "esacci_lakes_id",
    )


def read_summary_csv(
    path: Path,
) -> pd.DataFrame:
    return pd.read_csv(path)


# ----------------------------------------------------------------------
# data functions
# ----------------------------------------------------------------------
def get_longest_cluster(
    summary_df: pd.DataFrame,
) -> list[int]:
    return ast.literal_eval(summary_df["longest_cluster_weeks"].iloc[0])


def get_volume_group(
    vol_total_m3: float,
) -> str:
    if vol_total_m3 <= LOWER_BOUND:
        return "lower"

    if vol_total_m3 >= UPPER_BOUND:
        return "upper"

    return "middle"


def get_esacci_lakes_mean_delta(
    esacci_lakes_id:                                int,
    *,
    esacci_lakes_variable_over_high_smoke_season_df: pd.DataFrame,
    esacci_lakes_variable_over_low_smoke_season_df:  pd.DataFrame,
    weeks:                                           list[int],
) -> tuple[float, int] | None:
    if not weeks:
        return None

    if (
        esacci_lakes_id not in esacci_lakes_variable_over_high_smoke_season_df.index
        or esacci_lakes_id not in esacci_lakes_variable_over_low_smoke_season_df.index
    ):
        return None

    columns = [f"w_{week}" for week in weeks]

    high    = esacci_lakes_variable_over_high_smoke_season_df.loc[esacci_lakes_id, columns]
    low     = esacci_lakes_variable_over_low_smoke_season_df.loc[esacci_lakes_id, columns]
    diff    = high - low

    return diff.mean(), diff.notna().sum()


def get_esacci_lakes_deltas_df(
    esacci_lakes_metadata_df:       pd.DataFrame,
    *,
    esacci_lakes_hylak_fields_df:   pd.DataFrame,
    high_lakes_dfs_by_group:        dict[str, pd.DataFrame],
    low_lakes_dfs_by_group:         dict[str, pd.DataFrame],
    weeks_by_group:                 dict[str, list[int]],
) -> pd.DataFrame:
    records = []

    for id_, row in esacci_lakes_metadata_df.iterrows():
        hylak_fields_row    = esacci_lakes_hylak_fields_df.loc[id_] if id_ in esacci_lakes_hylak_fields_df.index else None
        vol_total_m3        = hylak_fields_row["vol_total_m3"] if hylak_fields_row is not None else None

        if vol_total_m3 is not None:
            group   = get_volume_group(vol_total_m3)
            result  = get_esacci_lakes_mean_delta(
                        id_,
                        esacci_lakes_variable_over_high_smoke_season_df = high_lakes_dfs_by_group[group],
                        esacci_lakes_variable_over_low_smoke_season_df  = low_lakes_dfs_by_group[group],
                        weeks                                            = weeks_by_group[group],
                    )
            mean_delta, coverage = result if result is not None else (None, None)
        else:
            group       = None
            mean_delta  = None
            coverage    = None

        records.append(
            {
                "esacci_lakes_id":  id_,
                "latitude":         row["lat_centre"],
                "longitude":        row["lon_centre"],
                "lake_area_m2":     hylak_fields_row["lake_area_m2"]   if hylak_fields_row is not None else None,
                "depth_avg_m":      hylak_fields_row["depth_avg_m"]    if hylak_fields_row is not None else None,
                "elevation_m":      hylak_fields_row["elevation_m"]    if hylak_fields_row is not None else None,
                "vol_total_m3":     vol_total_m3,
                "volume_group":     group,
                "mean_delta":       mean_delta,
                "coverage":         coverage,
            }
        )

    return pd.DataFrame(records).set_index("esacci_lakes_id")


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main(
) -> int:
    args = build_parser().parse_args()

    if not arguments_are_valid(args):
        return EXIT_FAILURE

    metadata_df     = read_esacci_lakes_metadata_csv(args.esacci_lakes_metadata_csv_path)
    hylak_fields_df = read_esacci_lakes_hylak_field_values_csv(args.esacci_lakes_hylak_field_values_csv_path)

    high_lakes_dfs_by_group = {}
    low_lakes_dfs_by_group  = {}
    weeks_by_group          = {}

    for group in GROUPS:
        high_lakes_dfs_by_group[group] = read_lakes_csv(getattr(args, f"{group}_high_lakes_csv_path"))
        low_lakes_dfs_by_group[group]  = read_lakes_csv(getattr(args, f"{group}_low_lakes_csv_path"))

        summary_df              = read_summary_csv(getattr(args, f"{group}_summary_csv_path"))
        weeks_by_group[group]   = get_longest_cluster(summary_df)

    esacci_lakes_deltas_df = get_esacci_lakes_deltas_df(
                                metadata_df,
                                esacci_lakes_hylak_fields_df    = hylak_fields_df,
                                high_lakes_dfs_by_group         = high_lakes_dfs_by_group,
                                low_lakes_dfs_by_group          = low_lakes_dfs_by_group,
                                weeks_by_group                  = weeks_by_group,
                            )

    to_csv(
        esacci_lakes_deltas_df,
        args.output,
    )

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())