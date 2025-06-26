from pathlib import Path

import pandas as pd

DATA_DIR = Path(".")
INPUT_DIR = Path(".")
OUTPUT_DIR = Path(".")

PORTFOLIO_CODE = "Portoflio Code"
ASSET_CODE = "Asset Code"
QUANTITY = "Quantity"
COLS = [PORTFOLIO_CODE, ASSET_CODE, QUANTITY]

portfolio_d1_df = pd.read_csv(
    Path(INPUT_DIR, "day1.ptf_inventories.csv"),
    sep=";",
    # usecols=COLS,
)
portfolio_d2_df = pd.read_csv(
    Path(INPUT_DIR, "day2.ptf_inventories.csv"),
    sep=";",
    # usecols=COLS,
)

portfolio_d1_df = portfolio_d1_df[COLS]
portfolio_d2_df = portfolio_d2_df[COLS]

aggregated_d1_df = portfolio_d1_df.groupby(
    [PORTFOLIO_CODE, ASSET_CODE]
).sum(
).reset_index()

aggregated_d2_df = portfolio_d2_df.groupby(
    [PORTFOLIO_CODE, ASSET_CODE]
).sum(
).reset_index()

merged_df = aggregated_d1_df.merge(
    aggregated_d2_df,
    how="outer",
    on=[PORTFOLIO_CODE, ASSET_CODE],
    suffixes=("_before", "_after"),
).fillna(0)

merged_df["variation"] = merged_df["Quantity_after"] - \
    merged_df["Quantity_before"]

variation_df = merged_df[
    merged_df["variation"] != 0
][
    [PORTFOLIO_CODE, ASSET_CODE, "variation"]
]

variation_df.to_csv(Path(OUTPUT_DIR, "variation.csv"), index=False)
