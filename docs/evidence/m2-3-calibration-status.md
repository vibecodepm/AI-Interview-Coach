# M2.3 Calibration Status

**Status:** Foundation complete; human rating in progress  
**Date:** October 15, 2026

## Completed

- Created a versioned seed dataset with 10 examples.
- Covered behavioral, product sense, strategy, metrics, and execution categories.
- Added insufficient, generic, and long-without-evidence edge cases.
- Added a human rating guide aligned to the four-dimension rubric.
- Added a standard-library comparison script for paired human/AI scores.

## Not Yet Complete

The project does not yet have human ratings, so no human/AI agreement or calibration claim is being made. The dataset is intentionally marked `awaiting_human_ratings`.

## Next Actions

1. Have two experienced PM interviewers independently rate all 10 seed examples.
2. Resolve disagreements above two points on any dimension.
3. Run the comparison script after AI results are attached.
4. Expand the dataset toward the 50–100 example release target.
5. Create a holdout split before tuning prompts or model settings.
