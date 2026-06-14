Title: Bulk-add Obsidian Copilot models in data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, ollama cloud, ai configuration, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: Bulk-add Obsidian Copilot models by editing data.json and checking model tags.

Adding one model through Copilot's settings is fine. Adding a batch is tedious.

Copilot stores the model list here:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

The workflow: close Obsidian, back up `data.json`, copy a working entry, change the model name, validate JSON, reopen Obsidian.

If you are not sure which vault Obsidian opens, check the macOS app registry:

```text
~/Library/Application Support/obsidian/obsidian.json
```

## Back up and validate

I copied `data.json` to a timestamped backup and checked both versions with `jq empty`:

```bash
cp ".obsidian/plugins/copilot/data.json" \
  ".obsidian/plugins/copilot/data.json.backup.$(date +%Y%m%d-%H%M%S)"

jq empty ".obsidian/plugins/copilot/data.json"
```

## Edit activeModels

Chat models live in `activeModels`. I duplicated an existing Ollama entry and changed `name` to the new model tag.

## Verify the tags

For Ollama, check a tag with:

```bash
ollama show "<model-name>"
```

I first guessed that every Ollama Cloud model used a plain `:cloud` suffix. Most did. Two needed explicit sizes: `gemma4:31b-cloud` and `gpt-oss:20b-cloud`.

## Reopen Obsidian

After reopening Obsidian, the new models appeared in Copilot's picker and answered a test prompt.
