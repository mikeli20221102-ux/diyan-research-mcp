from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from diyan_research_mcp.backend import BackendError, raise_for_status
from diyan_research_mcp.config import ConfigError, load_backend_config
from diyan_research_mcp.policy import PolicyError, require_safe_query, safe_research_output
from diyan_research_mcp import server


class ConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        for name in ("DIYAN_API_KEY", "DIYAN_BACKEND_URL", "DIYAN_TIMEOUT_SECONDS"):
            os.environ.pop(name, None)

    tearDown = setUp

    def test_missing_key_fails_closed_with_actionable_message(self) -> None:
        with self.assertRaisesRegex(ConfigError, "DIYAN_API_KEY"):
            load_backend_config()

    def test_plaintext_backend_is_rejected(self) -> None:
        os.environ["DIYAN_API_KEY"] = "k"
        os.environ["DIYAN_BACKEND_URL"] = "http://api.example/v1"
        with self.assertRaisesRegex(ConfigError, "HTTPS"):
            load_backend_config()

    def test_out_of_range_timeout_falls_back_to_default(self) -> None:
        os.environ["DIYAN_API_KEY"] = "k"
        os.environ["DIYAN_TIMEOUT_SECONDS"] = "9999"
        self.assertEqual(load_backend_config().timeout, 30.0)


class PolicyTests(unittest.TestCase):
    def test_transaction_fields_and_terms_are_stripped(self) -> None:
        envelope = safe_research_output(
            {"final_action": "买入", "summary": "建议重仓，预期收益承诺"},
            source="test",
        )
        self.assertNotIn("final_action", envelope["result"])
        self.assertNotIn("买入", envelope["result"]["summary"])
        self.assertNotIn("重仓", envelope["result"]["summary"])
        self.assertTrue(envelope["research_boundary"]["transaction_fields_removed"])

    def test_trade_flavoured_question_is_rejected(self) -> None:
        with self.assertRaises(PolicyError):
            require_safe_query("现在建议买入吗？")

    def test_usage_is_omitted_when_backend_sends_none(self) -> None:
        self.assertNotIn("usage", safe_research_output({}, source="test"))


class BackendStatusTests(unittest.TestCase):
    def test_success_status_passes(self) -> None:
        self.assertIsNone(raise_for_status(200))

    def test_quota_exhausted_is_explained(self) -> None:
        with self.assertRaisesRegex(BackendError, "配额"):
            raise_for_status(429)

    def test_unmapped_status_still_fails(self) -> None:
        with self.assertRaisesRegex(BackendError, "503"):
            raise_for_status(503)


class ToolTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ.pop("DIYAN_API_KEY", None)

    def test_unknown_framework_never_reaches_backend(self) -> None:
        result = server.framework_excerpt("nope")
        self.assertEqual(result["error_type"], "request")

    def test_missing_credentials_surface_as_config_error(self) -> None:
        result = server.stock_snapshot_latest()
        self.assertEqual(result["error_type"], "config")

    def test_trade_question_is_blocked_before_any_call(self) -> None:
        result = server.research_analyze_safe("600519", "该不该加仓")
        self.assertEqual(result["error_type"], "policy")


if __name__ == "__main__":
    unittest.main()
