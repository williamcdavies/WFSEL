r"""
view_esacci_lakes_variable_relative_to_smoke_season.py

Written by William Chuter-Davies
"""

# Standard Library Imports
import sys

from argparse import ArgumentParser
from pathlib  import Path

# Related Third-party Imports
import pandas            as pd
import matplotlib.axes
import matplotlib.pyplot as plt

# Local Application/Library Specific Imports
from lib.esacci_lakes.utils.argparse import (
    add_argument_esacci_lakes_variable,
    add_argument_esacci_lakes_average_depths_csv_path,
    argument_esacci_lakes_average_depths_csv_path_exists
)
from lib.esacci_lakes.vars import (
    AVERAGE_DEPTH_LOWER_BOUND,
    AVERAGE_DEPTH_UPPER_BOUND,
    ESACCI_LAKES_VARIABLES
)
from lib.io.vars import (
    RETURN_FAILURE,
    RETURN_SUCCESS
)

PROG = "view_esacci_lakes_variable_relative_to_smoke_season.py"


def plot(
    ax: matplotlib.axes.Axes,
    df: pd.DataFrame,
    esacci_lakes_variable: str
) -> None:
    labels  = list(range(df["label_as_int"].min(), df["label_as_int"].max() + 1))
    medians = []

    for label in labels:
        y = df.loc[df["label_as_int"] == label, esacci_lakes_variable]
        x = [label] * len(y)
        
        ax.scatter(
            x=x,
            y=y,
            alpha=0.25,
            edgecolors="none",
            color="black"
        )

        medians.append(y.median())

    ax.plot(
        x=labels,
        y=medians,
        color="blue",
        marker="o"
    )

    ax.set_xticks(labels)
    ax.tick_params(labelbottom=True)
    ax.set_ylim(-30, 30)
    ax.set_xlabel("Week relative to start of smoke season")
    # ax.set_ylabel(
    #     f"{ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name} ({ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units})",
    # )
    # ax.set_title(
    #     f"Averaged weekly {esacci_lakes_variable} for lakes with an average depth <= {AVERAGE_DEPTH_LOWER_BOUND} meters",
    # )
    # ax.set_ylabel(
    #     f"{ESACCI_LAKES_VARIABLES[esacci_lakes_variable].long_name} Anomaly ({ESACCI_LAKES_VARIABLES[esacci_lakes_variable].units})",
    # )
    # ax.set_title(
    #     f"Weekly {esacci_lakes_variable} change relative to pre-smoke-season baseline for lakes with an average depth <= {AVERAGE_DEPTH_LOWER_BOUND} meters",
    # )


def main() -> int:
    # Argument parsing
    # ==================================================================================================
    parser = ArgumentParser(
        prog=PROG,
        usage="%(prog)s [options]",
        description=""""""
    )

    # Positional arguments
    parser.add_argument(
        "input_csv_path",
        type=Path,
        help=""""""
    )
    add_argument_esacci_lakes_variable(parser)
    add_argument_esacci_lakes_average_depths_csv_path(parser)

    args = parser.parse_args()
    # ==================================================================================================

    # Argument validation
    # ==================================================================================================
    if not args.input_csv_path.exists():
        print(
            f"""error: argument input_csv_path: no such file or directory: {args.input_csv_path}"""
        )

        return RETURN_FAILURE

    if not argument_esacci_lakes_average_depths_csv_path_exists(
        args.esacci_lakes_average_depths_csv_path,
        loud=True
    ):
        return RETURN_FAILURE
    # ==================================================================================================

    # Program logic
    # ==================================================================================================
    df = pd.merge(
        pd.read_csv(args.input_csv_path),
        pd.read_csv(args.esacci_lakes_average_depths_csv_path),
        on="esacci_lakes_id",
        validate="one_to_one"
    )

    shal_df             = (
        df[df["depth_avg"] <= AVERAGE_DEPTH_LOWER_BOUND]
        .melt(
            ["esacci_lakes_id", "depth_avg"],
            var_name="label",
            value_name=args.esacci_lakes_variable
        )
        .drop(columns=["depth_avg"])
        .dropna(subset=args.esacci_lakes_variable)
    )
    shal_df["label_as_int"] = shal_df["label"].str[1:].astype(int)

    deep_df             = (
        df[df["depth_avg"] >= AVERAGE_DEPTH_UPPER_BOUND]
        .melt(
            ["esacci_lakes_id", "depth_avg"],
            var_name="label",
            value_name=args.esacci_lakes_variable
        )
        .drop(columns=["depth_avg"])
        .dropna(subset=args.esacci_lakes_variable)
    )
    deep_df["label_as_int"] = deep_df["label"].str[1:].astype(int)

    fig, (shal_ax, deep_ax) = plt.subplots(
        2,
        1,
        sharex=True,
        sharey=True
    )

    plot(
        shal_ax,
        shal_df[shal_df["label_as_int"] <= 20],
        args.esacci_lakes_variable
    )
    plot(
        deep_ax,
        deep_df[deep_df["label_as_int"] <= 20],
        args.esacci_lakes_variable
    )

    fig.tight_layout()
    plt.show()

    return RETURN_SUCCESS
    # ==================================================================================================


if __name__ == "__main__":
    sys.exit(main())
