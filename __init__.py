"""Fortytwo provider for Hermes, using the public provider-profile API."""

from providers import register_provider
from providers.base import ProviderProfile

MODEL = "qwen/qwen3.8-27b"
EFFORTS = ("none", "low", "medium", "xhigh")


class FortytwoProfile(ProviderProfile):
    def build_api_kwargs_extras(self, *, reasoning_config=None, **context):
        if reasoning_config is None:
            return {}, {}
        if reasoning_config.get("enabled") is False:
            return {}, {"reasoning_effort": "none"}
        effort = reasoning_config.get("effort")
        if effort is None:
            return {}, {}
        # Hermes has a wider ladder. Advertise native levels and round down.
        effort = {"minimal": "none", "high": "medium", "max": "xhigh",
                  "ultra": "xhigh"}.get(effort, effort)
        if effort not in EFFORTS:
            raise ValueError(f"Unsupported reasoning effort: {effort}")
        return {}, {"reasoning_effort": effort}


register_provider(FortytwoProfile(
    name="fortytwo",
    display_name="Fortytwo",
    description="Qwen3.8 27B on Fortytwo",
    signup_url="https://platform.fortytwo.network",
    env_vars=("FORTYTWO_API_KEY",),
    base_url="https://api.fortytwo.network/v1",
    api_mode="chat_completions",
    fallback_models=(MODEL,),
    supports_streaming=True,
    supports_vision=True,
    default_headers={
        "HTTP-Referer": "https://github.com/Fortytwo-Network/fortytwo-hermes",
        "X-Title": "Hermes Agent via Fortytwo",
    },
    model_capabilities={MODEL: {
        "supports_reasoning": True,
        "supports_vision": True,
        "supports_tools": True,
        "context_window": 262144,
    }},
))
