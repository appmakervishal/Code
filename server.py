# ⚠️ WARNING: This server provides full access to your PC's command line.
# It is extremely insecure and should NEVER be run on a public network or used for anything
# other than educational purposes in a secure, isolated environment.

from flask import Flask, render_template, request, jsonify
import subprocess
import os
import platform

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main HTML page for the web terminal."""
    return render_template('index.html')

@app.route('/execute_command', methods=['POST'])
def execute_command():
    """
    Executes a command received from the web interface.
    This function is the core of the application and the source of its
    security vulnerability due to the use of shell=True.
    """
    command = request.json.get('command')
    if not command:
        return jsonify({'output': 'Error: No command provided.'})

    try:
        # Popen is used to avoid blocking the Flask application for long commands.
        # shell=True allows full command execution in the system's shell (e.g., CMD).
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        stdout, stderr = process.communicate()
        
        # Format the output to look like a terminal
        output = f"{os.getcwd()}> {command}\n{stdout}{stderr}"
        
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'output': f'An error occurred: {str(e)}'})

if __name__ == '__main__':
    # Run the Flask server. It will be accessible at http://127.0.0.1:5000
    app.run(debug=True)
