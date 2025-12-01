# Task CLI

A simple command-line task manager written in Python to track tasks with status and timestamps. Tasks are stored in a local JSON file (`tasks.json`).

## Features

- Add new tasks with descriptions.
- Update task descriptions.
- Delete tasks by ID.
- Mark tasks as `todo`, `in-progress`, or `done`.
- List tasks with optional filtering by status.
- Timestamps for task creation and updates.

## Installation

1. Clone the repository or download the script:

```bash
git clone <repository-url>
cd <repository-folder>
```
2. Make sure Python is installed

## Usage

Run the script using Python:

```bash
python task_cli.py <command> [arguments]
```

* Add as task

```bash
python task_cli.py add "Buy groceries"
```

* Update a task
```bash
python task_cli.py update 1 "Buy groceries and banana"
```

* Delete a task
```bash
python task_cli.py delete 1
```

* Mark a task as done or in-progress
```bash
python task_cli.py mark-in-progress 1
python task_cli.py mark-done 1
```

* List tasks with optional filters
```bash
python task_cli.py list
python task_cli.py list done
python task_cli.py list todo
```

# Data Storage
Tasks are saved in a JSON file (tasks.json) in the same folder as the script. Example task structure:

```json
{
  "id": 1,
  "description": "Buy groceries",
  "status": "todo",
  "createdAt": "2025-10-28 23:00:00",
  "updatedAt": "2025-10-28 23:00:00"
}
```

# License
This project is open-source and available under the MIT License.