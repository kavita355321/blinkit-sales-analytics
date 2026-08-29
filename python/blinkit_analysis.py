"""Clean, analyse and visualise the Blinkit sales dataset."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "blinkit_data.csv"
PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "blinkit_data_clean.csv"
)
IMAGES_DIR = PROJECT_ROOT / "images"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

REQUIRED_COLUMNS = {
    "item_fat_content",
    "item_identifier",
    "item_type",
    "outlet_establishment_year",
    "outlet_identifier",
    "outlet_location_type",
    "outlet_size",
    "outlet_type",
    "item_visibility",
    "item_weight",
    "sales",
    "rating",
}


def to_snake_case(column_name: str) -> str:
    """Convert a source column name to a SQL-friendly name."""
    return column_name.strip().lower().replace(" ", "_")


def load_and_clean_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw CSV, validate its structure and clean known inconsistencies."""
    data = pd.read_csv(path, encoding="utf-8-sig")
    data.columns = [to_snake_case(column) for column in data.columns]

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Required columns are missing: {missing}")

    data["item_fat_content"] = data["item_fat_content"].replace(
        {"LF": "Low Fat", "low fat": "Low Fat", "reg": "Regular"}
    )

    numeric_columns = [
        "outlet_establishment_year",
        "item_visibility",
        "item_weight",
        "sales",
        "rating",
    ]
    for column in numeric_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data["outlet_size"] = data["outlet_size"].fillna("Unknown")
    data = data.drop_duplicates().reset_index(drop=True)

    if data["sales"].isna().any():
        raise ValueError("Sales contains missing or non-numeric values after cleaning.")

    return data


def calculate_kpis(data: pd.DataFrame) -> pd.DataFrame:
    """Return the core business KPIs as a two-column table."""
    return pd.DataFrame(
        {
            "metric": [
                "Total Sales",
                "Average Sales",
                "Number of Records",
                "Average Rating",
            ],
            "value": [
                data["sales"].sum(),
                data["sales"].mean(),
                data["sales"].count(),
                data["rating"].mean(),
            ],
        }
    )


def save_analysis_tables(data: pd.DataFrame) -> None:
    """Save recruiter-readable summary tables for reuse and validation."""
    sales_by_item_type = (
        data.groupby("item_type", as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            average_sales=("sales", "mean"),
            record_count=("sales", "size"),
            average_rating=("rating", "mean"),
        )
        .sort_values("total_sales", ascending=False)
    )
    sales_by_item_type.to_csv(
        OUTPUTS_DIR / "sales_by_item_type.csv", index=False
    )

    sales_by_outlet = (
        data.groupby("outlet_type", as_index=False)
        .agg(
            total_sales=("sales", "sum"),
            average_sales=("sales", "mean"),
            record_count=("sales", "size"),
            average_rating=("rating", "mean"),
        )
        .sort_values("total_sales", ascending=False)
    )
    sales_by_outlet.to_csv(OUTPUTS_DIR / "sales_by_outlet_type.csv", index=False)


def save_visualisations(data: pd.DataFrame) -> None:
    """Create reusable PNG evidence for the README and portfolio website."""
    sns.set_theme(style="whitegrid", palette="Blues_d")

    item_sales = (
        data.groupby("item_type")["sales"]
        .sum()
        .nlargest(10)
        .sort_values()
    )
    fig, axis = plt.subplots(figsize=(10, 6))
    item_sales.plot(kind="barh", ax=axis, color="#2f80ed")
    axis.set_title("Top 10 Item Types by Total Sales")
    axis.set_xlabel("Total sales (dataset units)")
    axis.set_ylabel("Item type")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "top_item_types.png", dpi=160)
    plt.close(fig)

    outlet_location_sales = (
        data.groupby(["outlet_location_type", "item_fat_content"])["sales"]
        .sum()
        .unstack(fill_value=0)
    )
    fig, axis = plt.subplots(figsize=(8, 5))
    outlet_location_sales.plot(kind="bar", ax=axis)
    axis.set_title("Sales by Outlet Tier and Item Fat Content")
    axis.set_xlabel("Outlet location tier")
    axis.set_ylabel("Total sales (dataset units)")
    axis.legend(title="Item fat content")
    axis.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "sales_by_outlet_tier.png", dpi=160)
    plt.close(fig)

    yearly_sales = data.groupby("outlet_establishment_year")["sales"].sum()
    fig, axis = plt.subplots(figsize=(9, 5))
    axis.plot(yearly_sales.index, yearly_sales.values, marker="o", color="#166534")
    axis.set_title("Sales by Outlet Establishment Year")
    axis.set_xlabel("Outlet establishment year")
    axis.set_ylabel("Total sales (dataset units)")
    fig.tight_layout()
    fig.savefig(IMAGES_DIR / "sales_by_establishment_year.png", dpi=160)
    plt.close(fig)


def main() -> None:
    """Run the complete reproducible analysis workflow."""
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    data = load_and_clean_data()
    data.to_csv(PROCESSED_DATA_PATH, index=False)

    kpis = calculate_kpis(data)
    kpis.to_csv(OUTPUTS_DIR / "kpi_summary.csv", index=False)
    save_analysis_tables(data)
    save_visualisations(data)

    print(f"Rows analysed: {len(data):,}")
    for row in kpis.itertuples(index=False):
        print(f"{row.metric}: {row.value:,.2f}")
    print(f"Processed data: {PROCESSED_DATA_PATH}")
    print(f"Outputs: {OUTPUTS_DIR}")


if __name__ == "__main__":
    main()

