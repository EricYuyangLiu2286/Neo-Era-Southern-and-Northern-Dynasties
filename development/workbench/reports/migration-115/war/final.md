# Final integration review

The three failing cases in review.md were repaired after independent review. Settlement checks the stored diplomatic play, requires an active case and guards callback scopes before reading them. Final review-ast-results.json has 17 passing live cases, including callback_other_play, callback_after_external_terminal and callback_missing_play. This is offline script evaluation against native adapters. Old landless opponents without recorded provinces cannot prove who annexed them.
