# Quest Platform Workflow Example

This example explains how a community quest platform can use the GenLayer Community Quest Moderator.

## Scenario

A platform runs a quest:

"Create a public post explaining how GenLayer can be used for community quest moderation."

The platform wants a transparent review process before granting XP, badges, or leaderboard points.

## Step 1: Participant creates evidence

The participant creates a public evidence file.

Example evidence URL:

https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/main/evidence/sample-community-post.md

## Step 2: Platform calls the contract

The platform calls:

review_submission(
  quest_name="GenLayer Community Special Quest",
  evidence_url="https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/main/evidence/sample-community-post.md"
)

## Step 3: Contract reviews the evidence

The contract:

1. Normalizes the evidence URL.
2. Derives the source identity from the GitHub raw URL.
3. Fetches the evidence content.
4. Uses an LLM-backed review process.
5. Validators fetch and review the same evidence again.
6. Stable fields are compared.
7. Status and reward points are derived deterministically.
8. The final result is stored as a durable record.

## Step 4: Platform reads the result

The platform calls:

get_submission(1)

The result includes:

- source_identity
- status
- score
- reward_points
- moderation
- reason

## Step 5: Platform applies product logic

The platform can use the result like this:

- If status is approved: grant XP, badge, or leaderboard points.
- If status is needs_revision: ask the user to improve the submission.
- If status is rejected: reject the submission.
- If moderation is spam or off_topic: flag or block the submission.
- If URL or content digest was already reviewed: prevent duplicate farming.

## Summary

This product is used as a GenLayer-powered decision layer inside a larger quest platform.

It does not replace the entire app. It gives the app a verified decision that can be used for rewards, badges, moderation, and leaderboard updates.
