-- PostgreSQL schema for the cleaned Blinkit dataset.

CREATE TABLE IF NOT EXISTS blinkit_sales (
    item_fat_content TEXT NOT NULL,
    item_identifier TEXT NOT NULL,
    item_type TEXT NOT NULL,
    outlet_establishment_year INTEGER NOT NULL,
    outlet_identifier TEXT NOT NULL,
    outlet_location_type TEXT NOT NULL,
    outlet_size TEXT NOT NULL,
    outlet_type TEXT NOT NULL,
    item_visibility NUMERIC,
    item_weight NUMERIC,
    sales NUMERIC NOT NULL,
    rating NUMERIC
);

CREATE INDEX IF NOT EXISTS idx_blinkit_item_type
    ON blinkit_sales (item_type);

CREATE INDEX IF NOT EXISTS idx_blinkit_outlet_type
    ON blinkit_sales (outlet_type);

CREATE INDEX IF NOT EXISTS idx_blinkit_outlet_location
    ON blinkit_sales (outlet_location_type);

