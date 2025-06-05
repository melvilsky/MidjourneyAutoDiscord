import subprocess
import threading
from flask import Flask, render_template_string, redirect, url_for, request

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
    <head>
        <title>Midjourney Auto Discord</title>
        <script src='https://unpkg.com/vue@3/dist/vue.global.prod.js'></script>
        <style>
            body { font-family: Arial, sans-serif; }
            ul { list-style: none; padding: 0; display: flex; }
            li { padding: 10px 20px; cursor: pointer; border: 1px solid #ccc; }
            .active { background-color: #ddd; }
            textarea { width: 100%; height: 400px; }
            pre { white-space: pre-wrap; border:1px solid #ccc; padding:10px; }
        </style>
    </head>
    <body>
    <div id='app'>
        <ul>
            <li :class="{active: tab==='control'}" @click="tab='control'">Control</li>
            <li :class="{active: tab==='config'}" @click="tab='config'">Config</li>
            <li :class="{active: tab==='prompts'}" @click="tab='prompts'">Prompts</li>
        </ul>
        <div v-if="tab==='control'">
            <h1>Midjourney Auto Discord</h1>
            <button @click="start" :disabled="running">Start</button>
            <button @click="pause" :disabled="!running">Pause</button>
            <pre>{{ logs }}</pre>
        </div>
        <div v-if="tab==='config'">
            <h2>config.yaml</h2>
            <textarea v-model="configText" @input="autoSaveConfig"></textarea>
        </div>
        <div v-if="tab==='prompts'">
            <h2>mj_gen.txt</h2>
            <textarea v-model="promptsText"></textarea><br>
            <button @click="savePrompts">Save</button>
        </div>
    </div>
    <script>
    const { createApp } = Vue;
    createApp({
        data() {
            return {
                tab: 'control',
                running: {{ 'true' if running else 'false' }},
                logs: `{{ logs }}`,
                configText: '',
                promptsText: ''
            }
        },
        mounted() {
            this.loadConfig();
            this.loadPrompts();
        },
        methods: {
            start() {
                fetch('/start', {method:'POST'}).then(()=>{this.running=true;});
            },
            pause() {
                fetch('/pause', {method:'POST'}).then(()=>{this.running=false;});
            },
            loadConfig() {
                fetch('/config').then(r=>r.text()).then(t=>{ this.configText = t; });
            },
            autoSaveConfig() {
                fetch('/config', {method:'POST', body:this.configText});
            },
            loadPrompts() {
                fetch('/prompts').then(r=>r.text()).then(t=>{ this.promptsText = t; });
            },
            savePrompts() {
                fetch('/prompts', {method:'POST', body:this.promptsText});
            }
        }
    }).mount('#app');
    </script>
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


@app.route('/config', methods=['GET', 'POST'])
def config_file():
    path = 'config.yaml'
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
        return '', 204
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/prompts', methods=['GET', 'POST'])
def prompts_file():
    path = 'mj_gen.txt'
    if request.method == 'POST':
        data = request.data.decode('utf-8')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(data)
        return '', 204
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    app.run(debug=True)

