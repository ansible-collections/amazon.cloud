#!/usr/bin/env python3
"""Script to update aws hard-coded user agent variable with value from galaxy.yml."""

import logging
import re

from pathlib import PosixPath
from argparse import ArgumentParser
import yaml


FORMAT = "[%(asctime)s] - %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def main() -> None:
    """Read collection info and update aws user agent if needed."""

    parser = ArgumentParser(description="Update collection constants with galaxy.yml version")
    parser.add_argument("--path", help="The path to the collection", type=PosixPath, default="")
    args = parser.parse_args()

    # Read collection information from galaxy.yml
    galaxy_info = {}
    with (args.path / "galaxy.yml").open(encoding="utf-8") as file_desc:
        galaxy_info = yaml.safe_load(file_desc)
    variable_name = f"{galaxy_info['namespace'].upper()}_{galaxy_info['name'].upper()}_COLLECTION_VERSION"
    logger.info("Collection variable name => %s", variable_name)

    galaxy_version = galaxy_info.get("version")
    logger.info("galaxy.yml version => %s", galaxy_version)

    variable_regex = rf"^{variable_name} = [\"|'](.*)[\"|']"

    # Update user-agent variable
    for item in (args.path / "plugins").glob("**/*.py"):
        updated_content = []
        for line in item.read_text().split("\n"):
            m = re.match(variable_regex, line)
            if m and m.group(1) != galaxy_version:
                logger.info("-- %s -- match variable [%s] with value [%s]", item.name, variable_name, m.group(1))
                updated_content.append(f'{variable_name} = "{galaxy_version}"')
                continue
            updated_content.append(line)
        result = "\n".join(updated_content)
        if result != item.read_text():
            logger.info("%s => updated.", item)
            item.write_text(result)


if __name__ == "__main__":
    main()