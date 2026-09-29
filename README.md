# OVN-Kubernetes ROCKs

ROCKs for OVN-Kubernetes CNI

OVN-Kubernetes is pulled from the [official repository](https://github.com/ovn-kubernetes/ovn-kubernetes).
Compiled binaries helper scripts are placed in the generated image to match the official
[ovn-kubernetes:ovn-kube-ubuntu](https://github.com/ovn-kubernetes/ovn-kubernetes/pkgs/container/ovn-kubernetes%2Fovn-kube-ubuntu) images.

## Build

To build and verify that the generated image can run the `ovnkube.sh` command
```shell
cd 1.4.0/ovn-kubernetes
rockcraft pack
sudo rockcraft.skopeo --insecure-policy copy oci-archive:ovn-kubernetes_1.4.0_amd64.rock docker-daemon:ovn-kubernetes:1.4.0
docker run -it --rm ovn-kubernetes:1.4 exec /root/ovnkube.sh display_env
```

### Building release 1.2.0

The Dockerfile for OVN-Kubernetes release 1.2 uses `ubuntu-25.10` as base.
This is an unsupported base for rockcraft, and the command is required to
build this version:

```shell
cd 1.2.0/ovn-kubernetes
rockcraft pack --ignore=unmaintained
```

## Manual Validation

With the image loaded into Docker, it is possible to use the OVN-Kubernetes
`kind.sh` development environment to test the CNI:

```shell
git clone https://github.com/ovn-kubernetes/ovn-kubernetes.git
cd ovn-kubernetes/contrib
./kind.sh -ov ovn-kubernetes:1.4.0
```
