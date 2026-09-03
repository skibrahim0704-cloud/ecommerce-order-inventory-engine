from fastapi import FastAPI

from sql.sql_connection import Base, engine
from sql import sql_models  # noqa: F401

from routes import product_routes, order_routes, analytics_routes


app = FastAPI(
    title="Hybrid E-Commerce & Inventory Engine",
    description=(
        "Orders and order lifecycle are stored in MySQL for transactional "
        "integrity. Product catalog and live stock levels are stored in "
        "MongoDB for flexible schema and fast inventory operations."
    ),
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    # Create MySQL tables if they don't exist
    Base.metadata.create_all(bind=engine)


# Register API routers
app.include_router(product_routes.router)
app.include_router(order_routes.router)
app.include_router(analytics_routes.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}