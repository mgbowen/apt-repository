#!/usr/bin/env python3
import datetime
import email.utils
import gzip
import hashlib
import os
import re
import shutil
import subprocess
from typing import Iterable, Tuple


LINUX_DISTROS = ["debian"]
KNOWN_ARCHITECTURES = ["all", "amd64", "arm64"]


def main():
    git_repo_root_dir = os.path.dirname(os.path.realpath(__file__))
    for linux_distro in LINUX_DISTROS:
        repo_root_dir = os.path.join(git_repo_root_dir, linux_distro)
        for distribution in os.listdir(os.path.join(repo_root_dir, "dists")):
            process_distribution(repo_root_dir, distribution)


def process_distribution(repo_root_dir: str, suite: str) -> None:
    dist_dir_path = os.path.join(repo_root_dir, "dists", suite)

    packages_file_paths = []
    components = set()
    all_architectures = set()

    for component, component_architectures in discover_components(dist_dir_path):
        # Generate a Packages file for each component-architecture tuple.
        for architecture in component_architectures:
            packages_file_paths.extend(
                generate_packages_files_for_component(
                    repo_root_dir,
                    os.path.join(dist_dir_path, component, f"binary-{architecture}"),
                )
            )

        components.add(component)
        all_architectures.update(component_architectures)

    generate_release_file_for_distribution(
        dist_dir_path,
        packages_file_paths,
        components,
        all_architectures,
    )


def generate_release_file_for_distribution(
    dist_dir_path: str,
    packages_file_paths: Iterable[str],
    components: Iterable[str],
    architectures: Iterable[str],
) -> None:
    # Generate the Release file from the components we discovered.
    with open(os.path.join(dist_dir_path, "Release"), "wt") as f:
        print(f"""
Suite: bullseye
Architectures: {' '.join(sorted(architectures))}
Components: {' '.join(sorted(components))}
Date: {email.utils.format_datetime(datetime.datetime.now())}
""".strip(),
            file=f,
        )

        hash_ctors = [
            ("MD5Sum", hashlib.md5),
            ("SHA1", hashlib.sha1),
            ("SHA256", hashlib.sha256),
        ]

        for hash_name, hash_ctor in hash_ctors:
            print(f"{hash_name}:", file=f)
            for file_path, hash_sum in get_file_hashsums(packages_file_paths, hash_ctor):
                relative_file_path = os.path.relpath(file_path, dist_dir_path)
                file_size = os.stat(file_path).st_size
                print(f" {hash_sum} {file_size:> 8} {relative_file_path}", file=f)


def discover_components(dist_dir_path: str) -> Iterable[Tuple[str, Iterable[str]]]:
    for component_name in os.listdir(dist_dir_path):
        if not os.path.isdir(os.path.join(dist_dir_path, component_name)):
            continue

        architectures = []
        for arch_name in os.listdir(os.path.join(dist_dir_path, component_name)):
            match = re.match(rf"binary-({'|'.join(KNOWN_ARCHITECTURES)})", arch_name)
            if match is None:
                continue

            architectures.append(match.group(1))

        yield component_name, architectures


def generate_packages_files_for_component(
    repo_root_dir: str, component_dir: str
) -> Iterable[str]:
    packages_path = os.path.join(component_dir, "Packages")
    with open(packages_path, "wb") as f:
        subprocess.run(
            ["dpkg-scanpackages", "-m", os.path.relpath(component_dir, repo_root_dir)],
            check=True,
            cwd=repo_root_dir,
            stdout=f,
        )

    # Create a compressed version of Packages
    packages_gz_path = packages_path + ".gz"
    with open(packages_path, "rb") as f_in:
        with gzip.open(packages_path + ".gz", "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    return [packages_path, packages_gz_path]


def get_file_hashsums(file_paths: Iterable[str], hash_ctor) -> Iterable[Tuple[str, str]]:
    for file_path in file_paths:
        hash_obj = hash_ctor()
        with open(file_path, "rb") as f:
            block = f.read(16384)  # Block size arbitrarily chosen
            if len(block) == 0:
                break

            hash_obj.update(block)

        yield file_path, hash_obj.hexdigest()


if __name__ == "__main__":
    main()
