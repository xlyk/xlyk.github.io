Title: Bulk-add Obsidian Copilot models in data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, ollama cloud, ai configuration, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: How to bulk-add Obsidian Copilot models by editing data.json and verifying model tags before using them.

Obsidian Copilot lets you add models through its settings screen. That works fine for one or two models. It gets tedious when you want to add a batch.

Copilot stores the model list in your vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

You can edit that file directly: quit Obsidian, back up the file, duplicate a working entry, verify the model tags, validate the JSON, then reopen Obsidian and test one model.

I used this to add several Ollama Cloud models. The same pattern can work for other providers, but start from a model that already works in Copilot.

## Find the right file

If you know your vault path, go straight to:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

If you are not sure which vault Obsidian opens, check Obsidian's app registry on macOS:

```text
~/Library/Application Support/obsidian/obsidian.json
```

I had two similarly named vaults. The registry made it clear which one I needed.

## Back up before editing

Quit Obsidian first. Then, from the vault root:

```bash
cp ".obsidian/plugins/copilot/data.json" \
  ".obsidian/plugins/copilot/data.json.backup.$(date +%Y%m%d-%H%M%S)"
```

Check that the file parses:

```bash
jq empty ".obsidian/plugins/copilot/data.json"
```

Run the same check after editing.

## Edit the model list

The important model fields live here:

```json
{
  "activeModels": [],
  "activeEmbeddingModels": [],
  "defaultModelKey": "...",
  "embeddingModelKey": "..."
}
```

Chat models go in `activeModels`. Embedding models go in `activeEmbeddingModels`. If you want to change the default model, use `<model>|<provider>` for `defaultModelKey`.

## Duplicate a working entry

I copied an existing working Ollama entry:

```json
{
  "name": "minimax-m3:cloud",
  "provider": "ollama",
  "enabled": true,
  "isBuiltIn": false,
  "baseUrl": "",
  "apiKey": "",
  "isEmbeddingModel": false,
  "capabilities": ["reasoning", "vision", "websearch"],
  "stream": true,
  "reasoningEffort": "high",
  "numCtx": 131072
}
```

The `name` must match a model tag Ollama recognizes.

## Verify the model tags

Most failures come from plausible-looking model names that are not exact tags.

For Ollama, check a tag with:

```bash
ollama show "<model-name>"
```

I first guessed that every Ollama Cloud model used a plain `:cloud` suffix. Most did. Two did not.

Wrong:

```text
gemma4:cloud
gpt-oss:cloud
```

Correct:

```text
gemma4:31b-cloud
gpt-oss:20b-cloud
```

Here is the set I used:

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

## Reopen and test

Reopen Obsidian and check Copilot. The new models should appear in the model picker. Select one and send a small test prompt:

```text
Reply with exactly: ok
```

If the model appears but fails, check the tag first:

```bash
ollama show "<model-name>"
```
