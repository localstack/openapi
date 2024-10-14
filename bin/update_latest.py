import os
from pathlib import Path

import yaml

from localstack.utils.openapi import get_localstack_openapi_spec

openapi_path = Path(os.path.dirname(__file__)) / ".." / "openapi" / "emulators"/ "localstack-spec-latest.yml"


def main():
    spec = get_localstack_openapi_spec()
    spec["info"]["version"] = "latest"
    if not openapi_path.parent.exists():
        openapi_path.parent.mkdir()
    with open(openapi_path, "w") as f:
        yaml.dump(spec, f, sort_keys=False)


if __name__ == "__main__":
    main()

