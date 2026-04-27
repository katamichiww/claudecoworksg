---
title: "The Claude Architect Exam Decoded: 5 Domains That Matter"
date: 2026-04-27
description: "Anthropic dropped a Claude Certified Architect exam. Here's the real breakdown of all 5 domains and what actually matters for passing it."
tags: ["claude code", "anthropic", "ai certification", "agents"]
draft: false
---

Anthropic just made it official: there's now a real exam that says you actually know what you're doing in Claude Code. Pass or fail. No participation trophies- and I am currently studying for the exam! 

It's called the **Claude Certified Architect**, and after going through the full 40-page exam guide myself (yes, with my own eyes, not an LLM summary), I can tell you it's not fluff. I've also talked to many sempais who have passed the exams, and here are the tips they gave. 

The following wisdom is structured around five domains that, honestly, even if you never sit the exam, will make you dangerously good at Claude Code if you master them.

So let's break down what actually matters — and where most people get it wrong.

## The 5 Domains (and Why the Weights Matter)

Here's how the exam splits the points:

- **Agent architecture** — 27%
- **Cloud Code configuration** — 20%
- **Tool and MCP integration** — 18%
- **Prompt engineering** — the rest, split with…
- **Context management and reliability**

If you only have time to study one thing, study **agent architecture**. It's the heaviest section for a reason — it's how Claude actually thinks, coordinates, and respects rules you set. Everything else builds on top of it.

The thing most people miss: this isn't a vibes-based "know your tools" exam. The scenarios are specific. They'll ask you what to do when an agent skips a function call 12% of the time in production. That's a real business problem, not a textbook one.

## The Agentic Loop Is the Engine — Learn It Cold

Every single time you run Claude Code, the SDK, or anything built on Claude, the same loop is running underneath:

1. Your code sends a request to Claude.
2. Claude responds with a `stop_reason`.
3. If it says `tool_use`, you run the tool and feed the result back.
4. If it says `end_turn`, Claude is done.

That's it. That's the whole engine.

The exam guide flags three classic anti-patterns and they're worth burning into your brain:

- **Don't read Claude's text** looking for "I'm done" or "task complete." It's unreliable and breaks constantly.
- **Don't hard-cap loops** at some arbitrary number like 10. You might cut off work that genuinely needed 11 steps.
- **Don't guess from the response text.** There's a `stop_reason` field. Use it. That's literally what it's there for.

Once you internalize this, multi-agent setups make way more sense — because now you understand what each sub-agent is actually doing in its own little loop.

## Sub-Agents Don't Talk to Each Other (Yet)

Here's a concept that trips people up: when you spawn multiple sub-agents from a main coordinator, **they don't share memory**. Sub-agent A has zero clue what sub-agent B is doing. Each one has its own context window, its own world, and the main agent stitches it all together at the end.

The newer **agent teams** feature was specifically designed to fix this — it's basically giving each agent an email inbox so they can ping each other, see who's blocked, and actually collaborate. But by default? They're working in parallel silos.

The most common mistake here isn't technical, it's managerial. The coordinator agent breaks tasks down too narrowly. Tell it "research AI in creative industries" and it might spawn three sub-agents that all only look at visual arts — completely missing music, film, writing, and games.

The fix: **give the coordinator broad goals, not narrow checklists.** Trust the sub-agents to figure out the breakdown.

I tested this in Warp with a prompt like "research the impact of AI on content creation by spawning three sub-agents in parallel — video, written, audio. Each should search the web and return a three-bullet summary." Broad assignment, narrow execution. All three came back, the main agent synthesized, done. That's the pattern.

If you want to play with these patterns hands-on without the exam pressure, the [Claude Code without coding guide](https://anchrlabs.com/claude-code-non-technical/claude-code-without-coding/) walks through this kind of orchestration in a way that doesn't assume you've been writing Python for 10 years.

## Prompts Are Suggestions. Hooks Are Laws.

This might be the single most important distinction in the entire exam guide.

A **prompt** is best-effort. You tell Claude "always verify the customer before processing a refund" and it'll listen… most of the time. But the guide gives a real production scenario where 12% of the time, the agent just skipped the verification step. From a business standpoint, that's a fireable bug — you're refunding the wrong people.

A **hook** is a script that runs automatically before or after an action, and it can flat-out block Claude from doing something unless a condition is met. Not 99%. Not 99.9%. **100%.**

Use them like this:

- **Prompts** → style, tone, formatting, anything where 90% is fine
- **Hooks** → compliance, financial actions, security, anything where one failure is catastrophic

The mistake I see all the time? People try to prompt-engineer their way out of a hook problem. They iterate on the prompt 5,000 times trying to get to 100%. It doesn't work. Some problems need code-level enforcement, full stop.

Quick tip: if you pop into your terminal and run `/hooks`, you'll see every hook available. Or use the Claude Code guide agent and ask it whether your use case actually needs a hook or just a better prompt.

## Tool Descriptions Are Where Money Leaks

Here's the silent killer: when you give Claude multiple tools with vague, overlapping descriptions, it picks the wrong one. A lot.

Imagine two tools — one "retrieves customer information," another "retrieves order details." Sounds clear to you. To Claude? Ambiguous. It'll guess. Sometimes wrong. Sometimes three times wrong before it lands on the right one.

And here's the catch: **you often don't see the failures.** You see the final correct output and assume it worked clean. But under the hood, it burned through your tokens trying tool A, then B, then back to A. Your bill shows up at the end of the month and you wonder where the money went.

Token efficiency isn't just about prompts being shorter. It's about tools picking right the **first** time. Write tool descriptions like you're onboarding a new hire — assume zero context, be obnoxiously specific about when to use this tool versus that one.

This is the kind of detail that separates people who use Claude from people who [actually run it as a business tool](https://anchrlabs.com/claude-code-non-technical/claude-code-for-business-owners/).

## What to Do Next

If you're going for the cert, start with **agent architecture**. It's 27% of the exam and the foundation for everything else. If you're not going for the cert but want to get sharper, pick the one domain you're weakest in and spend a weekend on it.

And if you're brand new to Claude Code and this whole loop-and-hooks thing sounds like another language — start with the [Claude Code setup for beginners guide](https://anchrlabs.com/claude-code-non-technical/claude-code-setup-beginners/) before touching the exam material. Trying to study certification content with no foundation is how people burn out in week one.

The exam isn't the goal. **Becoming someone who actually ships with this stuff is.** The cert is just proof and the bonus...and please send me a message if you are interested in forming a Claude Architect Exam Study Group together! :)
