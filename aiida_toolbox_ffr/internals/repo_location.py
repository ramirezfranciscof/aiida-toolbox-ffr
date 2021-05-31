
def get_repo_location():
    from aiida.manage.manager import get_manager

    manager = get_manager()
    profile = manager.get_profile()
    repository = profile.get_repository()
    return str(repository).split()[3][0:-1]

