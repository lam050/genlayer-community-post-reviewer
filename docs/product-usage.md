# Product Usage

## What is this product?

GenLayer Community Quest Moderator is a verification layer for community quest platforms.

It helps a platform review user-submitted evidence before giving rewards, XP, badges, leaderboard points, or moderation results.

This product is not meant to be randomly attached to any app. It is used at the exact point where a platform needs to decide whether a submission should be approved, rejected, or revised.

## Who uses it?

There are three main users:

1. Quest organizers  
They create campaigns and define what counts as a valid submission.

2. Participants  
They submit public evidence for a quest, such as a GitHub evidence file, article, tutorial, or social post.

3. Quest platforms or dashboards  
They call the GenLayer contract, read the decision, and update their own reward, badge, or leaderboard system.

## How does the workflow work?

The intended workflow is:

1. A quest platform creates a campaign.
2. A participant submits a public evidence URL.
3. The platform calls the GenLayer contract.
4. The contract fetches and reviews the evidence.
5. Validators independently reassess the same evidence.
6. The contract stores a structured decision.
7. The platform reads the result.
8. The platform applies product logic such as approval, rejection, revision request, XP, badge, or leaderboard update.

## Contract input

The contract takes:

- quest_name
- evidence_url

The contract does not trust a user-provided author name. It derives a source identity from the raw GitHub evidence URL.

Example:

https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/main/evidence/sample-community-post.md

becomes:

github:lam050/genlayer-community-post-reviewer

## Contract output

Each reviewed submission creates a record with:

- submission_id
- source_identity
- quest_name
- canonical_url
- content_digest
- status
- score
- reward_points
- moderation
- reason

## How a platform uses the result

A frontend or backend can use the contract result like this:

- approved: mark the quest as completed and grant XP or badge eligibility
- needs_revision: ask the user to improve the submission
- rejected: reject the submission and show the reason
- spam or off_topic: flag the submission
- duplicate URL or content digest: prevent repeated reward farming

## Example use cases

This project can be used for:

- community quest review
- campaign proof verification
- ambassador task moderation
- tutorial or article quality checks
- hackathon submission screening
- leaderboard point validation
- duplicate submission prevention

## What this product is not

This contract is not a full quest platform by itself.

An integrating platform still needs:

- a user interface
- user accounts
- campaign rules
- reward logic
- badge or leaderboard system
- a backend or frontend that reads the contract decision

The contract provides the GenLayer-based decision layer.
