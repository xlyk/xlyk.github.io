Title: Fixing RTK History in the Codex Sandbox
Date: 2026-07-22 23:15
Category: AI Engineering
Tags: codex, rtk, sqlite, sandboxing, developer tooling
Slug: fixing-rtk-history-codex-sandbox
Summary: RTK commands worked in Codex while its SQLite history stayed empty. The fix was a writable root for RTK's global database.

I had [RTK](https://github.com/rtk-ai/rtk) enabled in [Codex](https://github.com/openai/codex). `rtk ls -las` worked. `rtk cat README.md` worked. Then `rtk gain -H` showed one old command and none of the calls I had run.

The commands and the history report disagreed because RTK has two jobs. It filters command output, then records token savings in a SQLite database. The first job worked inside the Codex sandbox. The second needed write access outside the repository.

## The error that gave it away

RTK stores its global history on macOS at:

```text
~/Library/Application Support/rtk/history.db
```

Codex ran commands in a managed workspace that could write to the repository and temporary directories. The RTK directory sat outside those writable roots.

Most RTK commands still returned filtered output when the history write failed. `rtk gain -H` opened the database itself and exposed the error:

```text
rtk: Failed to initialize tracking database: unable to open database file:
Error code 14: Unable to open the database file
```

Supported commands such as `rtk ls` were missing from history too, so command eligibility was not the cause.

## Proving the database path was the problem

I pointed RTK at an isolated database under `/private/tmp` and used the same path for a command and its report:

```bash
RTK_DB_PATH=/private/tmp/rtk-codex-history.db rtk ls -la .
RTK_DB_PATH=/private/tmp/rtk-codex-history.db rtk gain -H
```

The report recorded the command with 235 tokens saved, a 72.8% reduction. That test separated the sandbox problem from RTK's filtering and tracking logic.

The temporary database proved the cause but made a poor permanent home. `/private/tmp` is disposable. A database under the repository would split history by project. Moving the file to `~/.rtk` would still leave it outside the Codex sandbox.

## Keeping one global history

RTK already had the right global location. Codex needed permission to write there.

I added the containing directory to the existing `writable_roots` list in `~/.codex/config.toml`:

```toml
[sandbox_workspace_write]
network_access = true
writable_roots = [
  "/Users/you/Library/Application Support/rtk",
]
```

If the list contains other writable roots, keep them and append the RTK directory.

Grant the directory rather than `history.db` alone. SQLite may create journal and sidecar files beside the database, so access to one file does not cover every write.

Codex reads its writable roots when a task starts. I opened a fresh task after changing the config, ran:

```bash
rtk ls -la .
rtk gain -H
```

The global report opened without error. The `ls` command appeared at the top of the recent history with a 70% token reduction.

[RTK issue #842](https://github.com/rtk-ai/rtk/issues/842) reports the same Codex restriction on the default database path. Redirecting the database works as a diagnostic or short-term workaround. Granting RTK's existing directory keeps one history across repositories.

Successful proxy output had hidden the failed history write. I now use `rtk gain -H` to check both RTK's savings and its access to the tracking database.
