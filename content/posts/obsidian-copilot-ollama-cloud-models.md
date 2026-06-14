Title: Bulk-add models to Obsidian Copilot by editing data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, ollama cloud, ai configuration, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: A safe workflow for bulk-adding Obsidian Copilot models by editing data.json directly: quit Obsidian, back up the config, duplicate a working provider entry, verify model tags, and test the result.

Obsidian Copilot's settings UI is fine for adding one or two models. If you want to add a batch of models, the repeated clicking gets old fast.

Copilot stores its model list in a JSON file inside your vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

You can edit that file directly, but treat it like a small config migration: quit Obsidian first, back up the file, duplicate a known-working entry, verify the model tags, validate the JSON, then reopen Obsidian and test the result.

This post uses Ollama Cloud models as the example, but the safer lesson is more general: when you already have one working provider entry, you can often duplicate it and change only the model-specific fields.

## When to use this

Use the Copilot settings UI if you only need to add one model. It is safer and easier.

Edit `data.json` directly when:

- you want to add or update several models at once;
- you already have at least one working model for the same provider;
- you are comfortable restoring a JSON backup if something breaks;
- you can quit Obsidian while editing the file.

Do not use this method if Obsidian Sync or another sync tool is actively modifying the vault, if you are not sure which vault you are editing, or if you are not comfortable recovering from a bad JSON edit.

One more caveat: Ollama Cloud models use Ollama's tooling/API, but they are not local inference. If your goal is fully local/private AI, use local Ollama models instead of `:cloud` models.

## The safe workflow

The order matters.

1. Quit Obsidian completely.
2. Find the vault you want to edit.
3. Back up Copilot's `data.json`.
4. Duplicate a working model entry for the same provider.
5. Change only the fields you need.
6. Validate the JSON.
7. Reopen Obsidian.
8. Confirm the models appear in Copilot.
9. Send a small test prompt to at least one new model.

If you edit while Obsidian is open, Copilot can rewrite the file from memory and discard your changes when the app exits or reloads.

## Find the right vault

If you already know the vault path, skip this section.

Obsidian keeps app-level state separately from per-vault settings. On macOS, the app registry lives here:

```text
~/Library/Application Support/obsidian/obsidian.json
```

Other common locations:

```text
Windows: %APPDATA%\Obsidian\obsidian.json
Linux:   ~/.config/obsidian/obsidian.json
```

That registry can help when you have multiple similarly named vaults. In my case, I had two near-duplicates and wanted the one Obsidian was actually opening.

Once you have the vault path, Copilot's config is inside the vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

If your plugin folder has a slightly different name, check:

```text
<vault>/.obsidian/plugins/
```

and look for the Copilot plugin directory.

## Back up data.json

From the vault root:

```bash
cp ".obsidian/plugins/copilot/data.json" \
   ".obsidian/plugins/copilot/data.json.backup.$(date +%Y%m%d-%H%M%S)"
```

Then make sure the current file is valid JSON before editing:

```bash
jq empty ".obsidian/plugins/copilot/data.json"
```

If you do not have `jq`, Python works too:

```bash
python -m json.tool ".obsidian/plugins/copilot/data.json" >/dev/null
```

Do this before and after the edit. It only checks JSON syntax, not whether Copilot likes the settings, but it catches the easy mistakes.

## The fields that matter

Copilot's `data.json` contains more than model settings. The model-related fields I cared about were:

```json
{
  "activeModels": [],
  "activeEmbeddingModels": [],
  "defaultModelKey": "...",
  "embeddingModelKey": "..."
}
```

Chat models go in `activeModels`. Embedding models go in `activeEmbeddingModels`.

Defaults use this shape:

```text
<model>|<provider>
```

For example:

```text
minimax-m3:cloud|ollama
```

If you only add models, you may not need to touch `defaultModelKey`. If you want one of the new models to be the default, update it after the new model entry exists.

## Duplicate a working provider entry

The safest way to add models is not to invent a new object from scratch. First create one working model through Copilot's settings UI, then duplicate that entry in `data.json`.

