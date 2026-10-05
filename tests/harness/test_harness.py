import json,tempfile,unittest
from pathlib import Path
from vec_harness.core import lock, verify

class HarnessTests(unittest.TestCase):
    def test_lock_detects_mutation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); source=root/"prompt"; source.write_text("x")
            cfg={"framework":"x","model":"m","command":["true"],"prompts":[str(source)],"harness_files":[],"inputs":[],"budget":{},"final_artifact":str(root/"final")}
            path=root/"config.json"; path.write_text(json.dumps(cfg)); lock(path,root/"run")
            self.assertEqual(verify(root/"run"),[]); source.write_text("y"); self.assertTrue(verify(root/"run"))

if __name__=="__main__": unittest.main()
