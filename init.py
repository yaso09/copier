import json

print("{\n\t/*")
target = input("\t* Target domain (https://example.com): ")
if not target: target = "https://example.com"
script = input("\t* JavaScript script (./script.js): ")
if not script: script = "./script.js"
action = input("\t* How much action will you add? (0): ")
if not action: action = 0
actions = []
for i in range(0, int(action)):
    actions.append([
        input("\t* Action route: "),
        input("\t* Python script: ")
    ])
print("\t*/")
print(f'\t"target": "{target}",')
if action == 0: print(f'\t"script": "{script}"')
else:
    print(f'\t"script": "{script}",')
    print('\t"actions": [')
for selection in actions:
    print(f'\t\t["{selection[0]}", "{selection[1]}"]')
if not action == 0: print("\t]")
print("}")
ok = input("\nIs this OK? (yes): ")

if not ok: ok = "yes"
if ok == "yes":

    out = {}
    out["target"] = target
    out["script"] = script
    out["actions"] = []

    for selection in actions:
        out["actions"].append([
            selection[0], selection[1]
        ])

    with open("copier.json", "w") as f:
        json.dump(out, f, indent=4)

    print("Saved to `copier.json`")

else: print("Aborted")