Here is the kind of entry I started from:

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

In my config, `_keychainOnly` was `true` and the `apiKey` fields were empty, so the API keys lived outside this JSON file. Do not assume that is true for your setup. Check your own `apiKey` fields before backing up, syncing, sharing, or committing this file.

Also do not blindly copy every model-specific field. Fields like `capabilities`, `reasoningEffort`, `stream`, and `numCtx` may be wrong for another model. Start with the smallest change that works: duplicate a known-good entry for the same provider and change the model name first.

For an Ollama model, the two fields that must line up are:

```json
{
  "name": "exact-model-tag",
  "provider": "ollama"
}
```

The model name is passed through to Ollama. If the tag is wrong, Copilot may still load the config, but the request will fail when you try to use the model.

## Verify model names before trusting them

Most failures come from model tags that look plausible but are not the exact IDs the provider expects.

For Ollama, check the tag before relying on it:

```bash
ollama show "<model-name>"
```

You can also test with:

```bash
ollama run "<model-name>"
```

My first pass used a plain `:cloud` suffix for every Ollama Cloud model. Most worked. Two did not.

Wrong guesses:

```text
gemma4:cloud
gpt-oss:cloud
```

Correct tags from my test:

```text
gemma4:31b-cloud
gpt-oss:20b-cloud
```

The corrected set I used:

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

Treat that list as a snapshot, not a canonical catalog. Cloud model availability and naming can change. Verify current tags with Ollama before assuming they still work.

## Validate before reopening Obsidian

After editing:

```bash
jq empty ".obsidian/plugins/copilot/data.json"
```

or:

```bash
python -m json.tool ".obsidian/plugins/copilot/data.json" >/dev/null
```

Then check the basics:

```text
- Obsidian is still closed.
- data.json has a timestamped backup.
- JSON validation passes.
- Every new model has the right provider.
- Every model tag was verified with the provider.
- defaultModelKey, if changed, uses <model>|<provider>.
- You did not accidentally paste secrets into the file.
```

JSON validation does not prove the model will work. It only proves the file can be parsed.

## Reopen Obsidian and test

Start Obsidian again, then open Copilot settings.

Check:

```text
- The Copilot settings page loads.
- The new models appear in the model picker.
- The old default model still works.
- One new model answers a tiny prompt.
```

Use a boring test prompt:

```text
Reply with exactly: ok
```

If that works, the model tag and provider route are probably correct.

## Troubleshooting

### My changes disappeared

Obsidian or Copilot probably overwrote the file from memory.

Fix:

1. Quit Obsidian completely.
2. Restore from the backup if needed.
3. Reapply the edit.
4. Validate JSON.
5. Reopen Obsidian.

### Copilot settings broke

The JSON may be invalid.

Run:

```bash
python -m json.tool ".obsidian/plugins/copilot/data.json"
```

If the error is not obvious, restore the backup and make a smaller edit.

### The model appears but fails when selected

The model tag is probably wrong, unavailable, or not accessible through your current Ollama setup.

Check:

```bash
ollama show "<model-name>"
```

Then compare the new entry against a model that already works in Copilot.

### The default model fails

Check `defaultModelKey`.

It should look like:

```text
<model>|<provider>
```

For example:

```text
deepseek-v4-pro:cloud|ollama
```

The model name in `defaultModelKey` has to match the `name` field of an active model entry.

### I expected this to be local/private

Local Ollama models run on your machine. Ollama Cloud models are accessed through Ollama but run in the cloud. If privacy is the reason you use Ollama, use local model tags instead of `:cloud` tags.

## What I would do differently next time

I would still use direct editing for a batch change, but I would not treat the copied entry as universally correct. The durable pattern is:

```text
1. Make one model work through the UI.
2. Quit Obsidian.
3. Back up data.json.
4. Duplicate the known-good entry.
5. Change one model tag.
6. Validate and test.
7. Repeat or generate the rest once the shape is confirmed.
```

That keeps the speed benefit without pretending the config schema is more stable than it is.
