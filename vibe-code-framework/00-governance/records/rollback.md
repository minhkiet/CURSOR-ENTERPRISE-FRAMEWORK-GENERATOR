# Target-only rollback procedure

Status: `VERIFIED_FOR_TARGET_ONLY`; this does not approve or unblock whole-ecosystem migration.

This procedure applies only to an explicitly approved additive import or adapter
write. It does not delete or rewrite any `.cursor` resource.

1. Before a write, record the target path, source repository/ref/path, content
   SHA-256, and the current Git revision in an Evidence Record.
2. Keep the target-only backup outside the canonical source tree, for example in
   a caller-owned release artifact directory named with the change ID.
3. Restore only the affected target directory from that backup, or restore the
   affected file from version control using the approved change ID. Do not use a
   repository-wide reset or clean operation.
4. Re-run the importer/preflight, validator, inventory, and relevant tests after
   restore. Verify that the restored SHA-256 matches the recorded evidence.
5. If the target is already tracked by version control, the release owner must
   approve the exact restore commit before it is applied.

The executed verification is limited to the explicitly selected target. It is
not evidence for a repository-wide or whole-ecosystem restore.

## Executed verification

Evidence `EVD-ROLLBACK-TARGET-001` records an isolated run on
`C:\Users\ADM\AppData\Local\Temp\vibe-rollback-smoke-d5ccdb2a1a694e4fb0964a5f9b315f4e\target\adapter`:

- Snapshot completed for two files and recorded SHA-256 values.
- An intentional extra file and content change were detected by `Verify` with
  exit code `1`.
- `Restore -ConfirmRestore` replaced only that target directory.
- Final `Verify` completed with exit code `0` and confirmed the recorded hashes.
- Passing the whole `.cursor` directory as the target was rejected with exit
  code `1`.

This evidence validates the rollback mechanism for an explicitly selected
target only. It does not classify the 910 unknown resources, resolve conflicts,
or grant approval for migration.
