Title: Adding Ollama Cloud Models to Obsidian Copilot by Editing data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, local ai, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: Adding Ollama Cloud models to the Obsidian Copilot plugin by editing its data.json: finding the active vault's config, duplicating a model entry, and verifying tags with ollama show.

I wanted to add eleven Ollama Cloud models to the Obsidian Copilot plugin. Its settings screen adds them one at a time, so I edited the config file directly. Two things needed care: finding the file Obsidian actually loads, and matching each Ollama tag exactly.

## Finding the active vault

Obsidian keeps app-level state in the application support directory and per-vault settings in each vault's `.obsidian/`. The app registry records which vault is open:

```text
~/Library/Application Support/obsidian/obsidian.json
```

I had two similarly named vaults; the registry showed which one was open. Its Copilot config sits at:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

## Inside data.json

`data.json` holds the settings the GUI writes. Top-level fields:

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

Chat models go in `activeModels`, embeddings in `activeEmbeddingModels`; `defaultModelKey` and `embeddingModelKey` pick the defaults, in `<model>|<provider>` form. Each `activeModels` entry:

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

`_keychainOnly` was `true` and every `apiKey` field was empty: API keys live in the macOS Keychain, not the JSON, so editing the file never touches them.

## Adding the models

I duplicated the `minimax-m3:cloud` entry for each of these:

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

Most Ollama Cloud models use a plain `:cloud` suffix, so I appended it to every name. Two failed: `gemma4` and `gpt-oss` returned "not found". Copilot passes `name` straight to Ollama, so each tag must match an existing model exactly.

## Verifying the model tags

`ollama show` prints a model's details and errors on an unknown tag:

```bash
ollama show "<model-name>"
```

On the two failures it gave the correct tags:

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

## Editing safely

If Obsidian is open while you edit, it can overwrite the file with its in-memory settings on shutdown, discarding your changes. The procedure I used:

1. Find the active vault from `obsidian.json`.
2. Back up `data.json` with a timestamp.
3. Edit only the `activeModels` array.
4. Validate the JSON with `jq`.
5. Confirm each tag with `ollama show`.
6. Restart Obsidian so the plugin reloads the file.
