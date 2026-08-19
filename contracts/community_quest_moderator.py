# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class CommunityQuestModerator(gl.Contract):
    next_submission_id: u32
    submissions: TreeMap[str, str]
    author_points: TreeMap[str, u32]

    def __init__(self):
        self.next_submission_id = u32(1)

    def _validate_decision(self, data) -> bool:
        if not isinstance(data, dict):
            return False

        status = str(data.get("status", "")).lower()
        moderation = str(data.get("moderation", "")).lower()

        try:
            score = int(data.get("score", -1))
            reward_points = int(data.get("reward_points", -1))
        except Exception:
            return False

        reason = str(data.get("reason", ""))

        if status not in ["approved", "needs_revision", "rejected"]:
            return False

        if moderation not in ["clean", "low_effort", "spam", "off_topic"]:
            return False

        if score < 0 or score > 100:
            return False

        if reward_points not in [0, 25, 50, 75, 100]:
            return False

        if len(reason) < 20 or len(reason) > 300:
            return False

        return True

    @gl.public.write
    def review_submission(
        self,
        author: str,
        quest_name: str,
        post_url: str,
        post_text: str
    ) -> u32:
        submission_id = self.next_submission_id

        def leader_fn():
            prompt = f"""
You are reviewing a GenLayer community quest submission.

Quest name:
{quest_name}

Author:
{author}

Post URL:
{post_url}

Submitted post text:
{post_text}

Evaluate whether this post should be accepted for a GenLayer community quest.

Return ONLY a JSON object with exactly these keys:
- status: one of "approved", "needs_revision", "rejected"
- score: integer from 0 to 100
- reward_points: one of 0, 25, 50, 75, 100
- moderation: one of "clean", "low_effort", "spam", "off_topic"
- reason: short explanation between 20 and 300 characters

Evaluation rules:
- approved: the post clearly explains GenLayer or Intelligent Contracts and includes at least one relevant use case.
- needs_revision: the post is related to GenLayer but too vague or missing important details.
- rejected: the post is off-topic, spammy, misleading, or only talks about token/airdrop farming.
- reward_points must reflect quality and usefulness.
- high score requires clear explanation, relevant use case, and useful community value.
"""
            return gl.nondet.exec_prompt(prompt, response_format="json")

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            leader_decision = leader_result.calldata
            return self._validate_decision(leader_decision)

        decision = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        status = str(decision["status"]).lower()
        score = int(decision["score"])
        reward_points = int(decision["reward_points"])
        moderation = str(decision["moderation"]).lower()
        reason = str(decision["reason"])

        record = (
            "submission_id=" + str(submission_id) + "\n"
            + "author=" + author + "\n"
            + "quest_name=" + quest_name + "\n"
            + "post_url=" + post_url + "\n"
            + "status=" + status + "\n"
            + "score=" + str(score) + "\n"
            + "reward_points=" + str(reward_points) + "\n"
            + "moderation=" + moderation + "\n"
            + "reason=" + reason + "\n"
            + "post_text=" + post_text
        )

        self.submissions[str(submission_id)] = record

        if status == "approved":
            current_points = self.author_points.get(author, u32(0))
            self.author_points[author] = u32(int(current_points) + reward_points)

        self.next_submission_id = u32(int(self.next_submission_id) + 1)

        return submission_id

    @gl.public.view
    def get_submission(self, submission_id: u32) -> str:
        return self.submissions.get(str(submission_id), "Submission not found")

    @gl.public.view
    def get_author_points(self, author: str) -> u32:
        return self.author_points.get(author, u32(0))

    @gl.public.view
    def get_next_submission_id(self) -> u32:
        return self.next_submission_id
