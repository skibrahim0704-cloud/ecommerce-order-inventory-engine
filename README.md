E-commerce-project/
├── main.py                      # entry point — builds the app, includes routers
├── config.py                    # env-based settings (Postgres + Mongo URLs)
├── schema/
│   ├── product_schema.py        # Pydantic models for products
│   └── order_schema.py          # Pydantic models for orders
├── mongodb/
│   ├── mongo_connection.py      # Mongo client + products collection
│   └── product_crud.py          # catalog CRUD + atomic stock reserve/release
├── sql/
│   ├── sql_connection.py        # Postgres engine/session (SQLAlchemy)
│   ├── sql_models.py            # Order, OrderItem, OrderStatus
│   └── order_crud.py            # order lifecycle logic
├── routes/
│   ├── product_routes.py        # /products endpoints
│   ├── order_routes.py          # /orders endpoints
│   └── analytics_routes.py      # /analytics endpoints
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example