#
# Copyright 2026 Canonical, Ltd.
#

import pytest
from k8s_test_harness.util import docker_util
from test_util import config, rock

IMAGE_NAME = "ovn-kubernetes"
IMAGE_BASE = f"ghcr.io/canonical/{IMAGE_NAME}"
OVNKUBE_BINARY = "/usr/bin/ovnkube"
IMAGE_ENTRYPOINT = f"{OVNKUBE_BINARY} --version"

# Binaries installed by the ovn-kubernetes part
OVN_KUBERNETES_BINARIES = [
    OVNKUBE_BINARY,
    "/usr/bin/ovn-kube-util",
    "/usr/bin/ovndbchecker",
    "/usr/bin/hybrid-overlay-node",
    "/usr/bin/ovnkube-identity",
    "/usr/libexec/cni/ovn-k8s-cni-overlay",
]


def get_ovn_kubernetes_params():
    return rock.get_rock_test_param(IMAGE_NAME, config.IMAGE_ARCH)


@pytest.mark.parametrize(
    "rock_param", get_ovn_kubernetes_params(), ids=rock.rock_param_id
)
def test_executable(rock_param: rock.RockTestParam):
    rock.run_image_direct(rock_param.image, rock_param.version, IMAGE_ENTRYPOINT)


@pytest.mark.parametrize(
    "rock_param", get_ovn_kubernetes_params(), ids=rock.rock_param_id
)
def test_pebble_executable(rock_param: rock.RockTestParam):
    if rock_param.variant == "static":
        # Static variants use different rockcraft channels with different pebble versions
        rock.check_pebble_direct(rock_param.image)
    else:
        rock.check_pebble_direct(rock_param.image, config.PEBBLE_VERSION)


@pytest.mark.parametrize(
    "binary", OVN_KUBERNETES_BINARIES, ids=lambda b: b.split("/")[-1]
)
@pytest.mark.parametrize(
    "rock_param", get_ovn_kubernetes_params(), ids=rock.rock_param_id
)
def test_binaries_present(rock_param: rock.RockTestParam, binary: str):
    process = docker_util.run_in_docker(
        rock_param.image, ["ls", binary], check_exit_code=False
    )
    assert process.returncode == 0, f"Binary {binary} not in {rock_param.image}"


@pytest.mark.parametrize(
    "rock_param", get_ovn_kubernetes_params(), ids=rock.rock_param_id
)
def test_ovn_kubernetes_version(rock_param: rock.RockTestParam):
    process = docker_util.run_in_docker(
        rock_param.image, [OVNKUBE_BINARY, "--version"], check_exit_code=0
    )
    version = None
    for line in process.stdout.splitlines():
        if "Version:" in line:
            version = line.split("Version:")[1].strip()
            break
    assert version is not None, "Version information not found in ovnkube output"
    assert (
        version == rock_param.version
    ), f"Expected version {rock_param.version} but got {version}"
