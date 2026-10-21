SELECT * 
FROM products;

-- ==================================================
-- FILTER WITH WHERE
-- ==================================================

SELECT name, price
FROM products
WHERE price > 1000;

-- ==================================================
-- ORDER BY + LIMIT
-- ==================================================

SELECT name, price
FROM products
ORDER BY price DESC
LIMIT 2;


-- ==================================================
-- STEP 22: INNER JOIN
-- ==================================================

SELECT
    c.name AS customer_name,
    p.name AS product_name,
    o.quantity,
    p.price,
    p.price * o.quantity AS total_amount
FROM orders AS o

INNER JOIN customers AS c
    ON o.customer_id = c.id

INNER JOIN products AS p
    ON o.product_id = p.id;


-- ==================================================
-- STEP 23: AGGREGATION
-- ==================================================

SELECT
    COUNT(*) AS product_count,
    SUM(stock) AS total_units,
    SUM(price * stock) AS inventory_value
FROM products;


-- ==================================================
-- STEP 24: QUERY PLAN INSPECTION
-- ==================================================

EXPLAIN
SELECT *
FROM products
WHERE name = 'Laptop';