#!/usr/bin/env python3

# To Do
# try to externalize common processes
# try to keep here all that depends on calls to the interface
# set up each test individually
# set up main to run each requested test or --all

import click

@click.command()
def test_control():
    click.echo('Hello there')



################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    test_control()

################################################################################
