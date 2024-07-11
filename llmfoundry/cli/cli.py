# Copyright 2024 MosaicML LLM Foundry authors
# SPDX-License-Identifier: Apache-2.0

import json
from argparse import Namespace
from typing import Any, Dict, List, Optional

import typer

from llmfoundry.cli import registry_cli
from llmfoundry.data_prep import convert_dataset_hf
from llmfoundry.train import train_from_yaml

app = typer.Typer(pretty_exceptions_show_locals=False)
app.add_typer(registry_cli.app, name='registry')


@app.command(name='train')
def train_from_yaml_cli(
    yaml_path: str = typer.Argument(
        ...,
        help='Path to the YAML configuration file',
    ),  # type: ignore
    args_list: Optional[list[str]] = typer.
    Argument(None, help='Additional command line arguments'),  # type: ignore
):
    """Run the training with optional overrides from CLI."""
    train_from_yaml(yaml_path, args_list)


@app.command(name='convert_dataset_hf')
def convert_dataset_hf_cli(
    dataset: str = typer.Argument(..., help='Name of the dataset'), # type: ignore
    data_subset: Optional[str] = typer.Argument(
        None, help='Subset of the dataset (e.g., "all" or "en")', # type: ignore
    ),
    splits: List[str] = typer.Argument([
        'train', 'train_small', 'val', 'val_small', 'val_xsmall', # type: ignore
    ],
                                       help='Dataset splits'), # type: ignore
    out_root: str = typer.Argument(..., help='Output root directory'), # type: ignore
    compression: Optional[str] = typer.Argument(None, help='Compression type'), # type: ignore
    concat_tokens: Optional[int] = typer.Argument(
        None, help='Concatenate tokens up to this many tokens', # type: ignore
    ),
    tokenizer: Optional[str] = typer.Argument(None, help='Tokenizer name'), # type: ignore
    tokenizer_kwargs: Optional[str] = typer.Argument( # type: ignore
        None, help='Tokenizer keyword arguments in JSON format',
    ),
    bos_text: Optional[str] = typer.Argument(None, help='BOS text'), # type: ignore
    eos_text: Optional[str] = typer.Argument(None, help='EOS text'), # type: ignore
    no_wrap: bool = typer.Option(
        False, help='Do not wrap text across max_length boundaries', # type: ignore
    ),
    num_workers: Optional[int] = typer.Argument(None, help='Number of workers'), # type: ignore
):
    # Initialize tokenizer_kwargs as an empty dictionary
    tokenizer_kwargs_dict: Dict[str, Any] = {}

    # Convert tokenizer_kwargs from JSON string to dictionary if it is a string
    if tokenizer_kwargs is not None:
        tokenizer_kwargs_dict = json.loads(tokenizer_kwargs)
    else:
        tokenizer_kwargs_dict = {}

    args = Namespace(
        dataset=dataset,
        data_subset=data_subset,
        splits=splits,
        out_root=out_root,
        compression=compression,
        concat_tokens=concat_tokens,
        tokenizer=tokenizer,
        tokenizer_kwargs=tokenizer_kwargs_dict,
        bos_text=bos_text,
        eos_text=eos_text,
        no_wrap=no_wrap,
        num_workers=num_workers,
    )
    convert_dataset_hf(args)


if __name__ == '__main__':
    app()
