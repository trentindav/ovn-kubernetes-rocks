# Repository Instructions for ovn-kubernetes-rocks

## 1. Project Overview

OCI container images (ROCKs) for the OVN-Kubernetes CNI, built with [rockcraft](https://canonical-rockcraft.readthedocs-hosted.com/). Each image is a drop-in replacement for the upstream [`ovn-kubernetes/ovn-kube-ubuntu`](https://github.com/ovn-kubernetes/ovn-kubernetes/pkgs/container/ovn-kubernetes%2Fovn-kube-ubuntu) image. This repository follows the same standards as [canonical/cilium-rocks](https://github.com/canonical/cilium-rocks).

## 2. Tech Stack

* **Languages:** YAML (rockcraft specs), Python (tests), Bash (build scripts within rockcraft parts)
* **Build Tools:** `rockcraft` (OCI image builder), `tox` (Python test runner)
* **Test Framework:** `pytest`, `k8s-test-harness`
* **CI/CD:** GitHub Actions with [`canonical/k8s-workflows`](https://github.com/canonical/k8s-workflows) reusable workflows
* **Security Scanning:** Trivy (configured in `trivy.yaml`)

## 3. The Constitution (Immutable Rules)

* **Formatting:** Use 4-space indentation in Python. Enforce `black` (max line length 120), `isort` with the `black` profile, `flake8`, and `codespell` via `tox -e format` and `tox -e lint`.
* **License Headers:** All Python files must start with the Canonical copyright header (enforced by `licenseheaders` in tox lint/format envs):
  ```python
  #
  # Copyright <year> Canonical, Ltd.
  #
  ```
* **Security:** Store all credentials and tokens in GitHub Actions secrets. Report vulnerabilities via [GitHub Private Security Report](https://github.com/canonical/ovn-kubernetes-rocks/security/advisories/new) as documented in `SECURITY.md`.
* **Testing:** All new or updated rocks must have corresponding sanity tests in `tests/sanity/`.
* **Multi-arch:** All rocks must declare both `amd64` and `arm64` under `platforms:` in `rockcraft.yaml`.
* **Rockcraft version pinning:** Pin the `rockcraft` snap revision per architecture in `.rockcraft-version.yaml`.

## 4. Project Structure

```
<version>/                    # One directory per upstream OVN-Kubernetes release
  ovn-kubernetes/             # Rock name for this project (matches image name)
    rockcraft.yaml            # Rock definition (or per-image subdirectory)
tests/
  tox.ini                     # Tox configuration for format, lint, sanity, integration envs
  requirements-dev.txt        # Dev/lint dependencies (black, isort, flake8, codespell, licenseheaders)
  requirements-test.txt       # Test dependencies (pytest, k8s-test-harness)
  .copyright.tmpl             # License header template for licenseheaders
  sanity/
    test_<rock_name>_rock.py  # Pytest sanity tests per rock image
    test_util/
      config.py               # Test configuration (arch, pebble version, repo path)
      rock.py                 # Shared test helpers (RockTestParam, run_image_direct, check_pebble_direct)
.github/
  workflows/
    pull_request.yaml         # CI: build, test, scan, assemble multiarch (uses canonical/k8s-workflows)
    cla-check.yaml            # CLA check workflow
docs/                         # Supplementary documentation (e.g., fips.md)
.rockcraft-version.yaml       # Pinned rockcraft snap revisions per architecture
trivy.yaml                    # Trivy offline scan config (timeout: 20m)
SECURITY.md                   # Vulnerability reporting policy
CODEOWNERS                    # Code ownership assignments
```

## 5. Development Workflow

* **Build a rock:** `cd <version> && rockcraft pack`
* **Load and test manually:**
  ```shell
  sudo rockcraft.skopeo --insecure-policy copy oci-archive:<rock-file>.rock docker-daemon:<name>:<version>
  docker run -it --rm <name>:<version> exec /root/ovnkube.sh display_env
  ```
* **Lint Python tests:** `cd tests && tox -e lint`
* **Format Python tests:** `cd tests && tox -e format`
* **Run sanity tests:**
  ```shell
  export BUILT_ROCKS_METADATA='[{"name":"<name>","version":"<version>","path":"<version>/<name>","arch":"amd64","image":"<name>:<version>","rockcraft-revision":"","runs-on-labels":[]}]' 
  cd tests && tox -e sanity
  ```

## 6. CI/CD Conventions

* CI reuses workflows from `canonical/k8s-workflows@main` for: building rocks, running tests, scanning images with Trivy, and assembling multiarch manifests.
* The `pull_request.yaml` workflow runs on both `pull_request` and `push` to `main`.
* Rockcraft revisions used in CI must match those in `.rockcraft-version.yaml`.

## 7. rockcraft.yaml Conventions

* Use `license: Apache-2.0` (matches OVN-Kubernetes upstream).
* Pin the upstream `source-branch` or `source-tag` explicitly in every `git` source part.
* Use `override-build` scripts to install binaries to `$CRAFT_PART_INSTALL` using `install -D -m 0755`.
* Reference upstream Dockerfile comments to document the purpose of each build step.
* Add `TODO` comments for any known gaps or areas requiring investigation.
