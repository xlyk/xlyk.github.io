Title: Configuring Obsidian Copilot the Easy Way: Editing data.json to Add Ollama Cloud Models
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, local ai, debugging
Slug: configuring-obsidian-copilot-the-easy-way
Summary: Batch-adding Ollama cloud models to the Obsidian Copilot plugin by hand-editing its data.json. The hard part isn't the JSON; it's finding which config file is live and verifying every model tag against Ollama instead of guessing.

Editing a plugin's config file by hand beats clicking through its settings GUI for a bulk change, but the editing was never the hard part. I wanted to add eleven Ollama cloud models to the Obsidian Copilot plugin. Two things did the real work: finding which config file was live, and verifying every model tag against Ollama rather than guessing. Editing the JSON took thirty seconds.

## Find the file that's actually live

The trap isn't syntax; it's editing the wrong file. Obsidian splits its state in two: app-level data in the platform support directory, and vault-level settings inside each vault's `.obsidian/`. The app registry tells you which vault is open:

```text
~/Library/Application Support/obsidian/obsidian.json
```

That mattered because I had two similarly named vault directories, and only one was open. The registry settled it. From there, the plugin config sits at a predictable path inside the active vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

In the same `.obsidian/` directory, `community-plugins.json` listed `copilot`, confirming the plugin ID and its folder; `manifest.json` gave the version. Everything pointed at one file.

## What's in the config, and what isn't

`data.json` holds the settings the GUI writes. The fields that matter:

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

The GUI's chat-model table maps to `activeModels`. Each entry looks like this:

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

One detail made the edit safer: `_keychainOnly` was `true`, and every `apiKey` field was empty. Model lists and behavior live in the JSON; secrets live in the macOS Keychain. That split is correct: you can edit the file without spilling API keys into a text editor.

## The trap: guessing model tags

The plan was to duplicate the existing `minimax-m3:cloud` entry for each model in this list:

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

Most Ollama cloud models take a plain `:cloud` suffix, so I assumed all of them did, appended it to every name, and reloaded. Two requests failed: `gemma4` and `gpt-oss` were not found.

That failure is the whole point. Copilot passes the configured model name straight through to Ollama. A name that's even slightly off sits quietly in the config and fails loudly at request time.

## The fix: ask Ollama, don't guess harder

The source of truth for an Ollama tag is Ollama:

```bash
ollama show "<model-name>"
```

Running it against the two failures returned the real tags:

```text
gemma4:31b-cloud
gpt-oss:20b-cloud
```

With those two patched, the full set resolved cleanly:

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

A final `ollama show` pass confirmed every configured model.

## The loop that made it safe

Editing live plugin config has one real hazard: the app can overwrite your changes. If Obsidian is open while you edit, its in-memory settings may be stale, and it can write them back over your file on shutdown. A backup makes the edit reversible. The full workflow:

1. Locate the active vault through Obsidian's app registry.
2. Find the config at `.obsidian/plugins/copilot/data.json`.
3. Make a timestamped backup before touching anything.
4. Edit only the `activeModels` array.
5. Validate the syntax with `jq`.
6. Verify the model tags with `ollama show`.
7. Reload Obsidian so the plugin reads the new file.

## What carries over

The JSON was easy; knowing which JSON was live was the hard part. That pattern holds for most plugin config, not just Copilot's. The specifics worth keeping:

- The chat-model table is `activeModels`; embeddings live in `activeEmbeddingModels`.
- `defaultModelKey` uses a `<model>|<provider>` format.
- With Keychain-only mode on, API keys stay in the Keychain, never the JSON.
- Ollama model names must be exact tags, never the GUI's display names.

The GUI still earns its place for discovery. Once you know the structure, batch edits in the file are faster and harder to get wrong, provided you verify afterward. Here, `jq` verified the file, and `ollama show` verified the names. Trust neither the GUI nor your memory; trust the tool that owns the answer.
