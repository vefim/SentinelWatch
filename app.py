import os
import hashlib
import time
import psutil
from flask import Flask, render_template, jsonify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

app = Flask(__name__)

# Global variables to store data for the dashboard
file_hashes = {}
alerts = []
file_sizes = {}  # Store file sizes for Z-score calculation
path_to_watch = r"C:\Users\victo\Downloads"  # Specify the directory to monitor
file_analytics = {"Text Files": 0, "Images": 0, "Videos": 0, "Others": 0}


def calculate_z_score(file_size):
    """Calculate Z-score for a file size."""
    if not file_sizes:
        return 0  # No data to calculate Z-score
    mean_size = sum(file_sizes.values()) / len(file_sizes)
    variance = sum((size - mean_size) ** 2 for size in file_sizes.values()) / len(file_sizes)
    std_dev = variance ** 0.5
    if std_dev == 0:
        return 0  # Avoid division by zero
    return (file_size - mean_size) / std_dev


def validate_system_data(system_data):
    """Ensure system data values are within expected ranges."""
    if not (0 <= system_data["CPU Usage"] <= 100):
        system_data["CPU Usage"] = 50  # Replace with actual data collection method
    if not (0 <= system_data["Memory Usage"] <= 100):
        system_data["Memory Usage"] = 50  # Replace with actual data collection method
    if not (0 <= system_data["Disk I/O"] <= 100):
        system_data["Disk I/O"] = 50  # Replace with actual data collection method
    return system_data


def get_system_metrics():
    """Fetch real-time system metrics using psutil."""
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage percentage
    memory_usage = psutil.virtual_memory().percent  # Memory usage percentage
    
    # For demonstration, calculate disk I/O usage as a percentage
    disk_total = psutil.disk_usage('/').total
    disk_used = psutil.disk_usage('/').used
    disk_io_percent = (disk_used / disk_total) * 100

    return {
        "CPU Usage": cpu_usage,
        "Memory Usage": memory_usage,
        "Disk I/O": disk_io_percent  # Disk usage as percentage
    }


class ChangeHandler(FileSystemEventHandler):
    """Handles file system events."""

    def on_created(self, event):
        if not event.is_directory:
            print(f'Created: {event.src_path}')
            process_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f'Modified: {event.src_path}')
            process_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            print(f'Deleted: {event.src_path}')
            file_hashes.pop(event.src_path, None)  # Remove from hash storage
            file_sizes.pop(event.src_path, None)  # Remove from size storage


def hash_file(filepath):
    """Generate SHA-256 hash for the given file."""
    try:
        if not os.path.isfile(filepath):  # Check if file exists
            print(f"Error: {filepath} is not a valid file.")
            return None
        
        with open(filepath, 'rb') as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return file_hash.hexdigest()
    except Exception as e:
        print(f'Error hashing file {filepath}: {e}')
        return None


def categorize_file(filepath):
    """Categorize a file based on its extension."""
    _, ext = os.path.splitext(filepath.lower())
    if ext in ['.txt', '.docx', '.pdf']:
        return "Text Files"
    elif ext in ['.jpg', '.png', '.gif']:
        return "Images"
    elif ext in ['.mp4', '.mkv', '.avi']:
        return "Videos"
    else:
        return "Others"


def process_file(filepath):
    """Process a file for integrity and analytics."""
    try:
        file_size = os.path.getsize(filepath)  # Get file size in bytes
        file_sizes[filepath] = file_size  # Track file size for Z-score calculation

        current_hash = hash_file(filepath)
        if current_hash:
            category = categorize_file(filepath)
            file_analytics[category] += 1

            # Z-score calculation and classification
            current_z_score = calculate_z_score(file_size)
            z_score_status = "low risk" if -2 <= current_z_score <= 2 else "high risk"

            # Check if integrity issue has been detected
            if current_hash != file_hashes.get(filepath):
                alerts.append({
                    "message": f"Integrity issue detected for {os.path.basename(filepath)} "
                               f"(Z-score: {current_z_score:.2f}, Status: {z_score_status})",
                    "time": time.strftime("%Y-%m-%d %I:%M %p")
                })
                file_hashes[filepath] = current_hash
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] File: {filepath} | "
                      f"Z-score: {current_z_score:.2f} ({z_score_status})")
    except Exception as e:
        print(f'Error processing file {filepath}: {e}')


@app.route('/')
def dashboard():
    """Render the dashboard page."""
    system_metrics = get_system_metrics()
    validated_system_data = validate_system_data(system_metrics)
    return render_template('index.html', system_data=validated_system_data)


@app.route('/alerts')
def get_alerts():
    """API route to fetch live alerts."""
    serializable_alerts = [{"message": alert.get("message", ""), "time": alert.get("time", "")} for alert in alerts if alert]
    return jsonify(alerts=serializable_alerts)


@app.route('/analytics')
def get_analytics():
    """API route to fetch file analytics."""
    return jsonify(file_analytics=file_analytics)


@app.route('/system-health')
def get_system_health():
    """API route to fetch system health metrics for monitoring."""
    system_metrics = get_system_metrics()
    return jsonify(system_metrics=system_metrics)


@app.route('/file-activity')
def get_file_activity():
    """API route to fetch file activity data for visualization."""
    total_files = sum(file_analytics.values())
    if total_files == 0:
        file_activity_percentages = {k: "No data yet" for k in file_analytics.keys()}
    else:
        file_activity_percentages = {k: (v / total_files) * 100 for k, v in file_analytics.items()}
    return jsonify(file_activity=file_activity_percentages)


def run_monitor():
    """Start monitoring the specified directory."""
    if not os.path.exists(path_to_watch):
        print(f"Error: The directory {path_to_watch} does not exist.")
        return
    
    observer = Observer()
    observer.schedule(ChangeHandler(), path_to_watch, recursive=False)
    observer.start()
    print(f'Started monitoring: {path_to_watch}')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    from threading import Thread
    monitor_thread = Thread(target=run_monitor)
    monitor_thread.start()
    app.run(debug=True, use_reloader=False)


