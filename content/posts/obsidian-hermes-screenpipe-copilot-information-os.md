Title: An Information Operating System: Obsidian, Hermes, Screenpipe, and Obsidian Copilot
Date: 2026-06-14 00:00
Category: AI Engineering
Tags: obsidian, hermes, screenpipe, copilot, ai agents, information systems, automation
Slug: obsidian-hermes-screenpipe-copilot-information-os
Summary: How Obsidian, Hermes, Screenpipe, and the Obsidian Copilot plugin run as one system.

# An Information Operating System

*How Obsidian, Hermes, Screenpipe, and the Obsidian Copilot plugin run as one system.*

Most people call a setup like this a "second brain." That label misses what matters. Here, Obsidian is not a second brain but a filesystem with an operating contract: notes have addresses, and agents have rules they can follow safely.

That is the whole shape. Notes need addresses, agents need rules, background work needs a scheduler, captured activity needs a destination, and the tools that query and edit it all need a shared substrate.

This is not a setup guide. It describes how five pieces fit together: Obsidian, Hermes, the Hermes scheduler, Screenpipe, and the Obsidian Copilot plugin.

## The contract

Obsidian stores the files, and the folder layout gives every note a home: inbox, projects, areas, archives, maps, raw material, support.

The folders matter least. The README at the root of the vault matters most. It defines what belongs where, what is protected, what an agent may patch, and when a human must review a change first.

Without the README, the vault is just Markdown. With it, the vault has an API.

## The operator

Hermes operates the vault. It reads the README, inspects files, triages the inbox, runs checks, coordinates workers, and writes results back.

The scheduler belongs to Hermes — not Unix cron, but a native layer that runs agent workflows, plain scripts, skill-backed processes, and watchdogs. Here the system stops being manual. Inbox triage, health reports, Screenpipe summaries, Kanban loops, watchdogs, reminders, and review checks all run without anyone opening a chat to ask.

## The capture layer

Screenpipe captures local activity: screenshots, transcripts, OCR, audio, private logs. None of it leaves the machine, and that boundary is the point.

Work leaves traces. Screenpipe turns those traces into summaries or candidates and writes them directly into the vault, under the same README contract Hermes follows. You take fewer notes by hand. You still review what lands.

## The interface

"Obsidian Copilot" means the Obsidian plugin, not GitHub Copilot.

Hermes and Copilot work the same files from opposite sides. Hermes works from outside the vault and does things: edits, checks, scheduled tasks, worker coordination. Copilot works inside Obsidian and answers questions while you read or write. Same files, different interface.

## The loop

The cycle is simple:

1. Work happens.
2. Screenpipe captures the local signal.
3. A pipe or scheduled task extracts something small.
4. Hermes applies the vault rules.
5. Obsidian stores the result.
6. Later, Hermes or Copilot queries or edits it.

This is why "information operating system" fits better than "agent memory." Memory is one behavior. The system is the coordination around it: filesystem, contract, scheduler, capture, interface, feedback.

## The failure modes

It is still rough, and it breaks in predictable ways. Rules drift. Summaries need review. Background jobs fail silently. Screenpipe demands a hard privacy boundary. Vague contracts make agents write junk. Scheduled tasks decay into automation theater once they stop producing anything useful.

So the boring parts carry the weight: logs, dated reports, protected zones, watchdogs, non-destructive checks.

The system is not an autonomous vault. It is an operable one.
