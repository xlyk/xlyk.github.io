Title: Bulk-add Obsidian Copilot models with data.json
Date: 2026-06-13 01:29
Category: AI Engineering
Tags: obsidian, copilot, ollama, ollama cloud, ai configuration, debugging
Slug: obsidian-copilot-ollama-cloud-models
Summary: Add a batch of Obsidian Copilot models by editing data.json and checking the model tags.

Adding one model in Copilot's settings is fine. Adding a dozen is tedious.

Copilot stores model config in the vault:

```text
<vault>/.obsidian/plugins/copilot/data.json
```

If you have similarly named vaults, Obsidian's macOS registry shows which one it opens:

```text
~/Library/Application Support/obsidian/obsidian.json
```

## Edit data.json

I closed Obsidian, copied `data.json`, and checked the file with `jq`:

```bash
cp ".obsidian/plugins/copilot/data.json" \
  ".obsidian/plugins/copilot/data.json.backup.$(date +%Y%m%d-%H%M%S)"

jq empty ".obsidian/plugins/copilot/data.json"
```

Then I duplicated an existing Ollama entry in `activeModels` and changed `name` to the new model tag. That was the only field I needed to change.

## Check model tags

Copilot passes `name` straight through to Ollama, so the tag has to be exact:

```bash
ollama show "<model-name>"
```

I first guessed that every Ollama Cloud model used a plain `:cloud` suffix. Most did. Two needed explicit sizes: `gemma4:31b-cloud` and `gpt-oss:20b-cloud`.

After reopening Obsidian, the new models appeared in Copilot's picker and answered a test prompt.
