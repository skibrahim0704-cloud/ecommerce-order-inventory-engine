from mongodb.mongo_connection import products_collection
from bson import ObjectId


def create_product(product_data):
    result = products_collection.insert_one(product_data)

    product_data["_id"] = str(result.inserted_id)

    return product_data


def get_products():
    products = []

    for product in products_collection.find():
        product["_id"] = str(product["_id"])
        products.append(product)

    return products


def get_product(product_id):
    product = products_collection.find_one(
        {"_id": ObjectId(product_id)}
    )

    if product:
        product["_id"] = str(product["_id"])

    return product


def update_product(product_id, update_data):
    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    return result.modified_count > 0


def delete_product(product_id):
    result = products_collection.delete_one(
        {"_id": ObjectId(product_id)}
    )

    return result.deleted_count > 0