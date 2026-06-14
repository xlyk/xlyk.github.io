Title: Bulk-add Obsidian Copilot models in data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, ollama cloud, ai configuration, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: How to bulk-add Obsidian Copilot models by editing data.json without losing changes or trusting bad model tags.

Obsidian Copilot lets you add models through its settings screen. That works fine for one or two models. It gets tedious when you want to add a batch.

Copilot stores the model list in your vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

You can edit that file directly. Do it carefully: quit Obsidian, back up the file, duplicate a working entry, verify the model tags, validate the JSON, then reopen Obsidian and test one model.

I used this to add several Ollama Cloud models. The same pattern can work for other providers, but do not invent provider entries from scratch. Start from a model that already works in Copilot.

One caveat before the steps: Ollama Cloud is not local inference. It uses Ollama's tooling, but the model runs in the cloud. If you want fully local/private AI, use local Ollama models instead of `:cloud` models.

## Use this only for bulk edits

Use Copilot's settings UI if you only need one model. It is safer and faster.

Edit `data.json` when:

- you need to add or update several models;
- you already have one working model for the same provider;
- you know which vault Copilot is using;
- you can restore a JSON backup if the edit breaks.

Do not edit the file while Obsidian is open. Copilot can write its in-memory settings back to disk and wipe out your changes.

## Find the right file

If you know your vault path, go straight to:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

If you are not sure which vault Obsidian opens, check Obsidian's app registry.

macOS:

```text
~/Library/Application Support/obsidian/obsidian.json
```

Windows:

```text
%APPDATA%\Obsidian\obsidian.json
```

Linux:

```text
~/.config/obsidian/obsidian.json
```

I had two similarly named vaults. The registry made it clear which one I needed.

## Back up before editing

Quit Obsidian first. Then, from the vault root:

```bash
cp ".obsidian/plugins/copilot/data.json" \
  ".obsidian/plugins/copilot/data.json.backup.$(date +%Y%m%d-%H%M%S)"
```

Check that the current file parses:

```bash
jq empty ".obsidian/plugins/copilot/data.json"
```

If you do not have `jq`, use Python:

```bash
python -m json.tool ".obsidian/plugins/copilot/data.json" >/dev/null
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

Chat models go in `activeModels`. Embedding models go in `activeEmbeddingModels`.

Defaults use this format:

```text
<model>|<provider>
```

Example:

```text
minimax-m3:cloud|ollama
```

If you only add models, leave `defaultModelKey` alone. Change it only if you want one of the new models to become the default.

## Duplicate a working entry

Do not build a new model object by hand. Create one working model through Copilot's UI, then duplicate that object in `data.json`.

This was my starting point:

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

For Ollama, the key fields are:

```json
{
  "name": "exact-model-tag",
  "provider": "ollama"
}
```

The `name` must match a model tag Ollama recognizes.

Do not blindly copy model-specific fields like `capabilities`, `numCtx`, `stream`, or `reasoningEffort`. They may be wrong for another model. Copy the shape from a working entry, then change as little as possible.

Also check your API key fields. In my config, `_keychainOnly` was `true`, and the `apiKey` fields were empty. That means my keys lived outside `data.json`. Do not assume your setup is the same. Never share or commit this file without checking for secrets.

## Verify the model tags

Most failures come from plausible-looking model names that are not exact tags.

For Ollama, check a tag with:

```bash
ollama show "<model-name>"
```

You can also run it directly:

```bash
ollama run "<model-name>"
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

Treat that list as a snapshot. Cloud catalogs change. Verify the tags before using them.

## Reopen and test

After editing, validate the file again:

```bash
jq empty ".obsidian/plugins/copilot/data.json"
```

Then reopen Obsidian and check Copilot.

Confirm that:

- Copilot settings still load;
- the new models appear in the model picker;
- the old default model still works;
- one new model answers a small test prompt.

Use a boring prompt:

```text
Reply with exactly: ok
```

If the model appears but fails, check the tag first:

```bash
ollama show "<model-name>"
```

If your changes disappeared, Obsidian probably overwrote the file. Quit Obsidian, restore the backup, and repeat the edit while the app stays closed.

## The pattern

The useful workflow is simple:

```text
1. Make one provider entry work in the UI.
2. Quit Obsidian.
3. Back up data.json.
4. Duplicate the working entry.
5. Change one model tag.
6. Validate JSON.
7. Reopen Obsidian and test.
8. Repeat once the shape is confirmed.
```

That gives you the speed of bulk editing without pretending Copilot's config file is safer or more stable than it is.
