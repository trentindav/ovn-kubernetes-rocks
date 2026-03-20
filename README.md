# OVN-Kubernetes Rocks

ROCKs for OVN-Kubernetes CNI

## Manual Testing

Go compiled binaries are expected to be in the dist/images folder
use Rockcraft to generate the .rock and skopeo to load it into a local Docker daemon or a registry

```shell
make bld
rockcraft pack
sudo rockcraft.skopeo --insecure-policy copy oci-archive:ovn-kubernetes_latest_amd64.rock docker-daemon:ovn-kubernetes:latest
```