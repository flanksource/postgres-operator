#!/bin/python3

import subprocess
import docker

flanksource = subprocess.run(["reg", "tags", "flanksource/postgres-operator"], capture_output=True)
fstags = flanksource.stdout.decode("utf-8").split()

upstream = subprocess.run(["reg", "tags", "registry.opensource.zalan.do/acid/postgres-operator"],capture_output=True)
upstags = upstream.stdout.decode("utf-8").split()

missing = [tag for tag in upstags if (tag not in fstags and "dirty" not in tag)]
client = docker.from_env()

print(f"Need to sync {len(missing)} images")
for tag in missing:
    print(f"Syncing {tag}... ", end="")
    upstring = f"registry.opensource.zalan.do/acid/postgres-operator:{tag}"
    try:
        client.images.pull(upstring)
        image = client.images.get(upstring)
        image.tag("docker.io/flanksource/postgres-operator", tag=tag)
        client.images.push(f"flanksource/postgres-operator:{tag}")
        print("Done")
    except Exception as e:
        print(f"Failed: {e}")
