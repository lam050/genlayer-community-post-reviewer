# genlayer-community-post-reviewer
A GenLayer Intelligent Contract demo using an LLM-backed workflow to review community posts.
## LLM-backed Community Post Reviewer

In addition to the basic Hello contract, this repository includes a more substantive GenLayer Intelligent Contract called `CommunityPostReviewer`.

This contract demonstrates a meaningful LLM-backed decision workflow:

1. A user submits a community post.
2. The contract asks an LLM to evaluate whether the post is a valid GenLayer community contribution.
3. Validators verify the result against explicit criteria.
4. The accepted decision is stored in contract state.
5. The result can be read through `get_decision`.

This demonstrates how GenLayer can be used for community task review, AI-assisted adjudication, campaign validation, and subjective content evaluation.
