Title: Configuring Obsidian Copilot Models by Editing data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, local ai, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: How to configure the Obsidian Copilot plugin's models by editing data.json directly instead of the GUI. Works for any provider; shown here with a batch of Ollama Cloud models.

Obsidian Copilot keeps its model configuration in a JSON file, and editing that file directly beats clicking through the settings GUI for any bulk change. Because each model entry just names a `provider`, the same approach works whatever you run: OpenAI, Anthropic, a local server, or Ollama Cloud. I used it to add a batch of Ollama Cloud models at once. Two things needed care: finding the file Obsidian actually loads, and getting each model name right.

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

The `provider` field is what makes this general: set it to `ollama`, `openai`, `anthropic`, and so on, and Copilot routes the model accordingly. `_keychainOnly` was `true` and every `apiKey` field was empty: the keys live in the macOS Keychain, not the JSON, so editing the file never touches them.

## Adding the models

My example was a batch of Ollama Cloud models, duplicating the existing `minimax-m3:cloud` entry for each of these:

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

Most Ollama Cloud models use a plain `:cloud` suffix, so I appended it to every name. Two failed: `gemma4` and `gpt-oss` returned "not found". Copilot passes `name` straight through to the provider, so each one has to match a model that provider actually serves.

## Verifying the model names

Whatever the provider, verify the names before trusting them: a typo fails quietly in the config and loudly at request time. For Ollama, `ollama show` prints a model's details and errors on an unknown tag:

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
5. Confirm each model name with the provider (`ollama show`, the provider's model list, and so on).
6. Restart Obsidian so the plugin reloads the file.
