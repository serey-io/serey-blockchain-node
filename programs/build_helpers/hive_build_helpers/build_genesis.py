import click
from jinja2 import Template

from pathlib import Path
import re


def clean(s):
    s = s.rstrip()
    # escape everything which is escaped again
    s = re.sub(r"\\", r"\\\\", s)
    # escape all "
    s = re.sub(r'"', r"\"", s)
    # # escape jsons again
    # s = re.sub(r'\\\\"', r"\\\\\"", s)

    return s


def read_clean(path):
    with open(path, "r") as f:
        return [clean(line) for line in f]


@click.command()
@click.argument("input_dir", type=Path)
@click.argument("output_file_path", type=Path)
@click.argument("is_testnet", type=str)
def cli(input_dir, output_file_path, is_testnet):
    is_testnet = is_testnet == "ON"

    genesis_template_path = input_dir / "genesis.hpp.tmpl"
    genesis_accounts_path = input_dir / "genesis_accounts.json"
    genesis_reward_fund_path = input_dir / "genesis_reward_fund.json"
    genesis_global_properties_path = input_dir / "genesis_global_properties.json"

    with open(genesis_template_path, "r") as f:
        template = "".join(f.readlines())
        template = Template(template)

    genesis_accounts = read_clean(genesis_accounts_path)
    if is_testnet:
        genesis_accounts = [line.replace("SRY", "TST", 1) for line in genesis_accounts]

    genesis_reward_fund = read_clean(genesis_reward_fund_path)

    genesis_global_properties = read_clean(genesis_global_properties_path)

    genesis = template.render(
        genesis_accounts=genesis_accounts,
        genesis_reward_fund=genesis_reward_fund,
        genesis_global_properties=genesis_global_properties,
    )

    if not output_file_path.parent.exists():
        try:
            output_file_path.parent.mkdir(parents=True)
        except FileExistsError:
            pass
        except:
            print(
                'Unexpected error occured while trying to create directory "{}"'.format(
                    out_file.parent.absolute().as_posix()
                )
            )
            raise
    elif not output_file_path.parent.is_dir():
        print(
            '"{}" is not a directory'.format(
                output_file_path.parent.absolute().as_posix()
            )
        )
        return 1

    with output_file_path.open(mode="w") as f:
        print(genesis, file=f)
    print('Built "{}" from .d directory'.format(output_file_path))
    return 0


if __name__ == "__main__":
    cli()
