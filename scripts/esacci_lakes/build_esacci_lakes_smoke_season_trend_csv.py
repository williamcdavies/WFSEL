PROG = "build_esacci_lakes_smoke_season_trend_csv.py"
DESC = ""

HIGH_SMOKE_YEAR_STRATEGIES = [
    "all",
    "most-recent",
    "most-smoke",
]
LOW_SMOKE_YEAR_STRATEGIES  = [
    "all",
    "most-recent",
    "most-smoke",
]
MULTI_HIGH_STRATEGIES      = [
    "network",
    "means",
    "medians",
]

WINDOWING_STRATEGIES       = [
    "sliding-window",
    "unimodal-distribution",
]
WINDOWING_EDGES            = [
    "early",
    "late",
]


DEFAULT_LOOKBACK_WEEKS      = 3
DEFAULT_LOOKAHEAD_WEEKS     = 20
DEFAULT_NORMALISATION_WEEKS = [-1]

COUNT_OF_DISTINCT_START_DAYS_LOWER_BOUND = 7
COUNT_OF_DISTINCT_START_DAYS_UPPER_BOUND = 42
ESACCI_LAKES_COVERAGE_LOWER_BOUND        = 0.5
ESACCI_LAKES_COVERAGE_UPPER_BOUND        = 1.0


# ----------------------------------------------------------------------
# argument functions
# ----------------------------------------------------------------------
def add_argument_high_year_strategy(
    parser: ArgumentParser,
) -> None:
    """
    Add a `high-year-strategy` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--high-year-strategy",
        type     = str,
        required = True,
        choices  = HIGH_SMOKE_YEAR_STRATEGIES,
    )


def add_argument_low_year_strategy(
    parser: ArgumentParser,
) -> None:
    """
    Add a `low-year-strategy` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--low-year-strategy",
        type     = str,
        required = True,
        choices  = LOW_SMOKE_YEAR_STRATEGIES,
    )


def add_argument_multi_high_strategy(
    parser: ArgumentParser,
) -> None:
    """
    Add a `multi-high-strategy` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--multi-high-strategy",
        required = True,
        type     = str,
        choices  = MULTI_HIGH_STRATEGIES,
    )


def add_argument_windowing_strategy(
    parser: ArgumentParser,
) -> None:
    """
    Add a `windowing-strategy` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--windowing-strategy",
        type     = str,
        required = True,
        choices  = WINDOWING_STRATEGIES,
    )


def add_argument_windowing_trigger(
    parser: ArgumentParser,
) -> None:
    """
    Add a `windowing-trigger` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--windowing-trigger",
        type     = int,
        required = True,
    )


def add_argument_windowing_edge(
    parser: ArgumentParser,
) -> None:
    """
    Add a `windowing-edge` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--windowing-edge",
        type     = str,
        required = True,
        choices  = WINDOWING_EDGES,
    )


def add_argument_lookback_weeks(
    parser: ArgumentParser,
) -> None:
    """
    Add a `lookback-weeks` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--lookback-weeks",
        type    = int,
        default = DEFAULT_LOOKBACK_WEEKS,
    )


def add_argument_lookahead_weeks(
    parser: ArgumentParser,
) -> None:
    """
    Add a `lookahead-weeks` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--lookahead-weeks",
        type    = int,
        default = DEFAULT_LOOKAHEAD_WEEKS,
    )


def add_argument_normalisation_weeks(
    parser: ArgumentParser,
) -> None:
    """
    Add a `normalisation-weeks` argument to a parser.

    Parameters
    ----------
    parser : ArgumentParser
        The parser

    """
    parser.add_argument(
        "--normalisation-weeks",
        nargs   = "+",
        type    = int,
        default = DEFAULT_NORMALISATION_WEEKS,
    )


