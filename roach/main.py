# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of Roach - https://github.com/jbremer/roach.
# See the file 'docs/LICENSE.txt' for copying permission.

from builtins import bytes
import click

from roach import procmem

@click.group()
def main():
    pass

@main.command("procmem.list")
@click.argument("mempath", type=click.Path(exists=True))
def procmem_list(mempath):
    p = procmem(mempath)
    for region in p.regions:
        s = p.readv(region.addr, 16)
        if isinstance(s, str):
            print("0x%08x .. 0x%08x" % (region.addr, region.addr + region.size)),
            print(repr(s))
        else:
            s = "'"+"".join([chr(c) for c in s])+"'"
            print("0x%08x .. 0x%08x" % (region.addr, region.addr + region.size), s)

