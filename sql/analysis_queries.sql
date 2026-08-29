-- 1. Overall KPIs
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_sales,
    COUNT(*) AS number_of_records,
    ROUND(AVG(rating), 2) AS average_rating
FROM blinkit_sales;

-- 2. Sales and customer ratings by fat-content category
SELECT
    item_fat_content,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_sales,
    COUNT(*) AS number_of_records,
    ROUND(AVG(rating), 2) AS average_rating
FROM blinkit_sales
GROUP BY item_fat_content
ORDER BY total_sales DESC;

-- 3. Top five item types by total sales
SELECT
    item_type,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_sales,
    COUNT(*) AS number_of_records,
    ROUND(AVG(rating), 2) AS average_rating
FROM blinkit_sales
GROUP BY item_type
ORDER BY total_sales DESC
LIMIT 5;

-- 4. Sales mix by outlet tier and fat-content category
SELECT
    outlet_location_type,
    ROUND(SUM(sales) FILTER (WHERE item_fat_content = 'Low Fat'), 2)
        AS low_fat_sales,
    ROUND(SUM(sales) FILTER (WHERE item_fat_content = 'Regular'), 2)
        AS regular_sales,
    ROUND(SUM(sales), 2) AS total_sales
FROM blinkit_sales
GROUP BY outlet_location_type
ORDER BY total_sales DESC;

-- 5. Sales performance by outlet establishment year
SELECT
    outlet_establishment_year,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(AVG(sales), 2) AS average_sales,
    COUNT(*) AS number_of_records,
    ROUND(AVG(rating), 2) AS average_rating
FROM blinkit_sales
GROUP BY outlet_establishment_year
ORDER BY outlet_establishment_year;

-- 6. Contribution of each outlet size to total sales
WITH outlet_size_sales AS (
    SELECT
        outlet_size,
        SUM(sales) AS total_sales
    FROM blinkit_sales
    GROUP BY outlet_size
)
SELECT
    outlet_size,
    ROUND(total_sales, 2) AS total_sales,
    ROUND(100.0 * total_sales / SUM(total_sales) OVER (), 2)
        AS sales_percentage
FROM outlet_size_sales
ORDER BY total_sales DESC;

-- 7. Complete outlet-type performance table
WITH outlet_performance AS (
    SELECT
        outlet_type,
        SUM(sales) AS total_sales,
        AVG(sales) AS average_sales,
        COUNT(*) AS number_of_records,
        AVG(rating) AS average_rating
    FROM blinkit_sales
    GROUP BY outlet_type
)
SELECT
    outlet_type,
    ROUND(total_sales, 2) AS total_sales,
    ROUND(100.0 * total_sales / SUM(total_sales) OVER (), 2)
        AS sales_percentage,
    ROUND(average_sales, 2) AS average_sales,
    number_of_records,
    ROUND(average_rating, 2) AS average_rating,
    DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
FROM outlet_performance
ORDER BY sales_rank;

-- 8. Rank item types within each outlet tier
WITH item_tier_sales AS (
    SELECT
        outlet_location_type,
        item_type,
        SUM(sales) AS total_sales
    FROM blinkit_sales
    GROUP BY outlet_location_type, item_type
)
SELECT
    outlet_location_type,
    item_type,
    ROUND(total_sales, 2) AS total_sales,
    DENSE_RANK() OVER (
        PARTITION BY outlet_location_type
        ORDER BY total_sales DESC
    ) AS item_rank_within_tier
FROM item_tier_sales
ORDER BY outlet_location_type, item_rank_within_tier, item_type;

