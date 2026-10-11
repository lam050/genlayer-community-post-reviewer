import { createAccount, createClient, isSuccessful } from "genlayer-js";
import { studionet } from "genlayer-js/chains";
import { TransactionHashVariant } from "genlayer-js/types";

/**
 * Minimal SDK integration example for GenLayer Community Quest Moderator V5.
 *
 * This shows how a real quest platform can:
 * 1. Submit a quest evidence URL to the contract.
 * 2. Wait for successful finalization.
 * 3. Read the resulting submission record.
 *
 * Replace CONTRACT_ADDRESS with the deployed contract address from GenLayer Studio.
 */

const CONTRACT_ADDRESS = "0x7Ae6A79abc3c32db2C95D4F24EE6e3F4b6B89B05";

const QUEST_NAME = "GenLayer Community Special Quest";

const EVIDENCE_URL =
  "https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/922b5f642dc6da34b058cb94f1e13acc229c760d/evidence/sample-community-post.md";

async function main() {
  const account = createAccount();

  const client = createClient({
    chain: studionet,
    account,
  });

  const write = {
    address: CONTRACT_ADDRESS as `0x${string}`,
    functionName: "review_submission",
    args: [QUEST_NAME, EVIDENCE_URL],
  };

  console.log("Submitting review_submission...");

  const estimate = await client.estimateTransactionFeesForWrite(write);

  const txId = await client.writeContract({
    ...write,
    fees: {
      distribution: estimate.distribution,
      feeValue: estimate.feeValue,
    },
  });

  console.log("Submitted transaction:", txId);

  const receipt = await client.waitForFinalization({
    hash: txId,
  });

  if (!isSuccessful(receipt)) {
    throw new Error(
      `review_submission failed: ${receipt.statusName} / ${receipt.txExecutionResultName}`,
    );
  }

  console.log("review_submission finalized successfully.");

  const submission = await client.readContract({
    address: CONTRACT_ADDRESS as `0x${string}`,
    functionName: "get_submission",
    args: [1],
    transactionHashVariant: TransactionHashVariant.LATEST_FINAL,
  });

  console.log("Submission record:");
  console.log(submission);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
