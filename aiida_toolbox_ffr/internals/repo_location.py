
def get_repo_location():
    from aiida.manage.manager import get_manager
    manager = get_manager()
    backend = manager.get_backend()
    repository = backend.get_repository()
    return str(repository).split()[3][0:-1]

