"""Run with Hermes on PYTHONPATH and this plugin installed in a scratch home."""

import unittest

from providers import get_provider_profile
from agent.models_dev import get_model_capabilities


class ProviderTest(unittest.TestCase):
    def test_discovery_and_capabilities(self):
        profile = get_provider_profile("fortytwo")
        self.assertEqual(profile.base_url, "https://api.fortytwo.network/v1")
        caps = get_model_capabilities("fortytwo", "qwen/qwen3.8-27b", allow_network=False)
        self.assertTrue(caps.supports_vision)
        self.assertTrue(caps.supports_tools)
        self.assertTrue(caps.supports_reasoning)
        self.assertEqual(caps.context_window, 262144)

    def test_all_models_and_description(self):
        profile = get_provider_profile("fortytwo")
        models = ("qwen/qwen3.8-27b", "nvidia/nemotron-3.5-super-vl",
                  "nvidia/nemotron-3.5-super-vl:free")
        self.assertEqual(profile.fallback_models, models)
        self.assertEqual(profile.description, "Fortytwo — Better answers from open models")
        for model in models:
            with self.subTest(model=model):
                caps = get_model_capabilities("fortytwo", model, allow_network=False)
                self.assertTrue(caps.supports_vision)
                self.assertTrue(caps.supports_tools)
                self.assertTrue(caps.supports_reasoning)
                self.assertEqual(caps.context_window, 262144)

    def test_nemotron_reasoning_modes(self):
        profile = get_provider_profile("fortytwo")
        for model in ("nvidia/nemotron-3.5-super-vl", "nvidia/nemotron-3.5-super-vl:free"):
            for requested, expected in (("none", "none"), ("minimal", "low"),
                                        ("low", "low"), ("medium", "low"),
                                        ("high", "xhigh"), ("xhigh", "xhigh"),
                                        ("max", "xhigh"), ("ultra", "xhigh")):
                with self.subTest(model=model, effort=requested):
                    self.assertEqual(profile.build_api_kwargs_extras(
                        model=model, reasoning_config={"effort": requested}),
                        ({}, {"reasoning_effort": expected}))
            self.assertEqual(profile.build_api_kwargs_extras(model=model), ({}, {}))
            self.assertEqual(profile.build_api_kwargs_extras(
                model=model, reasoning_config={"enabled": False, "effort": "high"}),
                ({}, {"reasoning_effort": "none"}))
        with self.assertRaises(ValueError):
            profile.build_api_kwargs_extras(reasoning_config={"effort": "invalid"})

    def test_reasoning_wire_and_disabled_default(self):
        profile = get_provider_profile("fortytwo")
        self.assertEqual(profile.build_api_kwargs_extras(), ({}, {}))
        self.assertEqual(profile.build_api_kwargs_extras(reasoning_config={"enabled": False}),
                         ({}, {"reasoning_effort": "none"}))
        for requested, expected in (("none", "none"), ("low", "low"),
                                    ("medium", "medium"), ("xhigh", "xhigh"),
                                    ("high", "medium"), ("max", "xhigh")):
            with self.subTest(requested=requested):
                self.assertEqual(profile.build_api_kwargs_extras(reasoning_config={"effort": requested}),
                                 ({}, {"reasoning_effort": expected}))


if __name__ == "__main__":
    unittest.main()
