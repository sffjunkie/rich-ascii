import pathlib
import unicodedata
from typing import Iterator, NamedTuple

import click
from rich.console import Console
from rich.table import Table


STYLE: str = "white"
TITLE_STYLE = "green"
HEADER_STYLE = "blue"
HIGHLIGHT_STYLE = "on green"


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


def code_point_to_int(code_point: str) -> int:
    try:
        if code_point.startswith("0x") and len(code_point) in [3, 4]:
            highlight_cp = int(code_point[2:], 16)
        else:
            highlight_cp = int(code_point)
            if highlight_cp > 255:
                highlight_cp = -1
    except ValueError:
        highlight_cp = -1

    return highlight_cp


def display_code_points(
    code_points: list[CodePointInfo],
    show_aliases: bool = True,
    style: str = STYLE,
    title_style: str = TITLE_STYLE,
    header_style: str = HEADER_STYLE,
    highlight_style: str = HIGHLIGHT_STYLE,
    code_point: str = "",
):
    if code_point != "":
        highlight_cp = code_point_to_int(code_point)
        highlight = highlight_style
    else:
        highlight_cp = -1
        highlight = ""

    table = Table(
        title="ASCII Code Points",
        title_justify="left",
        title_style=title_style,
        header_style=header_style,
    )
    if show_aliases:
        table.add_column("Dec")
        table.add_column("Hex")
        table.add_column("Name")
        table.add_column("Aliases")

        for cp in code_points:
            cp_style = highlight if cp.code_point == highlight_cp else style
            if cp.aliases is not None:
                aliases = ", ".join(formatted_aliases(cp.aliases))
            else:
                aliases = ""
            table.add_row(
                f"{cp.code_point:02d}",
                f"0x{cp.code_point:02X}",
                f"{cp.name.title()}",
                f"{aliases}",
                style=cp_style,
            )
    else:
        table.add_column("Dec")
        table.add_column("Hex")
        table.add_column("Name")
        table.add_column("Dec")
        table.add_column("Hex")
        table.add_column("Name")
        for cp1, cp2 in zip(code_points[:128], code_points[128:]):
            cp1_style = highlight if cp1.code_point == highlight_cp else style
            cp2_style = highlight if cp2.code_point == highlight_cp else style
            table.add_row(
                f"[{cp1_style}]{cp1.code_point:02d}[/]",
                f"[{cp1_style}]0x{cp1.code_point:02X}[/]",
                f"[{cp1_style}]{cp1.name.title()}[/]",
                f"[{cp2_style}]{cp2.code_point:02d}[/]",
                f"[{cp2_style}]0x{cp2.code_point:02X}[/]",
                f"[{cp2_style}]{cp2.name.title()}[/]",
            )

    console = Console()
    console.print(table)


@click.command()
@click.option(
    "--aliases/--no-aliases",
    default=False,
    help="Show a column with aliases for the name",
)
@click.option(
    "--style",
    default=STYLE,
    metavar="STYLE",
    help=f'Set the style of the text (default: "{STYLE}")',
)
@click.option(
    "--title-style",
    default=TITLE_STYLE,
    metavar="STYLE",
    help=f'Set the style of the table title (default: "{TITLE_STYLE}")',
)
@click.option(
    "--header-style",
    default=HEADER_STYLE,
    metavar="STYLE",
    help=f'Set the style of the table header (default: "{HEADER_STYLE}")',
)
@click.option(
    "--highlight-style",
    default=HIGHLIGHT_STYLE,
    metavar="STYLE",
    help=f'Set the style of highlighted text (default: "{HIGHLIGHT_STYLE}")',
)
@click.argument("code_point", default="")
def run(
    aliases: bool,
    style: str,
    title_style: str,
    header_style: str,
    highlight_style: str,
    code_point: str,
):
    """Display a table of ASCII code point information.

    \b
    If a CODE_POINT is provided then it will be hightlighted in the output.
    CODE_POINT can be either a decimal (245) or a hexadecimal (0xF5) string."""
    cp = get_code_points()
    display_code_points(
        cp, aliases, style, title_style, header_style, highlight_style, code_point
    )


run()
