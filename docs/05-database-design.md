# StockFlow — Database Design

## 1. Database Overview

StockFlow will use PostgreSQL as its main database.

The database will store information about users, roles, products, categories, suppliers, inventory, sales, purchases, and stock movements.

SQLAlchemy will be used in the Flask backend to interact with the database.



## 2. Database Entities

The initial database will contain the following entities:

- User
- Role
- Category
- Supplier
- Product
- Inventory
- Stock Transaction
- Sale
- Sale Item
- Purchase
- Purchase Item



## 3. User Table

The `users` table stores the users who can access the system.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique user ID |
| `role_id` | Integer | Foreign Key, Not Null | User's assigned role |
| `first_name` | String | Not Null | User's first name |
| `last_name` | String | Not Null | User's last name |
| `email` | String | Unique, Not Null | User's email |
| `password_hash` | String | Not Null | Hashed password |
| `is_active` | Boolean | Default True | Account status |
| `created_at` | DateTime | Not Null | Account creation date |
| `updated_at` | DateTime | Not Null | Last update date |



## 4. Role Table

The `roles` table defines the access levels available in StockFlow.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique role ID |
| `name` | String | Unique, Not Null | Role name |
| `description` | Text | Nullable | Role description |
| `created_at` | DateTime | Not Null | Creation date |

### Initial Roles

- Administrator
- Manager
- Staff

One role can be assigned to many users.



## 5. Category Table

The `categories` table is used to group related products.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique category ID |
| `name` | String | Unique, Not Null | Category name |
| `description` | Text | Nullable | Category description |
| `is_active` | Boolean | Default True | Category status |
| `created_at` | DateTime | Not Null | Creation date |
| `updated_at` | DateTime | Not Null | Last update date |

One category can contain many products.



## 6. Supplier Table

The `suppliers` table stores supplier information.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique supplier ID |
| `name` | String | Not Null | Supplier name |
| `contact_person` | String | Nullable | Main contact person |
| `phone` | String | Nullable | Supplier phone number |
| `email` | String | Nullable | Supplier email |
| `address` | String | Nullable | Supplier address |
| `is_active` | Boolean | Default True | Supplier status |
| `created_at` | DateTime | Not Null | Creation date |
| `updated_at` | DateTime | Not Null | Last update date |

A supplier can supply multiple products and can have multiple purchase records.



## 7. Product Table

The `products` table stores all products managed by the business.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique product ID |
| `category_id` | Integer | Foreign Key, Not Null | Product category |
| `supplier_id` | Integer | Foreign Key, Nullable | Primary supplier |
| `name` | String | Not Null | Product name |
| `sku` | String | Unique, Not Null | Stock Keeping Unit |
| `description` | Text | Nullable | Product description |
| `cost_price` | Numeric | Not Null | Product purchase cost |
| `selling_price` | Numeric | Not Null | Product selling price |
| `minimum_stock_level` | Integer | Default 0 | Low-stock threshold |
| `is_active` | Boolean | Default True | Product status |
| `created_at` | DateTime | Not Null | Creation date |
| `updated_at` | DateTime | Not Null | Last update date |

Each product belongs to a category.

A product can have a primary supplier. The supplier relationship is nullable because a product may be added before a supplier is assigned.

The SKU must be unique.



## 8. Inventory Table

The `inventory` table stores the current stock level for each product.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique inventory ID |
| `product_id` | Integer | Foreign Key, Unique, Not Null | Related product |
| `quantity` | Integer | Not Null, Default 0 | Current stock |
| `updated_at` | DateTime | Not Null | Last stock update |

Each product has one inventory record.

The quantity represents the current available stock.



## 9. Stock Transaction Table

The `stock_transactions` table keeps a record of stock movements.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique transaction ID |
| `product_id` | Integer | Foreign Key, Not Null | Affected product |
| `user_id` | Integer | Foreign Key, Not Null | User who recorded transaction |
| `transaction_type` | String | Not Null | Type of stock movement |
| `quantity` | Integer | Not Null | Quantity moved |
| `reference` | String | Nullable | Related sale/purchase reference |
| `notes` | Text | Nullable | Additional information |
| `created_at` | DateTime | Not Null | Transaction date |

### Transaction Types

- `STOCK_IN`
- `STOCK_OUT`
- `ADJUSTMENT`

Stock transactions provide a history of changes made to inventory.



## 10. Sale Table

The `sales` table stores completed sales.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique sale ID |
| `user_id` | Integer | Foreign Key, Not Null | User who recorded the sale |
| `total_amount` | Numeric | Not Null | Total sale amount |
| `status` | String | Not Null | Sale status |
| `created_at` | DateTime | Not Null | Sale date |
| `updated_at` | DateTime | Not Null | Last update date |

