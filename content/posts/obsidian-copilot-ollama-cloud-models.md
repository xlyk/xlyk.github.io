Title: Adding Ollama Cloud Models to Obsidian Copilot by Editing data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, local ai, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: Adding Ollama Cloud models to the Obsidian Copilot plugin by editing its data.json directly: finding the active vault's config, duplicating a model entry, and verifying each tag with ollama show.

I wanted to add eleven Ollama Cloud models to the Obsidian Copilot plugin at once. The plugin adds models one at a time through its settings screen, so I edited the config file directly instead. Two things needed care: finding the config file Obsidian actually loads, and matching each Ollama tag exactly.

## Finding the active vault

Obsidian keeps app-level state separate from per-vault settings. App data lives in the application support directory; vault settings live in each vault's `.obsidian/` directory. The app registry records which vault is currently open:

```text
~/Library/Application Support/obsidian/obsidian.json
```

I had two similarly named vault directories, and only one was open; the registry identified it. The plugin config then sits at a fixed path inside that vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

In the same `.obsidian/` directory, `community-plugins.json` lists the enabled plugin IDs (including `copilot`), and `manifest.json` gives the plugin version.

## Inside data.json

`data.json` holds the settings the plugin GUI writes. The top-level fields:

```json
{
  "activeModels": [],
  "activeEmbeddingModels": [],
  "defaultModelKey": "...",
  "embeddingModelKey": "...",
  "contextTurns": 15,
  "autoCompactThreshold": 256000,
  "temperature": 0.1,
  "stream": true,
  "maxTokens": 6000,
  "reasoningEffort": "low",
  "verbosity": "medium"
}
```

The chat-model table in the GUI is the `activeModels` array. Each entry:

```json
{
  "name": "minimax-m3:cloud",
  "provider": "ollama",
  "enabled": true,
  "isBuiltIn": false,
  "baseUrl": "",
  "apiKey": "",
  "isEmbeddingModel": false,
  "capabilities": [
    "reasoning",
    "vision",
    "websearch"
  ],
  "stream": true,
  "reasoningEffort": "high",
  "numCtx": 131072
}
```

`_keychainOnly` was `true` and every `apiKey` field was empty. Model definitions live in the JSON; API keys live in the macOS Keychain, so editing this file leaves them untouched.

## Adding the models

I duplicated the existing `minimax-m3:cloud` entry for each of these models:

```text
deepseek-v4-flash
deepseek-v4-pro
gemini-3-flash-preview
gemma4
glm-5.1
gpt-oss
kimi-k2.6
kimi-k2.7-code
nemotron-3-super
nemotron-3-ultra
qwen3.5
```

Most Ollama Cloud models use a plain `:cloud` suffix, so I appended it to every name. Two then failed: `gemma4` and `gpt-oss` returned "not found". Copilot passes the configured `name` straight to Ollama, so each tag has to match an existing model exactly.

## Verifying the model tags

`ollama show` prints a model's details and errors on an unknown tag:

```bash
ollama show "<model-name>"
```

Running it on the two failures gave the correct tags:

```text
gemma4:31b-cloud
gpt-oss:20b-cloud
```

The corrected set:

```text
minimax-m3:cloud
deepseek-v4-flash:cloud
deepseek-v4-pro:cloud
gemini-3-flash-preview:cloud
gemma4:31b-cloud
glm-5.1:cloud
gpt-oss:20b-cloud
kimi-k2.6:cloud
kimi-k2.7-code:cloud
nemotron-3-super:cloud
nemotron-3-ultra:cloud
qwen3.5:cloud
```

A final `ollama show` pass confirmed every tag.

## Editing safely

If Obsidian is open while you edit, it can write its in-memory settings back over the file on shutdown and discard your changes. The procedure I used:

1. Find the active vault from `obsidian.json`.
2. Back up `data.json` with a timestamp.
3. Edit only the `activeModels` array.
4. Validate the JSON with `jq`.
5. Confirm each tag with `ollama show`.
6. Restart Obsidian so the plugin reloads the file.

## Reference

- Chat models live in `activeModels`; embedding models in `activeEmbeddingModels`.
- `defaultModelKey` uses a `<model>|<provider>` format.
- With `_keychainOnly` set, API keys stay in the Keychain, not the JSON.
- Model `name` values must be exact Ollama tags, not the GUI's display names.
