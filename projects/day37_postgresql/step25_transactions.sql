-- ==================================================
-- DAY 37 — STEP 25
-- TRANSACTION + ROLLBACK PRACTICAL
-- ==================================================

-- Check original stock
SELECT id, name, stock
FROM products
WHERE id = 1;


-- Start transaction
BEGIN;


-- Reduce Laptop stock by 2
UPDATE products
SET stock = stock - 2
WHERE id = 1;


-- Check stock inside transaction
SELECT id, name, stock
FROM products
WHERE id = 1;


-- Undo the change
ROLLBACK;


-- Verify original stock was restored
SELECT id, name, stock
FROM products
WHERE id = 1;