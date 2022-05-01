from typing import Tuple

from b_aws_cdk_parallel.print_colors import PrintColors


def format_message(color: PrintColors, message: str):
    return (
        f'{color.value}'
        f'{message}'
        f'{PrintColors.ENDC.value}'
    )


def cprint(color: PrintColors, message: str) -> None:
    print(
        format_message(color, message),
        flush=True
    )


def multi_cprint(*cprints: Tuple[PrintColors, str]):
    formats = []
    for color, message in cprints:
        formats.append(format_message(color, message))

    print(
        ''.join(formats),
        flush=True
    )
