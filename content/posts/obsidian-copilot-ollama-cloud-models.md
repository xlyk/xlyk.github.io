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

If you are not sure which vault Obsidian opens, check Obsidian's app registry on macOS:

```text
~/Library/Application Support/obsidian/obsidian.json
```

## Back up before editing

I backed up `data.json`, edited it while Obsidian was closed, then checked it with `jq`:

```bash
cp ".obsidian/plugins/copilot/data.json" \
  ".obsidian/plugins/copilot/data.json.backup.$(date +%Y%m%d-%H%M%S)"

jq empty ".obsidian/plugins/copilot/data.json"
```

Run the same `jq` check after editing.

## Edit the model list

Chat models go in `activeModels`:

```json
{
  "activeModels": []
}
```

## Duplicate a working entry

I copied an existing working Ollama entry and changed the model name:

```json
{
  "name": "minimax-m3:cloud",
  "provider": "ollama",
  "enabled": true
}
```

## Verify the model tags

For Ollama, check a tag with:

```bash
ollama show "<model-name>"
```

I first guessed that every Ollama Cloud model used a plain `:cloud` suffix. Most did. Two needed explicit sizes: `gemma4:31b-cloud` and `gpt-oss:20b-cloud`.

## Reopen and test

After reopening Obsidian, the models appeared in Copilot's picker. I tested one with a short prompt:

```text
Reply with exactly: ok
```
