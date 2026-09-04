E-commerce-project/
├── main.py                      # entry point — builds the app, includes routers
├── config.py                    # env-based settings (MySQL + MongoDB URLs)
├── schema/
│   ├── product\_schema.py        # Pydantic models for products
│   └── order\_schema.py          # Pydantic models for orders
├── mongodb/
│   ├── mongo\_connection.py      # Mongo client + products collection
│   └── product\_crud.py          # catalog CRUD + atomic stock reserve/release
├── sql/
│   ├── sql\_connection.py        # MySQL engine/session (SQLAlchemy)
│   ├── sql\_models.py            # Order, OrderItem, OrderStatus
│   └── order\_crud.py            # order lifecycle logic
├── routes/
│   ├── product\_routes.py        # /products endpoints
│   ├── order\_routes.py          # /orders endpoints
│   └── analytics\_routes.py      # /analytics endpoints
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example



