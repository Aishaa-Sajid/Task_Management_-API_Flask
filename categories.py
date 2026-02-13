from flask import Blueprint, request, jsonify
from app.models.category import Category
from app import db
from app.utils.decorators import token_required

category_bp = Blueprint("categories", __name__)

@category_bp.route("", methods=["POST"])
@token_required
def create_category(user):
    category = Category(name=request.json["name"], user_id=user.id)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message":"Category created"}),201

@category_bp.route("/<int:id>", methods=["GET"])
@token_required
def get_category(user, id):
    category = Category.query.filter_by(id=id, user_id=user.id).first()

    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify({"id": category.id, "name": category.name})

@category_bp.route("", methods=["GET"])
@token_required
def get_categories(user):
    cats = Category.query.filter_by(user_id=user.id).all()
    return jsonify([{"id":c.id,"name":c.name} for c in cats])

@category_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_category(user, id):
    category = Category.query.filter_by(id=id, user_id=user.id).first()

    if not category:
        return jsonify({"error": "Category not found"}), 404

    category.name = request.json.get("name")
    db.session.commit()

    return jsonify({"message": "Category updated"})

@category_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_category(user, id):
    category = Category.query.filter_by(id=id, user_id=user.id).first()

    if not category:
        return jsonify({"error": "Category not found"}), 404

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted"})

from app.models.task import Task

@category_bp.route("/<int:id>/tasks", methods=["GET"])
@token_required
def category_tasks(user, id):
    tasks = Task.query.filter_by(
        category_id=id,
        user_id=user.id
    ).all()

    return jsonify([
        {"id": t.id, "title": t.title}
        for t in tasks
    ])
