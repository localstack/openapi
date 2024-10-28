import os
from pathlib import Path

import yaml

from localstack.utils.openapi import get_localstack_openapi_spec
from localstack.version import version as ls_version

import click

@click.command()
@click.option('--latest', is_flag=True, default=False, help='If enabled, sets the version of the spec to latest.')
def update_aws_spec(latest: bool) -> None:
    """
    This function retrieves the OpenAPI specs declared via plugins, sets a given version and store the result
    in a file at a given path.
    """
    version = "latest" if latest else ls_version
    openapi_path = Path(os.path.dirname(__file__)) / ".." / "openapi" / "emulators"/ f"localstack-spec-{version}.yml"
    spec = get_localstack_openapi_spec()
    spec["info"]["version"] = version
    if not openapi_path.parent.exists():
        openapi_path.parent.mkdir()
    with open(openapi_path, "w") as f:
        yaml.dump(spec, f, sort_keys=False)


if __name__ == "__main__":
    update_aws_spec()

