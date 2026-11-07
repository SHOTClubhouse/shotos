# Verify a Live Release

Use this Track skill after an authorised merge, publication or upload. It gives a release owner, operations lead or reviewer one record of what the intended audience could open and do.

1. Fill in the [release record](template.md) with the intended revision, URL, audience and critical actions.
2. Open the final destination with the audience's access. Check the revision and the expected content or behaviour for each path. A correct revision can still serve a broken page or the wrong download.
3. Record the result and the time you checked it. Keep preview or test-environment evidence beside the corresponding path. For an action that writes to production, use the [signup exercise](signup-example.md) to see when an authorised tester's receipt is needed.

## Try it

Read the bundled [input](../../examples/verify-live-release/input.md) and write the release record before comparing it with the [worked output](../../examples/verify-live-release/output.md). The [Northbank walkthrough](../../../../examples/northbank-club/README.md) lets you repeat the read-only checks on the public demo.

**Needs:** The authorised release record, access equivalent to the audience's and a way to read the revision and exercise the critical paths.

**Evidence:** The [Northbank read-back](../../../../examples/northbank-club/README.md#public-read-back) checked the public revision and visitor paths in an anonymous browser. Its paths collect no visitor details.
