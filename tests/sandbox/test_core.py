import json, os, sys, tempfile, unittest
from pathlib import Path

from vec_sandbox.core import filtered_environment, load_policy, run


def policy(root: Path) -> dict:
    return {"work_dir": str(root), "output_dir": str(root / "out"), "wall_seconds": 2,
            "cpu_seconds": 2, "memory_mb": 512, "file_mb": 10, "max_processes": 16,
            "network": "none", "environment_allowlist": []}


class SandboxTests(unittest.TestCase):
    def test_validation_and_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); os.environ["SECRET_TOKEN"] = "hidden"
            path = root / "policy.json"; path.write_text(json.dumps(policy(root)))
            self.assertEqual(load_policy(path)["network"], "none")
            self.assertNotIn("SECRET_TOKEN", filtered_environment([]))

    def test_run_and_timeout(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); ok = run(policy(root), [sys.executable, "-c", "print('ok')"])
            self.assertEqual(ok["returncode"], 0); self.assertIn("ok", ok["stdout"])
            short = policy(root); short["wall_seconds"] = .05
            timed = run(short, [sys.executable, "-c", "import time; time.sleep(1)"])
            self.assertEqual(timed["status"], "timeout")

    def test_reject_same_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); bad = policy(root); bad["output_dir"] = str(root)
            path = root / "bad.json"; path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError): load_policy(path)


if __name__ == "__main__": unittest.main()
