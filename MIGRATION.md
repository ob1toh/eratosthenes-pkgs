# Hyprdots to Eratosthenes package repository

## Prepared changes

- Repair and rename the keyring package directory to `eratosthenes-keyring`.
- Package the existing public signing key, fingerprint
  `34E532A43F4BBC4B10357ADB4B3EF8D3FFEA9BA3`, under Eratosthenes filenames.
  The UID remains `hyprdots-keyring <trevor.d.ndlovu@gmail.com>`; no private key
  was read, changed, or generated.
- Remove the Docker builder's dependency on an unpublished Eratosthenes repository.
- Correct the CI Docker context to `build/` and build-output ownership.
- Skip build/publish steps when no package changes are selected.
- Serialize publishing and validate manual package/channel inputs.
- Fetch the existing Eratosthenes database, falling back to Hyprdots for the first
  migration. Stop on download errors or missing channels instead of silently
  publishing an empty replacement database.
- Preserve existing entries during incremental CI updates. Full local rebuilds
  retain their previous behavior.
- Publish the public key and concrete database/signature aliases for R2.
- Upload package objects before database objects. No remote deletion is used.

## Validation completed

- Built `eratosthenes-keyring-20260915-1-any.pkg.tar.zst` locally with makepkg.
  This test package is unsigned and has not been installed or published.
- All four source SHA-512 checksums passed makepkg validation.
- The public key verified the downloaded live Hyprdots keyring package signature.
- A real repo-add test retained an old entry when only a new package was present.
  Run it with `python3 test/incremental-db.py`.
- A local rehearsal using the live stable database preserved all 123 original
  package descriptions byte-for-byte and added the Eratosthenes keyring (124 total).
- Modified shell files and YAML workflow shell blocks passed syntax checks.

Docker image construction and GitHub Actions execution are not yet tested.
The package server has not changed. Existing package signatures were not all
reverified; the live keyring package signature was verified.

## First rollout

1. Confirm GitHub Actions secrets `GPG_PRIVATE_KEY`, `GPG_PASSPHRASE`,
   `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`, and `R2_BUCKET`.
   The signing secret must contain the private key matching the fingerprint above.
   Do not put secret values in this repository or chat.
2. Confirm R2_BUCKET is the existing bucket served by `pkgs.trevorndlovu.com`.
   The fallback database assumes its existing package objects remain at the same
   channel paths. Publishing into an empty different bucket is not a migration.
3. Push the reviewed source changes. The existing push trigger can start an edge
   build; the workflow still retains the existing weekly build schedule.
4. Manually run **Build and Deploy Packages** with package
   `eratosthenes-keyring` and mirror `stable`. It should copy the old stable
   database entries and add the signed new package.
5. Verify stable/x86_64/eratosthenes.db, its signature, eratosthenes.gpg, and the
   new keyring package over HTTPS. Validate signatures before building the ISO.
6. Resume the ISO build and VM tests. Other renamed package recipes may require
   separate corrections; this change repairs the keyring/bootstrap/publishing path.

The original Hyprdots database and package objects are left in place for existing
clients. Reverting the Git commit alone does not revert already published objects.
