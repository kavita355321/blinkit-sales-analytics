# Data notes

## Raw data

`raw/blinkit_data.csv` contains 8,523 records and 12 fields describing items,
outlets, sales and ratings. It is retained unchanged for reproducibility.

## Processed data

Run `python python/blinkit_analysis.py` from the project root to create
`processed/blinkit_data_clean.csv`.

The cleaning workflow:

- converts column names to snake_case;
- standardises `LF`, `low fat` and `reg` category values;
- converts numeric fields using explicit coercion;
- labels missing outlet sizes as `Unknown`;
- removes exact duplicate records; and
- validates that sales contains no missing or non-numeric values.

## Important limitation

The dataset is a portfolio dataset and does not include transaction dates,
customer identifiers, costs or profit. The analysis therefore focuses on
descriptive sales performance rather than causal claims, customer behaviour,
profitability or genuine time-series trends.
