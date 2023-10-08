import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tasks import analyze_and_rename_document_task  # Importing the Celery task
import time

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'watcher.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        logging.info(f"{event.src_path} has been added!")
        if not event.is_directory:
            analyze_and_rename_document_task.delay(event.src_path)

def start_watching(path="."):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        logging.error(f"Error in watcher: {str(e)}")
    observer.join()

if __name__ == "__main__":
  # This needs to be changed depending on where the files will be watched. May need to find a smarter way to make the change.
    start_watching("/Users/kfelder/Desktop/CHRA")
