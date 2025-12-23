import time

def send_email(to: str, subject: str):
    print(f"Sending email to {to}: {subject}")
    time.sleep(2)  # Simulate work

def process_image(url: str):
    print(f"Processing image from {url}")
    # Simulate failure on certain calls for testing retries
    if "fail" in url:
        raise Exception("Image processing failed")
    time.sleep(3)

# Registry
TASK_REGISTRY = {
    "send_email": send_email,
    "process_image": process_image,
}