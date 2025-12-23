def execute_task(task_type, payload):
    if task_type == "send_email":
        print(f"Sending email to {payload['to']}")
    elif task_type == "process_data":
        print(f"Processing data: {payload}")
    else:
        raise Exception("Unknown task type")
