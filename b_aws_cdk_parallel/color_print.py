from b_aws_cdk_parallel.print_colors import PrintColors


def cprint(color: PrintColors, message: str) -> None:
    print(
        f'{color.value}'
        f'{message}'
        f'{PrintColors.ENDC.value}',
        flush=True
    )
