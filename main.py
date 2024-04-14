"""FastAPI Applikation zur Überwachung von Elite Dangerous Statusdaten"""

import json
import os
import asyncio
from fastapi import FastAPI
import uvicorn
from status_module import router as status_router
from cargo_module import router as cargo_router
from log_module import router as log_router, get_current_star_system

app = FastAPI(
    title="Elite Dangerous Status Check",
    version="0.0.1",
    description="Eine API zum Überwachen von Elite Dangerous Statusdaten",
)

# Filenames which should be watched for changes
files_to_watch = ["Status.json", "Cargo.json"]

# Path to the game data directory
base_path = os.path.join(
    os.environ["USERPROFILE"], "Saved Games", "Frontier Developments", "Elite Dangerous"
)

# Initial data cache
cached_data = {}


def read_and_update_files():
    """
    Reads and updates files based on the content of files_to_watch.

    This function iterates over a list of filenames, attempts to open each file,
    reads the JSON content, and then updates the cached_data dictionary with the
    content. If a file is not found or the JSON decoding fails, it prints an error message.

    Raises:
        FileNotFoundError: If a file in the files_to_watch list does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    # Iterate over each file in the files_to_watch list
    for filename in files_to_watch:
        # Construct the full path to the file
        file_path = os.path.join(base_path, filename)
        try:
            # Open the file with utf-8 encoding to read its content
            with open(file_path, "r", encoding="utf-8") as file:
                # Load the JSON content from the file
                data = json.load(file)
                # Update the cache with the new data
                cached_data[filename] = data
        except FileNotFoundError as e:
            # Print an error message if the file is not found
            print(f"File {filename} not found: {e}")
        except json.JSONDecodeError as e:
            # Print an error message if the JSON decoding fails
            print(f"Error decoding JSON in {filename}: {e}")


async def start_file_watcher():
    """
    Asynchronously start a loop that watches and updates files periodically.

    This coroutine enters an infinite loop, where it calls the `read_and_update_files`
    function to read and update the files specified. It then waits for a specified
    amount of time (10 seconds) before repeating the process.

    The loop runs indefinitely and must be cancelled externally to stop the file watching.
    """
    while True:
        # Call the function to read and update files
        read_and_update_files()
        # Wait for 10 seconds before the next iteration
        await asyncio.sleep(10)


async def app_lifespan():
    """
    Asynchronous context manager for the application's lifespan.

    This function is responsible for managing the setup and teardown
    of the application's resources. It starts the file watcher task
    on entering the context and ensures its cancellation and cleanup
    when exiting the context.

    Yields:
        None: This function is used with 'async with' and yields control
              back to the caller between the setup and teardown phases.
    """
    # Start the file watcher task asynchronously
    task = asyncio.create_task(start_file_watcher())
    try:
        # Yield control back to the event loop until the context is exited
        yield
    finally:
        # Attempt to cancel the file watcher task
        task.cancel()
        try:
            # Wait for the task to be cancelled
            await task
        except asyncio.CancelledError:
            # Handle the cancellation of the file watcher
            print("File watcher cancelled.")
        # Perform any necessary cleanup actions here
        print("Cleanup actions here")

# Configure the application's lifespan
app.router.lifespan = app_lifespan

# Include the routers for status, cargo, and log modules
app.include_router(status_router, prefix="/status")
app.include_router(cargo_router, prefix="/cargo")
app.include_router(log_router, prefix="/logs")


@app.get("/")
async def read_root():
    """Retrieve the current star system and status flags.

    This endpoint processes the status data to extract the current star system
    and the status flags 'Flags' and 'Flags2' returned by Elite Dangerous.

    Returns:
        dict: A dictionary containing the current star system, and the
              status flags 'Flags' and 'Flags2'.
    """
    # Retrieve the current star system from the log module
    current_star_system = await get_current_star_system()
    # Default to "Unknown System" if the star system is not found
    system_name = current_star_system.get("StarSystem", "System unknown")

    # Retrieve the status flags from the cached 'Status.json' data
    status_data = cached_data.get("Status.json", {})
    # Default to 0 if the flags are not found in the status data
    flags = status_data.get("Flags", 0)
    flags2 = status_data.get("Flags2", 0)

    # Return a dictionary with the system name and status flags
    return {"System": system_name, "Flags": flags, "Flags2": flags2}


# Start the FastAPI application
if __name__ == "__main__":
    try:
        uvicorn.run(app, host="{% load 0.0.0.0_tags %}", port=8888)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except asyncio.CancelledError:
        print("File watcher cancelled.")
    finally:
        print("Cleanup actions here.")
