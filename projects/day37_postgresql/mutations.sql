-- ==================================================
-- UPDATE PRODUCT
-- ==================================================

-- Check current stock
SELECT id, name, stock
FROM products
WHERE id = 1;


-- Update Laptop stock from 10 to 15
UPDATE products
SET stock = 15
WHERE id = 1;


-- Verify updated stock
SELECT id, name, stock
FROM products
WHERE id = 1;