# ----------------------------------------------------------------------
# setup functions
# ----------------------------------------------------------------------
def build_parser(
) -> ArgumentParser:
    """
    Wrap build_parser.

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        prog        = PROG,
        description = DESC,
        usage       = "%(prog)s [options]",
    )

    parser = _build_parser(
        parser,
        positional_arguments = [
            add_argument_esacci_lakes_merged_product_dir_path,
            add_argument_esacci_lakes_counts_of_distinct_start_days_by_year_csv_path,
        ],
        optional_arguments   = [
            add_argument_high_year_strategy,
            add_argument_low_year_strategy,
            add_argument_multi_high_strategy,
            add_argument_windowing_strategy,
            add_argument_windowing_trigger,
            add_argument_windowing_edge,
            add_argument_lookback_weeks,
            add_argument_lookahead_weeks,
            add_argument_normalisation_weeks,
            add_argument_output,
        ],
    )

    return parser


def arguments_are_valid(
    arguments: Namespace,
) -> bool:
    """
    Wrap arguments_are_valid.

    Parameters
    ----------
    arguments : Namespace
        The arguments

    Returns
    -------
    bool

    """
    argument_name_to_validator = {
        "esacci_lakes_merged_product_dir_path":                        argument_is_directory,
        "esacci_lakes_counts_of_distinct_start_days_by_year_csv_path": argument_is_file,
    }

    boolean = _arguments_are_valid(
        arguments,
        argument_name_to_validator,
    )

    return boolean


# ----------------------------------------------------------------------
# classification functions
# ----------------------------------------------------------------------
def classify_years(
    esacci_lakes_counts_of_distinct_start_days_by_year_df: pd.DataFrame,
    *,
    lower_bound: float | None = None,
    upper_bound: float | None = None,
) -> pd.DataFrame:
    """
    Classify (lake, year) pairs.

    Parameters
    ----------
    esacci_lakes_counts_of_distinct_start_days_by_year_df : pd.DataFrame
        The ESA CCI Lakes counts of distinct start days by year
    lower_bound : float | None, optional
        The lower bound, by default None
    upper_bound : float | None, optional
        The upper bound, by default None

    Returns
    -------
    pd.DataFrame
    """
    df = (
        esacci_lakes_counts_of_distinct_start_days_by_year_df
        .rename(columns = int)
        .melt(
            var_name     = "year",
            value_name   = "count_of_distinct_start_days",
            ignore_index = False,
        )
        .reset_index()
    )

    if lower_bound is not None:
        df = df[df["count_of_distinct_start_days"] >= lower_bound]

    if upper_bound is not None:
        df = df[df["count_of_distinct_start_days"] <= upper_bound]

    df = df.reset_index(drop = True)

    return df


# ----------------------------------------------------------------------
# selection functions
# ----------------------------------------------------------------------
def _smoke_year_strategy_most_recent(
    classified_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Smoke year strategy function mapping to "most-recent".

    Parameters
    ----------
    classified_df : pd.DataFrame
        Classified DataFrame, in long format

    Returns
    -------
    pd.DataFrame
    """
    df = (
        classified_df
        .loc[(
            classified_df
            .groupby("esacci_lakes_id")["year"]
            .idxmax()
        )]
        .reset_index(drop = True)
    )

    return df


