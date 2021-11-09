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
import sys
import yaml
import time
import subprocess

#from aiida import load_profile
#load_profile()
from aiida import orm
from aiida.manage.manager import get_manager

from aiida_toolbox_ffr.populators.folderdata import populatedb_folderdata
from aiida_toolbox_ffr.database.delete import delete_database_proportion
from aiida_toolbox_ffr.internals.repo_location import get_repo_location
from aiida_toolbox_ffr.internals.repo_size import get_repo_size
from aiida_toolbox_ffr.database.nodecount import get_database_nodecount


def performance_testrun():
    """Description pending"""

    # READ SETTINGS
    if len(sys.argv) != 2:
        raise ValueError('Use this as `verdi run performance_testrun.py <yaml_file>`')

    settings_yaml = sys.argv[1]
    with open(settings_yaml) as yaml_file:
        test_settings = yaml.safe_load(yaml_file)

    print(f' > Preliminary cleanup...')
    t1_start = time.perf_counter()
    delete_database_proportion(1.0)
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()

    # CHECK PROFILE
    if get_database_nodecount() > 0:
        manager = get_manager()
        profile = manager.get_profile()
        if profile is None:
            error_msg = 'There is no profile loaded, please create an empty new one.'
        else:
            error_msg = f'Current profile {profile.name} is not empty. Please change to an empty profile.'
        raise RuntimeError(error_msg)

    # MAKE SURE THE REPO IS SYNC AND CLEAN
    subprocess.run(['verdi', 'repository', 'maintain'], capture_output=True, input=b'y')

    # RUN THE ACTUAL TESTS
    t0_init = time.perf_counter()
    perform_tests(test_settings)
    t0_stop = time.perf_counter()
    print(f' > TOTAL elapsed time: {t0_stop-t0_init}')


################################################################################
def perform_tests(test_settings):
    """Description pending"""
    
    # Sets up the repository
    print(f'\n > Setting up initial repository...')
    t1_start = time.perf_counter()
    populatedb_folderdata(**test_settings['initial_repository'])
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()

    # Delete unpacked files
    print(f'\n > Now deleting unpacked nodes...')
    t1_start = time.perf_counter()
    delete_unpacked = test_settings.get('delete_unpacked', 0.25)
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
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-repack -clean"'], capture_output=True, input=b"y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time (pack): {t1_stops-t1_start}')
    print_repobase_stats()

    print(f'\n > Now packing the nodes...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-repack -clean"'], capture_output=True, input=b"y")
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
    delete_packed = test_settings.get('delete_packed', 0.333)
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
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -clean"'], capture_output=True, input=b"y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()

    print(f'\n > Now repacking nodes...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -clean"'], capture_output=True, input=b"y")
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    print_repobase_stats()

    print(f' > Now cleaning deleted packed nodes...')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()

    print(f' > Now deleting all the rest...')
    t1_start = time.perf_counter()
    delete_database_proportion(1.0)
    t1_stops = time.perf_counter()
    print(f' > Elapsed time: {t1_stops-t1_start}')
    perform_full_cleanup()
    print_repobase_stats()
    perform_full_cleanup()
    print_repobase_stats()




################################################################################
def perform_full_cleanup():
    """Description pending"""
    print(f' > Performing full cleanup...')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--live'], capture_output=True, input=b"y")
    t1_stops = time.perf_counter()
    print(f' >>> Elapsed time (transmit): {t1_stops-t1_start}')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -repack -vacuum"'], capture_output=True, input=b"y")
    t1_stops = time.perf_counter()
    print(f' >>> Elapsed time (clean): {t1_stops-t1_start}')
    t1_start = time.perf_counter()
    command = subprocess.run(['verdi', 'repository', 'maintain', '--pass-down "-pack -repack"'], capture_output=True, input=b"y")
    t1_stops = time.perf_counter()
    print(f' >>> Elapsed time (vacuum): {t1_stops-t1_start}')


def print_repobase_stats():
    """Description pending"""
    nodes = str(get_database_nodecount())
    space = get_repo_size()
    print(f' > STATS:')
    print(f' >>> The DB currently holds {nodes} nodes and the repo occupies {space}')

################################################################################
if __name__ == "__main__":
    """Main process"""
    performance_testrun()
################################################################################
