import subprocess
import threading
from flask import Flask, render_template_string, redirect, url_for

app = Flask(__name__)

process = None
log_lines = []


def read_output(proc):
    """Read subprocess output and store it for display."""
    for line in proc.stdout:
        log_lines.append(line.rstrip())


@app.route('/')
def index():
    running = process is not None and process.poll() is None
    html = """
    <html>
    <head><title>Midjourney Auto Discord</title></head>
    <body>
        <h1>Midjourney Auto Discord</h1>
        <form action='/start' method='post'>
            <button type='submit' {{ 'disabled' if running else '' }}>Start</button>
        </form>
        <form action='/pause' method='post'>
            <button type='submit' {{ '' if running else 'disabled' }}>Pause</button>
        </form>
        <pre>{{ logs }}</pre>
    </body>
    </html>
    """
    return render_template_string(html, running=running, logs="\n".join(log_lines[-100:]))


@app.route('/start', methods=['POST'])
def start():
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen(
            ['python', 'discord_print.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        threading.Thread(target=read_output, args=(process,), daemon=True).start()
    return redirect(url_for('index'))


@app.route('/pause', methods=['POST'])
def pause():
    global process
    if process and process.poll() is None:
        process.terminate()
        process.wait()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

