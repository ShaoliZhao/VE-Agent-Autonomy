import json
from pathlib import Path
root=Path(__file__).parent; (root/"prompt.txt").write_text("Create a deterministic demo artifact.\n"); (root/"input.txt").write_text("demo\n")
(root/"controller.py").write_text("from pathlib import Path\nPath('examples/harness/final.bin').write_bytes(b'agent-output')\n")
config={"framework":"demo","model":"deterministic-demo","command":["python3","examples/harness/controller.py"],"prompts":[str(root/"prompt.txt")],"harness_files":[str(root/"controller.py")],"inputs":[str(root/"input.txt")],"budget":{"wall_seconds":30,"max_candidates":1},"final_artifact":str(root/"final.bin")}
(root/"demo-config.json").write_text(json.dumps(config,indent=2)+"\n")
