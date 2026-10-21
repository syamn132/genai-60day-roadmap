-- ==================================================
-- DAY 37 — STEP 21
-- DELETE PRACTICAL
-- ==================================================

-- 1. Create a temporary product
INSERT INTO products (
    name,
    price,
    stock
)
VALUES (
    'Temporary Item',
    99.00,
    1
)
RETURNING id, name, price, stock;


-- 2. Verify the inserted product
SELECT id, name, stock
FROM products
WHERE name = 'Temporary Item';


-- 3. Delete the temporary product
DELETE FROM products
WHERE name = 'Temporary Item'
RETURNING id, name;


-- 4. Verify deletion
SELECT id, name
FROM products
WHERE name = 'Temporary Item';