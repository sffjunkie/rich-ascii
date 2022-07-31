import pathlib
import unicodedata
from typing import Iterator, NamedTuple

import click
from rich.console import Console
from rich.table import Table


class CodePointInfo(NamedTuple):
    code_point: int
    name: str
    aliases: list[str] | None


def load_name_aliases() -> dict[str, list[str]]:
    def non_comment(p: pathlib.Path) -> Iterator[str]:
        text = p.read_text()
        for line in text.split("\n"):
            if not line.startswith("#"):
                line = line.strip()
                if line:
                    yield line

    aliases: dict[str, list[str]] = {}
    p = pathlib.Path(__file__).parent / "NameAliases.txt"
    if not p.exists():
        return aliases

    for line in non_comment(p):
        code_point, alias, _ = line.split(";")
        code_point = code_point.upper()
        if code_point not in aliases:
            aliases[code_point] = [alias]
        else:
            aliases[code_point].append(alias)

    return aliases


def get_code_points() -> list[CodePointInfo]:
    name_aliases = load_name_aliases()
    code_points: list[CodePointInfo] = []
    for idx in range(256):
        if idx <= 0x1F or idx >= 0x7F and idx <= 0x9F:
            name = name_aliases[f"{idx:04X}"]
        else:
            name = [unicodedata.name(chr(idx))]

        if len(name) > 1:
            aliases = name[1:]
        else:
            aliases = None

        cp = CodePointInfo(code_point=idx, name=name[0], aliases=aliases)
        code_points.append(cp)
    return code_points


def formatted_aliases(aliases: list[str]) -> Iterator[str]:
    for alias in aliases:
        if len(alias) < 4:
            yield alias
        else:
            yield alias.title()


def display_code_points(code_points: list[CodePointInfo], show_aliases: bool = True):
    table = Table(
        title="ASCII Code Points",
        title_justify="left",
        title_style="bold green",
        header_style="blue",
    )
    if show_aliases:
        table.add_column("Dec")
        table.add_column("Hex")
        table.add_column("Name")
        table.add_column("Aliases")

        for cp in code_points:
            if cp.aliases is not None:
                aliases = ", ".join(formatted_aliases(cp.aliases))
            else:
                aliases = ""
            table.add_row(
                f"{cp.code_point:02d}",
                f"0x{cp.code_point:02X}",
                cp.name.title(),
                aliases,
            )
    else:
        table.add_column("Dec")
        table.add_column("Hex")
        table.add_column("Name")
        table.add_column("Dec")
        table.add_column("Hex")
        table.add_column("Name")
        for cp1, cp2 in zip(code_points[:128], code_points[128:]):
            table.add_row(
                f"{cp1.code_point:02d}",
                f"0x{cp1.code_point:02X}",
                cp1.name.title(),
                f"{cp2.code_point:02d}",
                f"0x{cp2.code_point:02X}",
                cp2.name.title(),
            )

    console = Console()
    console.print(table)


@click.command()
@click.option("-a", "--aliases/--no-aliases", default=False)
def run(aliases: bool):
    cp = get_code_points()
    display_code_points(cp, aliases)


run()
