import os
from pathlib import Path

import yaml

from localstack.utils.openapi import get_localstack_openapi_spec
from localstack.version import version as ls_version

import click


def str_presenter(dumper, data):
    """
    Reading multiline yaml strings (with the `|` indicator) results in newlines added when dumping the YAML.
    This function helps to preserve the original multiline formatting.
    """
    if '\n' in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


yaml.add_representer(str, str_presenter)


@click.command()
@click.option('--latest', is_flag=True, default=False, help='If enabled, sets the version of the spec to latest.')
def update_aws_spec(latest: bool) -> None:
    """
    This function retrieves the OpenAPI specs declared via plugins, sets a given version and store the result
    in a file at a given path.
    """
    version = "latest" if latest else ls_version
    base_path = Path(os.path.dirname(__file__)) / ".." / "openapi" / "emulators"
    if latest:
        openapi_path = base_path / "localstack-spec-latest.yml"
    else:
        openapi_path = base_path / "localstack-spec.yml"
    spec = get_localstack_openapi_spec()
    spec["info"]["version"] = version
    if not openapi_path.parent.exists():
        openapi_path.parent.mkdir()
    with open(openapi_path, "w") as f:
        yaml.dump(spec, f, sort_keys=False)


if __name__ == "__main__":
    update_aws_spec()

