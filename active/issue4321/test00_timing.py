#!/usr/bin/env python3
# TO BE USED ON COMMIT d5c689c02ec7624bfdcc5473b72ab6bfd9187ae6
# To Do
# try to externalize common processes
# try to keep here all that depends on calls to the interface
# set up each test individually
# set up main to run each requested test or --all

import click
import time
import subprocess

@click.command()
def test_control():
    click.echo('Hello there')
    command = subprocess.run(['verdi', 'database', 'summary'], capture_output=True)
    output_lines = command.stdout.split(b'\n')
    output_data = output_lines[5].decode("utf-8").split()
    print( int(output_data[1]) )



def test_run():

    # Sets up the repository
    print(f'\n > Now setting up the repository...')

    # Delete unpacked files
    print(f'\n > Now deleting unpacked nodes...')

    # Do cleaning
    print(f'\n > Now cleaning deleted unpacked nodes...')
    command = subprocess.run(['verdi', 'repository', 'maintain', '--transmit'], capture_output=True)
    command = subprocess.run(['verdi', 'repository', 'maintain', '--clean'], capture_output=True)
    command = subprocess.run(['verdi', 'repository', 'maintain', '--vacuum'], capture_output=True)

    # Pack files
    print(f'\n > Now packing the nodes...')
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pack'], capture_output=True)

    # Delete packed files 
    print(f'\n > Now deleting packed nodes...')
    command = subprocess.run(['verdi', 'repository', 'maintain', '--repack'], capture_output=True)

    # Do cleaning
    print(f'\n > Now cleaning deleted packed nodes...')
    command = subprocess.run(['verdi', 'repository', 'maintain', '--transmit'], capture_output=True)
    command = subprocess.run(['verdi', 'repository', 'maintain', '--clean'], capture_output=True)
    command = subprocess.run(['verdi', 'repository', 'maintain', '--vacuum'], capture_output=True)


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    test_control()

################################################################################
