# OVN-Kubernetes ROCKs

ROCKs for OVN-Kubernetes CNI

OVN-Kubernetes is pulled from the [official repository](https://github.com/ovn-kubernetes/ovn-kubernetes).
Compiled binaries helper scripts placed in the generated image to match the official
[ovn-kubernetes:ovn-kube-ubuntu](https://github.com/ovn-kubernetes/ovn-kubernetes/pkgs/container/ovn-kubernetes%2Fovn-kube-ubuntu) images.

## Manual Testing

To build and verify that the generated image can run the `ovnkube.sh` command
```shell
cd 1.2
rockcraft pack
sudo rockcraft.skopeo --insecure-policy copy oci-archive:ovn-kubernetes_1.2_amd64.rock docker-daemon:ovn-kubernetes:1.2
docker run -it --rm ovn-kubernetes:1.2 exec /root/ovnkube.sh display_env
```