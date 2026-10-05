import tempfile
import unittest
from pathlib import Path

from vec_search.core import Ledger, aggregate, promote


class SearchTests(unittest.TestCase):
    def test_aggregate_and_deterministic_promotion(self):
        rows = [{"candidate_id": "b", "metrics": {"x": .5}}, {"candidate_id": "a", "metrics": {"x": .5}}]
        self.assertEqual(aggregate({"x": .5}, {"x": 1}), .5)
        self.assertEqual(promote(rows, {"x": 1}, .5), ["a"])

    def test_hash_chain_detects_edit(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = Ledger(Path(directory) / "ledger.jsonl")
            ledger.append("init", {"budget": 2}); ledger.append("result", {"cost": 1})
            self.assertTrue(ledger.verify())
            ledger.path.write_text(ledger.path.read_text().replace('"cost": 1', '"cost": 9'))
            self.assertFalse(ledger.verify())


if __name__ == "__main__": unittest.main()
