# Sol regional review

Configuration: gpt-6.1-sol / medium, delegated by root. Read-only source review, no game. Compared current root regional changes to before/ snapshots; new customizable localization has no before/ file.

## Finding: P2 retarget permits unchanged coverage when only anchor two becomes invalid

common/scripted_triggers/nesnd_small_actions.txt:22 includes NOT targets_valid as an unconditional reason that groups changed. targets_valid also checks representative population minimum, independently of group membership. Five owned populated states at 5m,2m,1.5m,1m,0.4m can retain group1={5m},group2={other4}, anchor_one=5m, anchor_two=0.4m after population changes. Old anchor_two is now below 5% of total9.9m, so targets_valid=false. generic_targets_available remains true via5m and2m. All current groups already match the proposed split. Nevertheless changes_groups=true; can_retarget and visible pass with no cooldown/revolution; execution picks2m as new second representative, registers identical populated group memberships and resets observation/cooldown. This contradicts the new comment and player text that representative names alone are not new development targets.

Suggested gate distinguishes anchor_one missing/wrong group registration from complete target validity; keep comparisons for a larger populated state, extra first-group members and missing second-group members. Anchor_two validity alone must not imply changed coverage.

## Other reviewed behavior

Regional economy flattening is logically equivalent to the previous source: the previous safe predicate expands to hidden state_country+not provisional, no default, nonnegative net_fixed_income and no revolution; all employment/access thresholds remain0.6/0.75; previous regional_industry expands to identical targets-valid, each production>=1 and classes>=2 OR specialisation. Far-south non-generic50%-occupied port checks are unchanged. custom_tooltip wraps predicates without changing their values. No references to removed regional_industry symbol remain in txt files.

Custom region names match registered geography: far-south mainland/NewZealand, Burma upper/lower, Siam Bangkok/interior-or-outer; generic first is anchor_one and second is remaining selected states. Numeric scripts aggregate registered groups, so these labels correct the former implication that anchor states alone were counted. New employment/access/production/class/port tooltips agree with actual numeric definitions and thresholds. Chinese/English key contracts correspond; prose final author review belongs to Astra.

Retarget protection is repeated in visible, possible and execution guard; nesnd_small_retarget itself calls can_retarget. More-than4 states is enforced throughout. Outer trigger_if exists anchor_one excludes missing-reference branches; inside any_scope_state prev is the invoking country, so prev.var:anchor_one accesses that country variable. Inner scripted group predicates do not alter the caller scope. This is scope reasoning from actual call sites, not engine execution certification. Ties in largest state are conservatively treated as no change when existing membership already matches; no claim of exact tie-order equivalence to ordered_scope_state is made.

Remaining engine boundary: no live UI evaluation or native ordered tie selection was run. This review does not certify ENGINE_PASS.