def _smoke_year_strategy_most_smoke(
    classified_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Smoke year strategy function mapping to "most-smoke".

    Parameters
    ----------
    classified_df : pd.DataFrame
        Classified DataFrame, in long format

    Returns
    -------
    pd.DataFrame
    """
    df = (
        classified_df
        .loc[(
            classified_df
            .groupby("esacci_lakes_id")["count_of_distinct_start_days"]
            .idxmax()
        )]
        .reset_index(drop = True)
    )

    return df


def _smoke_year_strategy_all(
    classified_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Smoke year strategy function mapping to "all".

    Parameters
    ----------
    classified_df : pd.DataFrame
        Classified DataFrame, in long format

    Returns
    -------
    pd.DataFrame
    """
    return classified_df


def get_high_smoke_year_strategy_function(
    strategy: str,
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """
    Get high smoke year strategy function.

    Parameters
    ----------
    strategy : str
        The high smoke year strategy

    Returns
    -------
    Callable[[pd.DataFrame], pd.DataFrame]

    Raises
    ------
    ValueError
        If strategy is not in HIGH_SMOKE_YEAR_STRATEGIES
    """
    match strategy:
        case "most-recent":
            return _smoke_year_strategy_most_recent
        case "most-smoke":
            return _smoke_year_strategy_most_smoke
        case "all":
            return _smoke_year_strategy_all
        case _:
            message = f"expected strategy to be in {HIGH_SMOKE_YEAR_STRATEGIES}: got {strategy}"

            raise ValueError(message)


def get_low_smoke_year_strategy_function(
    strategy: str,
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    """
    Get low smoke year strategy function.

    Parameters
    ----------
    strategy : str
        The low smoke year strategy

    Returns
    -------
    Callable[[pd.DataFrame], pd.DataFrame]

    Raises
    ------
    ValueError
        If strategy is not in LOW_SMOKE_YEAR_STRATEGIES
    """
    match strategy:
        case "most-recent":
            return _smoke_year_strategy_most_recent
        case "most-smoke":
            return _smoke_year_strategy_most_smoke
        case "all":
            return _smoke_year_strategy_all
        case _:
            message = f"expected strategy to be in {LOW_SMOKE_YEAR_STRATEGIES}: got {strategy}"

            raise ValueError(message)


# ----------------------------------------------------------------------
# smoke range functions
# ----------------------------------------------------------------------
def query_table_esacci_lakes_for_distinct_start_days(
    esacci_lakes_id: int,
    year:            int,
    cursor:          psycopg.Cursor,
) -> pd.Series:
    """
    Query spatial.esacci_lakes for distinct start days.

    Parameters
    ----------
    esacci_lakes_id : int
        The ESA CCI Lakes id
    year : int
        The year
    cursor : psycopg.Cursor
        The cursor

    Returns
    -------
    pd.Series
    """
    query = DISTINCT_START_DAYS_QUERY.format(table = sql.Identifier(f"hms_smokes{year}"))

    cursor.execute(
        query,
        params = {
            "id": esacci_lakes_id,
        },
    )

    distinct_start_days_ser = pd.Series(
        [
            record[0]
            for record
            in cursor.fetchall()
        ],
    )

    return distinct_start_days_ser


def compute_first_day_of_smoke_season_range(
    distinct_start_days_ser: pd.Series,
    *,
    windowing_trigger: int,
    windowing_edge:    str,
) -> int | None:
    """
    Compute the first day of a smoke season range.

    Parameters
    ----------
    distinct_start_days_ser : pd.Series
        The distinct start days
    windowing_trigger : int
        The windowing trigger
    windowing_edge : str
        The windowing edge

    Returns
    -------
    int | None

    Raises
    ------
    ValueError
        If windowing edge is not in WINDOWING_EDGES
    """
    for i in range(
        windowing_trigger - 1,
        len(distinct_start_days_ser),
    ):
        earliest_distinct_start_day_in_window = distinct_start_days_ser.iloc[i - (windowing_trigger - 1)]
        latest_distinct_start_day_in_window   = distinct_start_days_ser.iloc[i]

        if latest_distinct_start_day_in_window - earliest_distinct_start_day_in_window < DAYS_IN_A_WEEK:
            match windowing_edge:
                case "early":
                    return earliest_distinct_start_day_in_window
                case "late":
                    return latest_distinct_start_day_in_window
                case _:
                    message = f"expected windowing edge to be in {WINDOWING_EDGES}: got {windowing_edge}"

                    raise ValueError(message)

    return None


def compute_last_day_of_smoke_season_range(
    distinct_start_days_ser: pd.Series,
    *,
    windowing_trigger: int,
    windowing_edge:    str,
) -> int | None:
    """
    Compute the last day of a smoke season range.

    Parameters
    ----------
    distinct_start_days_ser : pd.Series
        The distinct start days
    windowing_trigger : int
        The windowing trigger
    windowing_edge : str
        The windowing edge

    Returns
    -------
    int | None

    Raises
    ------
    ValueError
        If windowing edge is not in WINDOWING_EDGES
    """
    for i in reversed(range(
        windowing_trigger - 1,
        len(distinct_start_days_ser),
    )):
        earliest_distinct_start_day_in_window = distinct_start_days_ser.iloc[i - (windowing_trigger - 1)]
        latest_distinct_start_day_in_window   = distinct_start_days_ser.iloc[i]

        if latest_distinct_start_day_in_window - earliest_distinct_start_day_in_window < DAYS_IN_A_WEEK:
            match windowing_edge:
                case "early":
                    return earliest_distinct_start_day_in_window
                case "late":
                    return latest_distinct_start_day_in_window
                case _:
                    message = f"expected windowing edge to be in {WINDOWING_EDGES}: got {windowing_edge}"

                    raise ValueError(message)

    return None


def compute_smoke_season_range(
    distinct_start_days_ser: pd.Series,
    *,
    windowing_trigger: int,
    windowing_edge:    str,
) -> tuple[int, int] | None:
    """
    Compute the smoke season range.

    Parameters
    ----------
    distinct_start_days_ser : pd.Series
        The distinct start days
    windowing_trigger : int
        The windowing trigger
    windowing_edge : str
        The windowing edge

    Returns
    -------
    tuple[int, int] | None
    """
    first_day_of_smoke_season_range = compute_first_day_of_smoke_season_range(
        distinct_start_days_ser,
        windowing_trigger = windowing_trigger,
        windowing_edge    = windowing_edge,
    )
    last_day_of_smoke_season_range  = compute_last_day_of_smoke_season_range(
        distinct_start_days_ser,
        windowing_trigger = windowing_trigger,
        windowing_edge    = windowing_edge,
    )

    if (
           first_day_of_smoke_season_range is None
        or last_day_of_smoke_season_range  is None
    ):
        return None

    return (
        first_day_of_smoke_season_range,
        last_day_of_smoke_season_range,
    )


def build_smoke_season_ranges_row(
    smoke_year_row: Any,
    connection:     psycopg.Connection,
    *,
    windowing_trigger: int,
    windowing_edge:    str,
) -> dict[str, Any] | None:
    """
    Build a smoke season ranges row.

    Parameters
    ----------
    smoke_year_row : Any
        The smoke year row
    connection : psycopg.Connection
        The connection
    windowing_trigger : int
        The windowing trigger
    windowing_edge : str
        The windowing edge

    Returns
    -------
    dict[str, Any] | None
    """
    with connection.cursor() as cursor:
        distinct_start_days_ser = query_table_esacci_lakes_for_distinct_start_days(
            smoke_year_row.esacci_lakes_id,
            smoke_year_row.year,
            cursor,
        )

    smoke_season_range = compute_smoke_season_range(
        distinct_start_days_ser,
        windowing_trigger = windowing_trigger,
        windowing_edge    = windowing_edge,
    )

    if smoke_season_range is None:
        return None

    (
        first_day_of_smoke_season_range,
        last_day_of_smoke_season_range,
    ) = smoke_season_range

    row                                    = {}
    row["esacci_lakes_id"]                 = smoke_year_row.esacci_lakes_id
    row["year"]                            = smoke_year_row.year
    row["first_day_of_smoke_season_range"] = first_day_of_smoke_season_range
    row["last_day_of_smoke_season_range"]  = last_day_of_smoke_season_range

    return row


def build_smoke_season_ranges_df(
    smoke_years_df: pd.DataFrame,
    connection:     psycopg.Connection,
    *,
    windowing_trigger: int,
    windowing_edge:    str,
) -> pd.DataFrame:
    """
    Build a smoke season ranges DataFrame.

    Parameters
    ----------
    smoke_years_df : pd.DataFrame
        The smoke years
    connection : psycopg.Connection
        The connection
    windowing_trigger : int
        The windowing trigger
    windowing_edge : str
        The windowing edge

    Returns
    -------
    pd.DataFrame
    """
    rows = [
        row
        for row in (
            build_smoke_season_ranges_row(
                smoke_year_row,
                connection,
                windowing_trigger = windowing_trigger,
                windowing_edge    = windowing_edge,
            )
            for smoke_year_row
            in smoke_years_df.itertuples(index = False)
        )
        if row is not None
    ]

    smoke_season_ranges_df = pd.DataFrame(rows)

    return smoke_season_ranges_df


# ----------------------------------------------------------------------
# interest range functions
# ----------------------------------------------------------------------
def compute_first_day_of_interest_range(
    first_day_of_smoke_season_range: int,
    *,
    lookback_weeks: int,
) -> int | None:
    """
    Compute the first day of an interest range.

    Parameters
    ----------
    first_day_of_smoke_season_range : int
        The first day of the smoke season range
    lookback_weeks : int
        The number of lookback weeks

    Returns
    -------
    int | None
    """
    first_day_of_interest_range = (
        first_day_of_smoke_season_range
        - (lookback_weeks * DAYS_IN_A_WEEK)
    )

    if first_day_of_interest_range < 1:
        return None

    return first_day_of_interest_range


def compute_last_day_of_interest_range(
    first_day_of_smoke_season_range: int,
    *,
    lookahead_weeks: int,
) -> int | None:
    """
    Compute the last day of an interest range.

    Parameters
    ----------
    first_day_of_smoke_season_range : int
        The first day of the smoke season range
    lookahead_weeks : int
        The number of lookahead weeks

    Returns
    -------
    int | None
    """
    last_day_of_interest_range = (
        first_day_of_smoke_season_range
        + (DAYS_IN_A_WEEK - 1)
        + (lookahead_weeks * DAYS_IN_A_WEEK)
    )

    if last_day_of_interest_range > 366:
        return None

    return last_day_of_interest_range


def compute_interest_range(
    first_day_of_smoke_season_range: int,
    *,
    lookback_weeks:  int,
    lookahead_weeks: int,
) -> tuple[int, int] | None:
    """
    Compute the interest range.

    Parameters
    ----------
    first_day_of_smoke_season_range : int
        The first day of the smoke season range
    lookback_weeks : int
        The number of lookback weeks
    lookahead_weeks : int
        The number of lookahead weeks

    Returns
    -------
    tuple[int, int] | None
    """
    first_day_of_interest_range = compute_first_day_of_interest_range(
        first_day_of_smoke_season_range,
        lookback_weeks = lookback_weeks,
    )
    last_day_of_interest_range  = compute_last_day_of_interest_range(
        first_day_of_smoke_season_range,
        lookahead_weeks = lookahead_weeks,
    )

    if (
           first_day_of_interest_range is None
        or last_day_of_interest_range  is None
    ):
        return None

    return (
        first_day_of_interest_range,
        last_day_of_interest_range,
    )


def build_interest_ranges_row(
    smoke_season_ranges_row: Any,
    *,
    lookback_weeks:  int,
    lookahead_weeks: int,
) -> dict[str, Any] | None:
    """
    Build an interest range row.

    Parameters
    ----------
    smoke_season_ranges_row : Any
        The smoke season ranges row
    lookback_weeks : int
        The number of lookback weeks
    lookahead_weeks : int
        The number of lookahead weeks

    Returns
    -------
    dict[str, Any] | None
    """
    interest_range = compute_interest_range(
        smoke_season_ranges_row.first_day_of_smoke_season_range,
        lookback_weeks  = lookback_weeks,
        lookahead_weeks = lookahead_weeks,
    )

    if interest_range is None:
        return None

    (
        first_day_of_interest_range,
        last_day_of_interest_range,
    ) = interest_range

    row                                = {}
    row["esacci_lakes_id"]             = smoke_season_ranges_row.esacci_lakes_id
    row["year"]                        = smoke_season_ranges_row.year
    row["first_day_of_interest_range"] = first_day_of_interest_range
    row["last_day_of_interest_range"]  = last_day_of_interest_range

    return row


def build_interest_ranges_df(
    smoke_season_ranges_df: pd.DataFrame,
    *,
    lookback_weeks:  int,
    lookahead_weeks: int,
) -> pd.DataFrame:
    """
    Build an interest ranges DataFrame.

    Parameters
    ----------
    smoke_season_ranges_df : pd.DataFrame
        The smoke season ranges
    lookback_weeks : int
        The number of lookback weeks
    lookahead_weeks : int
        The number of lookahead weeks

    Returns
    -------
    pd.DataFrame
    """
    rows = [
        row
        for row in (
            build_interest_ranges_row(
                smoke_season_ranges_row,
                lookback_weeks  = lookback_weeks,
                lookahead_weeks = lookahead_weeks,
            )
            for smoke_season_ranges_row
            in smoke_season_ranges_df.itertuples(index = False)
        )
        if row is not None
    ]

    interest_ranges_df = pd.DataFrame(rows)

    return interest_ranges_df


def _multi_high_strategy_network(
    high_interest_ranges_df: pd.DataFrame,
) -> pd.DataFrame:
    return high_interest_ranges_df


def _multi_high_strategy_means(
    high_interest_ranges_df: pd.DataFrame,
) -> pd.DataFrame:
    df = (
        high_interest_ranges_df
        .groupby("esacci_lakes_id")[[
            "first_day_of_interest_range",
            "last_day_of_interest_range",
        ]]
        .mean()
        .apply(np.floor)
        .astype(int)
        .reset_index()
    )

    return df


def _multi_high_strategy_medians(
    high_interest_ranges_df: pd.DataFrame,
) -> pd.DataFrame:
    df = (
        high_interest_ranges_df
        .groupby("esacci_lakes_id")[[
            "first_day_of_interest_range",
            "last_day_of_interest_range",
        ]]
        .median()
        .apply(np.floor)
        .astype(int)
        .reset_index()
    )

    return df


def get_multi_high_strategy_function(
    strategy: str,
) -> Callable[[pd.DataFrame], pd.DataFrame]:
    match strategy:
        case "network":
            return _multi_high_strategy_network
        case "means":
            return _multi_high_strategy_means
        case "medians":
            return _multi_high_strategy_medians
        case _:
            message = f"expected strategy to be in {MULTI_HIGH_STRATEGIES}: got {strategy}"

            raise ValueError(message)


def _build_low_interest_ranges_df_network(
    high_interest_ranges_df: pd.DataFrame,
    low_selected_df:         pd.DataFrame,
) -> pd.DataFrame:
    df = low_selected_df.merge(
        high_interest_ranges_df[[
            "esacci_lakes_id",
            "year",
            "first_day_of_interest_range",
            "last_day_of_interest_range",
        ]],
        on  = "esacci_lakes_id",
        how = "inner",
    )

    df = df.rename(columns = {
        "year_x": "low_year",
        "year_y": "high_year",
    })

    return df


def _build_low_interest_ranges_df_collapsed(
    high_interest_ranges_df: pd.DataFrame,
    low_selected_df:         pd.DataFrame,
) -> pd.DataFrame:
    df = low_selected_df.merge(
        high_interest_ranges_df[[
            "esacci_lakes_id",
            "first_day_of_interest_range",
            "last_day_of_interest_range",
        ]],
        on  = "esacci_lakes_id",
        how = "inner",
    )

    df = df.rename(columns = {
        "year": "low_year",
    })

    return df


def get_build_low_interest_ranges_df_function(
    strategy: str,
) -> Callable[[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
    match strategy:
        case "network":
            return _build_low_interest_ranges_df_network
        case "medians" | "means":
            return _build_low_interest_ranges_df_collapsed
        case _:
            message = f"expected strategy to be in {MULTI_HIGH_STRATEGIES}: got {strategy}"

            raise ValueError(message)


# ----------------------------------------------------------------------
# observation functions (spooky section)
# ----------------------------------------------------------------------
def slice_esacci_lakes_merged_product_csv_paths_by_interest_range(
    esacci_lakes_merged_product_csv_paths: list[Path],
    *,
    first_day_of_interest_range: int,
    last_day_of_interest_range:  int,
) -> list[tuple[int, Path]]:
    pairs = [
        (
            to_day(index),
            esacci_lakes_merged_product_csv_paths[index],
        )
        for index
        in range(
            to_index(first_day_of_interest_range),
            to_index(last_day_of_interest_range) + 1,
        )
    ]

    return pairs


def build_observations_row(
    interest_ranges_row:                  Any,
    esacci_lakes_merged_product_dir_path: Path,
) -> dict[str, Any] | None:
    merged_product_csv_paths        = find_files_by_extension(
        esacci_lakes_merged_product_dir_path / str(interest_ranges_row.year),
        "csv",
    )
    sliced_merged_product_csv_paths = slice_esacci_lakes_merged_product_csv_paths_by_interest_range(
        merged_product_csv_paths,
        first_day_of_interest_range = interest_ranges_row.first_day_of_interest_range,
        last_day_of_interest_range  = interest_ranges_row.last_day_of_interest_range,
    )

    observations = []

    for (
        day,
        sliced_merged_product_csv_path,
    ) in sliced_merged_product_csv_paths:
        merged_product_df = read_esacci_lakes_merged_product_csv(sliced_merged_product_csv_path)
        merged_product_df = merged_product_df[
              (merged_product_df["lake_surface_water_temperature_coverage"] >= ESACCI_LAKES_COVERAGE_LOWER_BOUND)
            & (merged_product_df["lake_surface_water_temperature_coverage"] <= ESACCI_LAKES_COVERAGE_UPPER_BOUND)
        ]

        if interest_ranges_row.esacci_lakes_id in merged_product_df.index:
            lake_surface_water_temperature_mean = merged_product_df.loc[
                interest_ranges_row.esacci_lakes_id,
                "lake_surface_water_temperature_mean",
            ]

            observations.append((
                day,
                lake_surface_water_temperature_mean,
            ))

    if not observations:
        return None

    row                 = interest_ranges_row._asdict()
    row["observations"] = observations

    return row


def build_observations_df(
    interest_ranges_df:                   pd.DataFrame,
    esacci_lakes_merged_product_dir_path: Path,
) -> pd.DataFrame:
    rows = [
        row
        for row in (
            build_observations_row(
                interest_ranges_row,
                esacci_lakes_merged_product_dir_path,
            )
            for interest_ranges_row
            in interest_ranges_df.itertuples(index = False)
        )
        if row is not None
    ]

    observations_df = pd.DataFrame(rows)

    return observations_df


def build_bucketed_observations_row(
    merged_row: Any,
) -> dict[str, Any]:
    bucketed_observations = defaultdict(list)

    for (
        day,
        lake_surface_water_temperature_mean,
    ) in merged_row.observations:
        bucketed_observations[
            (day - merged_row.first_day_of_interest_range)
            // DAYS_IN_A_WEEK
        ].append(lake_surface_water_temperature_mean)

    row                          = merged_row._asdict()
    row["bucketed_observations"] = list(bucketed_observations.items())

    return row


def build_bucketed_observations_df(
    merged_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        build_bucketed_observations_row(
            merged_row,
        )
        for merged_row
        in merged_df.itertuples(index = False)
    ]

    bucketed_observations_df = pd.DataFrame(rows)

    return bucketed_observations_df


def build_averaged_observations_row(
    bucketed_observations_row: Any,
) -> dict[str, Any]:
    averaged_observations = []

    for (
        week_index,
        lake_surface_water_temperature_means,
    ) in bucketed_observations_row.bucketed_observations:
        averaged_observations.append((
            week_index,
            np.mean(lake_surface_water_temperature_means),
        ))

    row                          = bucketed_observations_row._asdict()
    row["averaged_observations"] = averaged_observations

    return row


def build_averaged_observations_df(
    bucketed_observations_df: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        build_averaged_observations_row(
            bucketed_observations_row,
        )
        for bucketed_observations_row
        in bucketed_observations_df.itertuples(index = False)
    ]

    averaged_observations_df = pd.DataFrame(rows)

    return averaged_observations_df
