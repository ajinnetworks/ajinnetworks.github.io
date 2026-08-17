# Phase 3.2-B Status

- Commercial re-ranking engine added.
- Regression tests added for industrial buyer-intent acceptance and trend-jacking exclusion.
- Site Integrity CI runs the commercial re-rank and tests before Jekyll build.
- Priority 30 is generated at runtime from repository content.
- CI validation must run on the current PR head before merge.

Next implementation step after CI validation: rehabilitate the highest-value 5 posts as Batch 1.
