def create_task(tasks, task_data):
    new_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {
        "id": new_id,
        **task_data.model_dump(),
    }

    tasks.append(new_task)

    return new_task


def get_all_tasks(tasks):
    return tasks


def get_task_by_id(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None


def complete_task(tasks, task_id):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        return None

    task["completed"] = True
    return task


def update_task(tasks, task_id, task_data):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        return None

    task.update(task_data.model_dump())
    return task


def delete_task(tasks, task_id):
    task = get_task_by_id(tasks, task_id)

    if task is None:
        return False

    tasks.remove(task)
    return True
