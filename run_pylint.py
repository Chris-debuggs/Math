import os
import subprocess
import sys

def main():
    """
    Finds and runs pylint on all Python files and directories in the current project.
    """
    # Define the core directories and files to lint
    targets = [
        "app.py",
        "content",
        "generators",
        "solvers",
        "tests",
        "visualizers"
    ]
    
    # Filter only those targets that actually exist to prevent errors
    existing_targets = [t for t in targets if os.path.exists(t)]
    
    if not existing_targets:
        print("No python packages or files found to lint.")
        sys.exit(1)

    print(f"Starting Pylint on the following targets: {', '.join(existing_targets)}")
    print("-" * 60)
    
    # Use python -m pylint to ensure we use the pylint installed in the current Python environment
    command = [sys.executable, "-m", "pylint"] + existing_targets
    
    try:
        # Run the command and let the output print directly to the console
        result = subprocess.run(command)
        
        print("-" * 60)
        if result.returncode == 0:
            print("Pylint finished successfully. No issues found! 🚀")
        else:
            print(f"Pylint finished with exit code {result.returncode}. Please review the issues above. 🛠️")
            
        sys.exit(result.returncode)
        
    except FileNotFoundError:
        print("Error: Could not execute pylint. Make sure it is installed (pip install pylint).")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while running pylint: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
