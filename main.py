import json, os, requests, uuid
from flask import *
app = Flask(__name__)


try: os.mkdir("tmp")
except: pass

try:
    with open("./copier.json", "r") as f:
        global conf
        conf = json.load(f)
except:
    print("Please create `copier.json` config file")
    os._exit(1)


def proxy(url: str):
    script = ""
    try:
        if conf["script"]: script = open(conf["script"], "r").read()
    except: print(f"Script not found: {conf['script']}")
    

    target_url = f"{conf['target']}/{url}"

    method = request.method
    data = request.data

    headers = request.headers
    
    res = eval(
        f"requests.{method.lower()}(target_url, {data}, json='{data}')"
    )

    res_headers = res.headers
    res_data = res.content

    if "</html>" in res.text:
        return f"""
        {res.text.split('</body></html>')[0]}
        <script>
            const route = '/{url}';
            let routes = route.split("/");
            routes.shift();
            if (routes[routes.length-1] == "")
                routes.pop();
            console.log(
            `This page copied with Copier by Yasir Eymen Kayabaşı, use for only educational purposes.`
            );
        </script>
        <script>{script}</script>
        </body></html>
        """
    return res_data


app = Flask(__name__)

try:
    for action in conf["actions"]:
        f:open
        try: f = open(action[1], "r")
        except:
            print(f"Action not found: {action[1]}")
            break
        script = f.readlines()
        for line in script:
            script[script.index(line)] = f"    {line}".split("\n")[0]
        script_final = "\n".join(script)
        name = "a"+str(uuid.uuid4()).replace("-", "")
        out = f"""
@app.route("{action[0]}")
def {name}():
{script_final}
        """
        with open(f"tmp/{name}.py", "w") as f2:
            f2.write(out)
        exec(compile(open(f"tmp/{name}.py").read(), name, "exec"))
except: print("Continuing without actions")

@app.route("/", methods=[
    "GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"
])
def master(): return proxy("")

@app.route("/<path:url>", methods=[
    "GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"
])
def other(url): return proxy(url)



