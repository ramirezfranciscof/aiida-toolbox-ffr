#!/usr/bin/env python3
################################################################################
#
# To Do
# try to externalize common processes
# try to keep here all that depends on calls to the interface
# set up each test individually
# set up main to run each requested test or --all
# > --small-files still not sure if it works ...
#
# WORKING COMMITS:
# > ea3a697ee1e153f10881ec6a70e6d0b1d67cb9b2
#
################################################################################
import time
import click
import subprocess

from aiida_toolbox_ffr.populators.folderdata import populatedb_folderdata
from aiida_toolbox_ffr.database.delete import delete_database_proportion
from aiida_toolbox_ffr.internals.repo_location import get_repo_location
from aiida_toolbox_ffr.internals.repo_size import get_repo_size
from aiida_toolbox_ffr.database.nodecount import get_database_nodecount

from aiida import load_profile
load_profile()


@click.command()
@click.option('--mini-test', is_flag=True, help='100 nodes with around 5 files of 100kb each.')
@click.option('--big-files', is_flag=True, help='10 nodes with 1 file of 1gb each.')
@click.option('--mid-files', is_flag=True, help='200 nodes with around 5 files of 10mb each.')
@click.option('--small-files', is_flag=True, help='20000 nodes with around 5 files of 100kb each.')
@click.option('--many-files', is_flag=True, help='50000 nodes with around 10 files of 20kb each.')
@click.option('--custom-input-file', default='')
def test_control(mini_test, big_files, mid_files, small_files, many_files, custom_input_file):
    t0_start = time.perf_counter()

    if mini_test:
        click.echo('Running test for "--mini-test"...')
        setup_repository = {
            'nt_nodes': 100,
            'av_files': 5,
            'sd_files': 1,
            'av_fsize': 100,
            'sd_fsize': 10,
        }
        test_run({'setup_repository': setup_repository})

    if big_files:
        click.echo('Protocol for "--big-files" not currently implemented...')

    if mid_files:
        click.echo('Running test for "--mid-files"...')
        setup_repository = {
            'nt_nodes': 200,
            'av_files': 5,
            'sd_files': 2,
            'av_fsize': 1024*10,
            'sd_fsize': 1024*3,
        }
        test_run({'setup_repository': setup_repository})

    if small_files:
        click.echo('Running test for "--small-files"...')
        setup_repository = {
            'nt_nodes': 20000,
            'av_files': 5,
            'sd_files': 2,
            'av_fsize': 100,
            'sd_fsize': 20,
        }
        test_run({'setup_repository': setup_repository})

    if many_files:
        click.echo('Protocol for "--many-files" not currently implemented...')

    if len(custom_input_file) > 0:
        click.echo('Protocol for "--custom-input-file" not currently implemented...')

    t0_stops = time.perf_counter()
    click.echo(f' TOTAL Elapsed time: {t0_stops-t0_start}')
    click.echo('\nAll requested tests have been run. Goodbye!\n')




def test_run(test_parameters):

    # Sets up the repository
    print(f'\n > Now setting up the repository...')
    t1_start = time.perf_counter()
    setup_repository(test_parameters['setup_repository'])
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()

    # Delete unpacked files
    print(f'\n > Now deleting unpacked nodes...')
    t1_start = time.perf_counter()
    delete_unpacked = test_parameters.get('delete_unpacked', 0.25)
    delete_database_proportion(delete_unpacked)
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()
    print(f' > Now cleaning deleted unpacked nodes...')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()

    # Pack files
    print(f'\n > Now packing the nodes...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-repack -clean"'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time (pack): {t1_stops-t1_start}')
    print_repobase_stats()

    print(f'\n > Now packing the nodes...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-repack -clean"'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time (pack): {t1_stops-t1_start}')
    print_repobase_stats()
    
    print(f' > Now cleaning repacked nodes...')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()

    # Delete packed files 
    print(f'\n > Now deleting packed nodes...')
    t1_start = time.perf_counter()
    delete_packed = test_parameters.get('delete_packed', 0.333)
    delete_database_proportion(delete_packed)
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()
    print(f' > Now cleaning deleted packed nodes...')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()

    # Repack files
    print(f'\n > Now repacking nodes...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -clean"'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()

    print(f'\n > Now repacking nodes...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -clean"'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()

    print(f' > Now cleaning deleted packed nodes...')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()


################################################################################
def perform_full_cleanup():
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--live'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' >>> Elapsed time (transmit): {t1_stops-t1_start}')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -repack -vacuum"'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' >>> Elapsed time (clean): {t1_stops-t1_start}')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -repack"'], capture_output=True, input="y")
    t1_stops = time.perf_counter()
    print(f' >>> Elapsed time (vacuum): {t1_stops-t1_start}')


def print_repobase_stats():
    from aiida_toolbox_ffr.internals.repo_size import get_repo_size
    from aiida_toolbox_ffr.database.nodecount import get_database_nodecount

    nodes = str(get_database_nodecount())
    space = get_repo_size()
    print(f' > The database currently holds {nodes} nodes and the repo occupies {space}')

################################################################################
def setup_repository(setup_dict):
    # I CAN'T DO THIS LIKE SO BECAUSE I GENERATE NEW FILES THAT ARE DIFFERENT
    # FROM THE PREVIOUS ONES =(
    from os import path
    import shutil
    import hashlib
    import json

    setup_json = json.dumps(setup_dict, sort_keys=True)
    setup_hash = hashlib.md5(setup_json.encode("utf-8")).hexdigest()

    current_repopath = get_repo_location()
    source0_repobase = path.dirname(current_repopath)
    source0_reponame = 'container_src_' + setup_hash
    source0_repopath = path.join( source0_repobase, source0_reponame )

    print(f' >>> Deleting all nodes...')
    delete_database_proportion(1.0)
    print(f' >>> Cleaning up database and repository...')
    command = subprocess.run(['verdi', 'repository', 'maintain'], capture_output=True, input="y")

    #if path.exists(source0_repopath):
    #    print(f' >>> Existing source directory found: {source0_repopath}')
    #    print(f' >>> Deleting current repository...')
    #    shutil.rmtree(current_repopath)
    #    print(f' >>> Copying source repository...')
    #    shutil.copytree(source0_repopath, current_repopath)

    print(f' >>> Populating the database...')
    populate_data = populatedb_folderdata(**setup_dict)
    #print(f' >>> Total files added: {populate_data["total_files"]}')
    #print(f' >>> Total size added: {populate_data["total_size"]}')
    #print(f' >>> Average filesize: {populate_data["average_size"]}')

    if not path.exists(source0_repopath):
        print(f' >>> Copying repository for future usage...')
        shutil.copytree(current_repopath, source0_repopath)


################################################################################
if __name__ == "__main__":
    # execute only if run as a script
    test_control()

################################################################################
