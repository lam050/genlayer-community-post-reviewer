# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class CommunityQuestModerator(gl.Contract):
    next_submission_id: u32
    submissions: TreeMap[str, str]
    author_points: TreeMap[str, u32]
    reviewed_evidence: TreeMap[str, str]
    author_quest_claims: TreeMap[str, str]

    def __init__(self):
        self.next_submission_id = u32(1)

    def _derive_status(self, score: int, moderation: str) -> str:
        moderation = str(moderation).lower()

        if moderation in ["spam", "off_topic"]:
            return "rejected"

        if moderation == "low_effort":
            return "needs_revision"

        if score >= 75:
            return "approved"

        if score >= 50:
            return "needs_revision"

        return "rejected"

    def _derive_reward_points(self, status: str, score: int, moderation: str) -> u32:
        status = str(status).lower()
        moderation = str(moderation).lower()

        if status != "approved":
            return u32(0)

        if moderation != "clean":
            return u32(0)

        if score >= 90:
            return u32(100)

        if score >= 80:
            return u32(75)

        return u32(50)

    def _validate_llm_decision(self, data) -> bool:
        if not isinstance(data, dict):
            return False

        moderation = str(data.get("moderation", "")).lower()
        reason = str(data.get("reason", ""))

        try:
            score = int(data.get("score", -1))
        except Exception:
            return False

        if moderation not in ["clean", "low_effort", "spam", "off_topic"]:
            return False

        if score < 0 or score > 100:
            return False

        if len(reason) < 20 or len(reason) > 300:
            return False

        return True

    def _normalize_evidence_key(self, evidence_url: str) -> str:
        return evidence_url.strip().lower()

    def _author_quest_key(self, author: str, quest_name: str) -> str:
        return author.strip().lower() + "|" + quest_name.strip().lower()

    @gl.public.write
    def review_submission(
        self,
        author: str,
        quest_name: str,
        evidence_url: str
    ) -> u32:
        evidence_key = self._normalize_evidence_key(evidence_url)
        author_key = self._author_quest_key(author, quest_name)

        if self.reviewed_evidence.get(evidence_key, "") == "reviewed":
            raise gl.UserError("This evidence URL has already been reviewed.")

        if self.author_quest_claims.get(author_key, "") == "claimed":
            raise gl.UserError("This author has already claimed this quest.")

        submission_id = self.next_submission_id

        def leader_fn():
            response = gl.nondet.web.get(evidence_url)
            evidence_text = response.body.decode("utf-8")

            if len(evidence_text) < 80:
                raise gl.UserError("Evidence content is too short.")

            if author.lower() not in evidence_text.lower():
                raise gl.UserError("Evidence does not include the submitted author.")

            if quest_name.lower() not in evidence_text.lower():
                raise gl.UserError("Evidence does not include the submitted quest name.")

            prompt = f"""
You are reviewing a GenLayer community quest submission.

The evidence below was fetched from a public evidence URL by the contract.

Author:
{author}

Quest name:
{quest_name}

Evidence URL:
{evidence_url}

Fetched evidence content:
{evidence_text}

Evaluate the quality of this submission.

Return ONLY a JSON object with exactly these keys:
- score: integer from 0 to 100
- moderation: one of "clean", "low_effort", "spam", "off_topic"
- reason: short explanation between 20 and 300 characters

Evaluation rules:
- High score requires a clear explanation of GenLayer or Intelligent Contracts.
- High score requires at least one relevant use case such as AI agents, dispute resolution, prediction markets, decentralized verification, or community moderation.
- "clean" means useful and relevant.
- "low_effort" means related but too vague or incomplete.
- "spam" means promotional spam, airdrop farming spam, or meaningless content.
- "off_topic" means not about GenLayer or relevant use cases.
"""
            decision = gl.nondet.exec_prompt(prompt, response_format="json")

            if not isinstance(decision, dict):
                raise gl.UserError("LLM did not return a JSON object.")

            return decision

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            leader_decision = leader_result.calldata

            if not self._validate_llm_decision(leader_decision):
                return False

            validator_decision = leader_fn()

            if not self._validate_llm_decision(validator_decision):
                return False

            leader_score = int(leader_decision["score"])
            validator_score = int(validator_decision["score"])

            leader_moderation = str(leader_decision["moderation"]).lower()
            validator_moderation = str(validator_decision["moderation"]).lower()

            leader_status = self._derive_status(leader_score, leader_moderation)
            validator_status = self._derive_status(validator_score, validator_moderation)

            leader_reward = int(self._derive_reward_points(leader_status, leader_score, leader_moderation))
            validator_reward = int(self._derive_reward_points(validator_status, validator_score, validator_moderation))

            if leader_moderation != validator_moderation:
                return False

            if leader_status != validator_status:
                return False

            if leader_reward != validator_reward:
                return False

            if abs(leader_score - validator_score) > 15:
                return False

            return True

        decision = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        score = int(decision["score"])
        moderation = str(decision["moderation"]).lower()
        reason = str(decision["reason"])

        status = self._derive_status(score, moderation)
        reward_points = self._derive_reward_points(status, score, moderation)

        record = (
            "submission_id=" + str(submission_id) + "\n"
            + "author=" + author + "\n"
            + "quest_name=" + quest_name + "\n"
            + "evidence_url=" + evidence_url + "\n"
            + "status=" + status + "\n"
            + "score=" + str(score) + "\n"
            + "reward_points=" + str(reward_points) + "\n"
            + "moderation=" + moderation + "\n"
            + "reason=" + reason
        )

        self.submissions[str(submission_id)] = record
        self.reviewed_evidence[evidence_key] = "reviewed"
        self.author_quest_claims[author_key] = "claimed"

        if status == "approved":
            current_points = self.author_points.get(author, u32(0))
            self.author_points[author] = u32(int(current_points) + int(reward_points))

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

    @gl.public.view
    def is_evidence_reviewed(self, evidence_url: str) -> str:
        evidence_key = self._normalize_evidence_key(evidence_url)
        return self.reviewed_evidence.get(evidence_key, "not_reviewed")
