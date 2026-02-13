from flask import Blueprint, request, jsonify
from app.models.task import Task
from app import db
from app.utils.decorators import token_required

task_bp = Blueprint("tasks", __name__)

@task_bp.route("", methods=["POST"])
@token_required
def create_task(user):
    data = request.json
    task = Task(
        title=data["title"],
        description=data.get("description"),
        status=data.get("status","pending"),
        priority=data.get("priority","medium"),
        user_id=user.id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created"}), 201


# @task_bp.route("", methods=["GET"])
# @token_required
# def get_tasks(user):
#     tasks = Task.query.filter_by(user_id=user.id).all()
#     return jsonify([
#         {"id":t.id,"title":t.title,"status":t.status,"priority":t.priority}
#         for t in tasks
#     ])
@task_bp.route("", methods=["GET"])
@token_required
def get_tasks(user):
    query = Task.query.filter_by(user_id=user.id)

    status = request.args.get("status")
    priority = request.args.get("priority")
    due_date = request.args.get("due_date")

    if status:
        query = query.filter_by(status=status)

    if priority:
        query = query.filter_by(priority=priority)

    if due_date:
        query = query.filter_by(due_date=due_date)

    tasks = query.all()

    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "status": t.status,
            "priority": t.priority
        } for t in tasks
    ])


@task_bp.route("/<int:id>", methods=["PUT"])
@token_required
def update_task(user, id):
    task = Task.query.filter_by(id=id, user_id=user.id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)
    task.priority = data.get("priority", task.priority)
    task.due_date = data.get("due_date", task.due_date)
    task.category_id = data.get("category_id", task.category_id)

    db.session.commit()

    return jsonify({"message": "Task updated"})


@task_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def delete_task(user,id):
    task = Task.query.filter_by(id=id,user_id=user.id).first()
    if not task:
        return jsonify({"error":"Not found"}),404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message":"Deleted"})

@task_bp.route("/<int:id>", methods=["GET"])
@token_required
def get_single_task(user, id):
    task = Task.query.filter_by(id=id, user_id=user.id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "id": task.id,
        "title": task.title,
        "status": task.status,
        "priority": task.priority,
        "due_date": task.due_date
    })
