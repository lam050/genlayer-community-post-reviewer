# SDK Integration Example

This document explains how a real quest platform can use the GenLayer Community Quest Moderator V5 contract.

## Purpose

The project is a headless GenLayer decision layer.

It does not need to be a standalone frontend app. Instead, another app, backend, or quest platform can call the contract and consume the result.

The goal of this SDK example is to show the full integration flow:

1. A quest platform receives a public evidence URL from a participant.
2. The platform calls `review_submission(quest_name, evidence_url)`.
3. The platform waits for successful finalization.
4. The platform reads the resulting record with `get_submission(submission_id)`.
5. The platform uses the result to update XP, badges, moderation state, or leaderboard state.

## Example file

See:

```text
examples/sdk-review-submission.ts
```

## What the SDK example does

The SDK example shows how a real app can:

1. Create a GenLayer client.
2. Prepare a quest name and commit-pinned evidence URL.
3. Call `review_submission`.
4. Wait for the transaction to finalize.
5. Check that the transaction succeeded.
6. Read `get_submission(1)`.
7. Print the structured decision record.

## Contract method used

The write method is:

```text
review_submission(quest_name, evidence_url)
```

Example input:

```text
quest_name:
GenLayer Community Special Quest
```

```text
evidence_url:
https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/922b5f642dc6da34b058cb94f1e13acc229c760d/evidence/sample-community-post.md
```

## Read method used

After the transaction is finalized, the app reads:

```text
get_submission(1)
```

The returned record includes fields such as:

- `source_identity`
- `quest_name`
- `canonical_url`
- `commit_hash`
- `content_digest_sha256`
- `status`
- `score`
- `reward_points`
- `incremental_reward`
- `moderation`
- `reason`

## How a platform uses the result

A quest platform can use the returned record like this:

| Contract result | Platform action |
|---|---|
| `status = approved` | Mark the quest as completed |
| `status = needs_revision` | Ask the participant to improve the evidence |
| `status = rejected` | Reject the submission |
| `reward_points > 0` | Add XP, badge eligibility, or leaderboard points |
| `moderation = spam` | Flag or block the submission |
| Duplicate URL or digest | Prevent repeated reward farming |

## Why this matters

This shows that the contract is not just an isolated demo.

It can be used by:

- a frontend
- a backend
- a quest platform
- a campaign dashboard
- a community moderation system
- a leaderboard system

The contract provides the GenLayer-powered decision layer. The integrating app decides how to apply the result to users, XP, badges, and leaderboards.

## Integration summary

The full flow is:

```text
participant submits evidence
→ platform calls review_submission
→ GenLayer validators review the evidence
→ contract stores the decision
→ platform calls get_submission
→ platform updates XP / badge / leaderboard / moderation state
```

## Notes

The SDK example uses a deployed contract address from GenLayer Studio.

Before running the example, replace:

```text
0xYOUR_DEPLOYED_CONTRACT_ADDRESS
```

with the real deployed address from GenLayer Studio.

The contract address can be found next to:

```text
Deployed at 0x...
```

inside GenLayer Studio.
