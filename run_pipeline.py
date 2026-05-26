import os
import subprocess
import time
import webbrowser
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

def run_command(command, cwd=None):
    """Executes a terminal command in a specific folder and stops if it fails."""
    print(f"\n>>> Executing: {' '.join(command)} (in {os.path.basename(cwd) if cwd else '.'}/)")
    result = subprocess.run(command, cwd=cwd)
    if result.returncode != 0:
        print(f"\nCRITICAL ERROR: Failed to run {' '.join(command)}. Exiting pipeline.")
        exit(1)

def serve_dashboard(docs_dir):
    """Hosts the local web server for the dashboard."""
    os.chdir(docs_dir)
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("="*60)
    print("   GREEN GRID SIMULATION - END-TO-END PIPELINE AUTOMATION")
    print("="*60)

    # Get the root directory of the project
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: Train the ML Model (Grid Search)
    run_command(['python', 'train_model.py'], cwd=os.path.join(root_dir, 'ml'))

    # Step 2: Run the SimPy Simulation Engine
    run_command(['python', 'main.py'], cwd=os.path.join(root_dir, 'simulator'))

    # Step 3: Start the Web Server in the background
    docs_dir = os.path.join(root_dir, 'docs')
    print("\n>>> Spinning up Dashboard Server at http://localhost:8000...")
    server_thread = threading.Thread(target=serve_dashboard, args=(docs_dir,), daemon=True)
    server_thread.start()

    # Wait a brief moment to ensure the server is online
    time.sleep(1.5)

    # Step 4: Automatically open the browser
    print(">>> Opening Interactive Dashboard in your default web browser...")
    webbrowser.open('http://localhost:8000')

    print("\n" + "="*60)
    print("PIPELINE COMPLETE! Dashboard is live.")
    print("Press Ctrl+C in this terminal to shut down the web server.")
    print("="*60 + "\n")
    
    # Keep the script running so the web server doesn't close
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down pipeline and server. Goodbye!")
