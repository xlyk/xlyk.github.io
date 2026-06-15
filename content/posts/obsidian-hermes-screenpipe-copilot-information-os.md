Title: An Information Operating System: Obsidian, Hermes, Screenpipe, and Obsidian Copilot
Date: 2026-06-15 10:02
Category: AI Engineering
Tags: obsidian, hermes, screenpipe, copilot, ai agents, information systems, automation
Slug: obsidian-hermes-screenpipe-copilot-information-os
Summary: A system description of using Obsidian, Hermes, Screenpipe, and Hermes scheduled tasks as an information operating system.

Obsidian is not a second brain in this system.

It is a filesystem with an operating contract that agents can safely use.

That is the core shape. Notes need addresses. Agents need rules. Background work needs a scheduler. Captured activity needs a destination. Query and editing tools need a shared substrate.

This is not a setup guide. It describes a system composed of Obsidian, Hermes, Screenpipe, Hermes scheduled tasks, and the Obsidian Copilot plugin.

## The contract

Obsidian stores the files. The folder layout gives notes a place to live: inbox, projects, areas, archives, maps, raw material, and support files.

The README at the root of the vault matters more than the folder names. It defines what belongs where, what is protected, what can be patched, and when review is required.

Without that README, the vault is just Markdown. With it, the vault has an API.

## The operator

Hermes is the operator.

It can read the README, inspect files, triage inbox material, run checks, coordinate workers, and write results back into the vault.

Hermes scheduled tasks are the scheduler. This does not mean Unix `crontab`. The scheduler is part of Hermes. It can run agent workflows, no-agent scripts, skill-backed processes, and watchdogs.

That is where the system stops being manual. Inbox triage, health reports, Screenpipe summaries, Kanban and watchdog loops, reminders, and review checks can run without a human opening a chat and asking for each step.

## The capture layer

Screenpipe captures local activity signals.

Raw screenshots, transcripts, OCR, audio, and private logs do not need to leave the machine. Raw capture stays local.

Work leaves traces. Screenpipe can turn those traces into summaries or candidates. Hermes can route those into the vault under the README rules.

The capture layer reduces dependence on manual note-taking. It does not remove the need for review.

## The interface

Obsidian Copilot means the Obsidian plugin, not GitHub Copilot.

Hermes works from outside the vault. Obsidian Copilot works from inside Obsidian. Hermes is better for actions: edits, checks, scheduled tasks, and worker coordination. Copilot is better for asking questions while reading or writing inside the vault.

Same files. Different interface.

## The loop

The loop is simple:

1. Work happens.
2. Screenpipe captures local signal.
3. A pipe or Hermes scheduled task extracts something small.
4. Hermes applies the vault rules.
5. Obsidian stores the result.
6. Hermes or Obsidian Copilot queries or edits it later.

That is why "information operating system" fits better than "agent memory." Memory is one behavior. The system is the coordination: filesystem, contract, scheduler, capture, interface, feedback.

## The failure modes

This is still rough.

Rules drift. Generated summaries need review. Background jobs can fail silently. Screenpipe needs a hard privacy boundary. Agents write junk when the contract is vague. Hermes scheduled tasks can become automation theater if they stop producing useful output.

So the boring parts matter: logs, dated reports, protected zones, watchdogs, and non-destructive checks.

The system is not an autonomous vault. It is an operable vault.
