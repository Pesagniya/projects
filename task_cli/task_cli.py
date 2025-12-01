import json
import os
from argparse import ArgumentParser
from datetime import datetime

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_task(description):
    tasks = load_tasks()
    new_id = tasks[-1]["id"] + 1 if tasks else 1
    now = get_timestamp()
    task = {
        "id": new_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print("Error: Task not found.")
        return
    task["description"] = new_description
    task["updatedAt"] = get_timestamp()
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print("Error: Task not found.")
        return
    save_tasks(new_tasks)
    print(f"Task {task_id} deleted successfully.")

def mark_task(task_id, status):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if not task:
        print("Error: Task not found.")
        return
    if status not in ["in-progress", "done", "todo"]:
        print("Error: Invalid status.")
        return
    task["status"] = status
    task["updatedAt"] = get_timestamp()
    save_tasks(tasks)
    print(f"Task {task_id} marked as {status}.")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return

    filtered = tasks
    if filter_status:
        filtered = [t for t in tasks if t["status"] == filter_status]

    if not filtered:
        print(f"No tasks with status '{filter_status}'.")
        return

    for t in filtered:
        print(f"[{t['id']}] {t['description']} — {t['status']} (Updated: {t['updatedAt']})")

# ------------------ CLI setup ------------------

def main():
    parser = ArgumentParser(prog="task-cli", description="Task Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")

    # Update
    upd_parser = subparsers.add_parser("update", help="Update a task description")
    upd_parser.add_argument("id", type=int, help="Task ID")
    upd_parser.add_argument("description", type=str, help="New description")

    # Delete
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID")

    # Mark done/in-progress
    mark_done = subparsers.add_parser("mark-done", help="Mark a task as done")
    mark_done.add_argument("id", type=int)

    mark_prog = subparsers.add_parser("mark-in-progress", help="Mark a task as in-progress")
    mark_prog.add_argument("id", type=int)

    # List
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("status", nargs="?", help="Filter by status (todo, done, in-progress)")

    args = parser.parse_args()

    # Handle commands
    if args.command == "add":
        add_task(args.description)
    elif args.command == "update":
        update_task(args.id, args.description)
    elif args.command == "delete":
        delete_task(args.id)
    elif args.command == "mark-done":
        mark_task(args.id, "done")
    elif args.command == "mark-in-progress":
        mark_task(args.id, "in-progress")
    elif args.command == "list":
        list_tasks(args.status)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
