# Fortytwo for Hermes

Adds Fortytwo to Hermes's provider picker using its public provider-profile API.
Requires Hermes 0.22.5 or later. Model: `qwen/qwen3.8-27b`, with text and image
input, streaming, tool calls, reasoning and a 262,144-token context window.

## Install

Until the catalogue entry is accepted, install from this repository:

```sh
hermes plugins install https://github.com/Fortytwo-Network/fortytwo-hermes
```

Once listed in the Hermes catalogue:

```sh
hermes plugins install fortytwo-provider
```

Get an API key from [Fortytwo](https://platform.fortytwo.network), then use
`hermes model` to select **Fortytwo** and enter the key through Hermes's prompt.
Alternatively, supply `FORTYTWO_API_KEY` through your environment or Hermes's
credential settings. Select `qwen/qwen3.8-27b`.

The plugin sends native efforts `none`, `low`, `medium` and `xhigh`. Unset effort
leaves the API default in charge. Wider Hermes levels round down to the nearest
offered level. Hermes reads Fortytwo's `reasoning` response field natively.

See [models](https://docs.fortytwo.network/docs/models),
[OpenAI compatibility](https://docs.fortytwo.network/docs/openai-compatibility)
and the [Hermes guide](https://docs.fortytwo.network/agents/hermes-agent).

## Data and permissions

Hermes sends prompts, images and tool results to `https://api.fortytwo.network/v1`
using the key you configure. Requests carry `HTTP-Referer` identifying this
repository and `X-Title: Hermes Agent via Fortytwo` for application attribution.
There is no separate telemetry endpoint. Backend attribution reporting has not
yet been verified.

The plugin registers only a provider profile. It does not read credential files,
run shell commands, start background processes, patch Hermes or update itself.
Credentials and transport are managed by Hermes. Catalogue updates require a
reviewed SHA bump. No additional Python dependencies are required.
