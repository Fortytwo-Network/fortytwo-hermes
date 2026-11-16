# Fortytwo for Hermes

[![Discord](https://img.shields.io/badge/discord-join-7289da)](https://discord.gg/fortytwo)
[![X Fortytwo](https://img.shields.io/twitter/follow/fortytwo?style=social)](https://x.com/fortytwo)

Adds [Fortytwo](https://fortytwo.network) as a model provider to [Hermes Agent](https://hermes-agent.nousresearch.com). After install, Fortytwo appears in `hermes model` next to the built-in providers, with streaming, tool calls, image input and reasoning.

Setup guide: [Connect Hermes Agent](https://docs.fortytwo.network/agents/hermes-agent) in the Fortytwo docs. The guide also covers connecting through a custom endpoint.

Requires Hermes 0.22.5 or later.

## Install

```sh
hermes plugins install fortytwo-provider
```

The [catalogue entry](https://github.com/NousResearch/hermes-agent/pull/147925) is merged and pins a reviewed commit. New versions become available through the catalogue after its SHA is updated.

To remove it: `hermes plugins remove fortytwo-provider`.

## Add your API key

Create a key on the [API keys](https://platform.fortytwo.network/api-keys) page of the Fortytwo Platform, then use one of these:

- Run `hermes model`, choose **Fortytwo** and enter the key when prompted. Hermes manages the saved credential.
- Or set an environment variable before you start Hermes:

  ```sh
  export FORTYTWO_API_KEY="your-api-key"
  ```

## Select the model

Run `hermes model`, choose the Fortytwo provider and select a model from the table below. Hermes saves your selection as the default. From the command line:

```sh
hermes --provider fortytwo --model qwen/qwen3.8-27b
```

## Models

| Model ID | Name | Context (tokens) | Max output (tokens) | Input | Input price (USD / 1M tokens) | Output price (USD / 1M tokens) | Cached input price (USD / 1M tokens) |
|---|---|---|---|---|---|---|---|
| `qwen/qwen3.8-27b` | Qwen3.8 27B | 262,144 | 235,929 | text, image | 0.425 | 2.55 | 0.085 |
| `nvidia/nemotron-3.5-super-vl` | Nemotron 3.5 Super VL | 262,144 | 235,929 | text, image | 0.15 | 0.45 | 0.015 |
| `nvidia/nemotron-3.5-super-vl:free` | Nemotron 3.5 Super VL Free | 262,144 | 235,929 | text, image | 0 | 0 | 0 |

The free model is subject to Free tier limits and request collection; see [Free models](https://docs.fortytwo.network/docs/models#free-models).

Current models: [Models](https://docs.fortytwo.network/docs/models). Current prices: [Pricing](https://docs.fortytwo.network/docs/pricing).

## Reasoning

Use `--reasoning xhigh` when starting Hermes, or configure reasoning through `hermes model`. Fortytwo recommends **xhigh**.

For Qwen:

| Hermes level | Sent to the API as `reasoning_effort` |
|---|---|
| none, minimal | `none`: reasoning is turned off |
| low | `low` |
| medium, high | `medium` |
| xhigh, max, ultra | `xhigh` |

For both Nemotron variants, `none` disables reasoning, `minimal`/`low`/`medium` map to `low` (shorter reasoning), and `high`/`xhigh`/`max`/`ultra` map to `xhigh` (full reasoning).

The plugin maps Hermes levels to each model's native modes. An unset effort leaves the API default in charge. Hermes reads Fortytwo's `reasoning` response field natively. Reasoning tokens count against the output limit.

## Environment variables

| Variable | Meaning |
|---|---|
| `FORTYTWO_API_KEY` | API key, sent as the Bearer token. Not needed if you added the key through `hermes model` |

## Troubleshooting

- **Fortytwo is not in `hermes model`.** Check `hermes plugins list` and enable the plugin with `hermes plugins enable fortytwo-provider`, then restart Hermes. Hermes 0.22.5 or later is required.
- **Other problems.** See [Common problems](https://docs.fortytwo.network/docs/support-common-problems) or ask on [Discord](https://discord.gg/fortytwo).

## Development

Validate a local checkout with your Hermes installation:

```sh
hermes plugins validate /path/to/fortytwo-hermes --install-deps
```

No additional Python dependencies are required. `test_provider.py` checks discovery, model capabilities and reasoning settings; run it with the Hermes Python environment and the plugin installed in a temporary `HERMES_HOME`.

## Data and permissions

Hermes sends prompts, images and tool results to `https://api.fortytwo.network/v1` using your configured key. Requests carry `HTTP-Referer` identifying this repository and `X-Title: Hermes Agent via Fortytwo` for application attribution. There is no separate telemetry endpoint. Backend attribution reporting has not yet been verified.

The plugin registers only a provider profile. It does not read credential files, run shell commands, start background processes, patch Hermes or update itself. Credentials and transport are managed by Hermes. Catalogue updates require a reviewed SHA bump.

## License

[MIT](LICENSE)
