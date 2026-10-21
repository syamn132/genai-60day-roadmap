INSERT INTO products (name, price, stock)
VALUES
    ('Laptop', 65000.00, 10),
    ('Mouse', 500.00, 25),
    ('Keyboard', 1500.00, 15);

INSERT INTO customers (name, city)
VALUES
    ('Arjun', 'Bengaluru'),
    ('Priya', 'Mysuru');

INSERT INTO orders (customer_id, product_id, quantity)
VALUES
    (1, 1, 1),
    (2, 2, 3);