A sale can contain multiple sale items.



## 11. Sale Item Table

The `sale_items` table stores the individual products included in each sale.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique sale item ID |
| `sale_id` | Integer | Foreign Key, Not Null | Related sale |
| `product_id` | Integer | Foreign Key, Not Null | Product sold |
| `quantity` | Integer | Not Null | Quantity sold |
| `unit_price` | Numeric | Not Null | Price at time of sale |
| `subtotal` | Numeric | Not Null | Quantity × unit price |

The `unit_price` is stored at the time of the sale so that changing a product's current selling price does not change historical sales records.



## 12. Purchase Table

The `purchases` table stores purchases made from suppliers.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique purchase ID |
| `supplier_id` | Integer | Foreign Key, Not Null | Supplier |
| `user_id` | Integer | Foreign Key, Not Null | User who recorded purchase |
| `total_amount` | Numeric | Not Null | Total purchase amount |
| `status` | String | Not Null | Purchase status |
| `created_at` | DateTime | Not Null | Purchase date |
| `updated_at` | DateTime | Not Null | Last update date |

A purchase can contain multiple purchase items.



## 13. Purchase Item Table

The `purchase_items` table stores the individual products included in each purchase.

| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | Integer | Primary Key | Unique purchase item ID |
| `purchase_id` | Integer | Foreign Key, Not Null | Related purchase |
| `product_id` | Integer | Foreign Key, Not Null | Product purchased |
| `quantity` | Integer | Not Null | Quantity purchased |
| `unit_cost` | Numeric | Not Null | Cost at time of purchase |
| `subtotal` | Numeric | Not Null | Quantity × unit cost |

The `unit_cost` is stored at the time of purchase so historical purchase records remain accurate if the product cost changes later.



## 14. Entity Relationships

The main relationships in the database are:

- One role can have many users.
- One category can have many products.
- One supplier can have many products.
- One product has one inventory record.
- One product can have many stock transactions.
- One user can record many stock transactions.
- One user can record many sales.
- One sale can contain many sale items.
- One product can appear in many sale items.
- One supplier can have many purchases.
- One user can record many purchases.
- One purchase can contain many purchase items.
- One product can appear in many purchase items.



## 15. Relationship Diagram

The main database relationships can be represented as:

```text
Role
  │
  └──< User
          │
          ├──< Sale
          │      │
          │      └──< SaleItem >── Product
          │
          ├──< Purchase
          │      │
          │      └──< PurchaseItem >── Product
          │
          └──< StockTransaction >── Product

Category
  │
  └──< Product >── Supplier
          │
          └── Inventory

## 16. Data Integrity Rules

The database will use constraints to help keep the data accurate and consistent.

The main rules are:

- User email addresses must be unique.
- Product SKUs must be unique.
- Required fields cannot be null.
- Foreign keys must reference existing records.
- Product prices cannot be negative.
- Stock quantities cannot be negative.
- Sale quantities must be greater than zero.
- Purchase quantities must be greater than zero.
- A sale item must belong to an existing sale.
- A purchase item must belong to an existing purchase.
- An inventory record must belong to an existing product.


## 17. Inventory Transaction Integrity

Sales, purchases, and stock adjustments will update inventory through controlled database transactions.

When a sale is completed:

1. The sale record is created.
2. The sale items are recorded.
3. Available stock is checked.
4. The relevant inventory quantities are reduced.
5. The corresponding stock-out transactions are recorded.

When a purchase is completed:

1. The purchase record is created.
2. The purchase items are recorded.
3. The relevant inventory quantities are increased.
4. The corresponding stock-in transactions are recorded.

If any part of the operation fails, the related database changes should be rolled back to prevent inconsistent inventory records.

## 18. Historical Data

StockFlow will preserve important historical transaction information.

For example, the price stored in a `sale_item` will represent the price at the time of the sale rather than the product's current selling price.

The same approach will be used for `purchase_items`, where the recorded unit cost represents the cost at the time of purchase.

Products, categories, and suppliers may be deactivated instead of permanently deleted when they are linked to historical records.


## 19. Database Indexing

Indexes will be added to fields that are frequently searched or used in database relationships.

Initial indexes may include:

- `users.email`
- `products.sku`
- `products.category_id`
- `products.supplier_id`
- `inventory.product_id`
- `stock_transactions.product_id`
- `stock_transactions.created_at`
- `sales.created_at`
- `purchases.created_at`

Additional indexes may be added during implementation based on actual query patterns and performance requirements.