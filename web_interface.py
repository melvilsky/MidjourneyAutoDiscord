import subprocess
import threading
import yaml
from flask import (
    Flask,
    render_template_string,
    redirect,
    url_for,
    request,
)
from load_config import load_config, TXT_PATH

app = Flask(__name__)

process = None
log_lines = []

# Shared navigation bar for all pages
NAVIGATION = """
    <nav>
        <a href='{{ url_for('index') }}'>Home</a> |
        <a href='{{ url_for('show_config') }}'>Config</a> |
        <a href='{{ url_for('edit_prompts') }}'>Prompts</a>
    </nav>
"""


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
        """ + NAVIGATION + """
        <form action='{{ url_for('start') }}' method='post'>
            <button type='submit' {{ 'disabled' if running else '' }}>Start</button>
        </form>
        <form action='{{ url_for('pause') }}' method='post'>
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


@app.route('/config')
def show_config():
    config = load_config()
    html = """
    <html>
    <head><title>Config</title></head>
    <body>
        <h1>Current Configuration</h1>
        """ + NAVIGATION + """
        <pre>{{ config_text }}</pre>
    </body>
    </html>
    """
    return render_template_string(html, config_text=yaml.dump(config, allow_unicode=True))


@app.route('/prompts', methods=['GET', 'POST'])
def edit_prompts():
    message = ""
    if request.method == 'POST':
        new_text = request.form.get('prompts', '')
        with open(TXT_PATH, 'w', encoding='utf-8') as f:
            f.write(new_text)
        message = "Saved!"
    with open(TXT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    html = """
    <html>
    <head><title>Edit Prompts</title></head>
    <body>
        <h1>Edit Prompts</h1>
        """ + NAVIGATION + """
        <form method='post'>
            <textarea name='prompts' rows='20' cols='80'>{{ content }}</textarea><br>
            <button type='submit'>Save</button>
        </form>
        <p>{{ message }}</p>
    </body>
    </html>
    """
    return render_template_string(html, content=content, message=message)


if __name__ == '__main__':
    app.run(debug=True)

