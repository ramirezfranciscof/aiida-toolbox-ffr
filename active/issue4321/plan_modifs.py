# aiida.cmdline.commands.cmd_repository.py

@verdi_repository.command('maintain')
@click.option('--fast', is_flag=True, help='Performs only the quickest of maintenances')
@click.option('--deep', is_flag=True, help='Performs deep maintenance tasks')
def database_version(fast, deep):
    """Performs maintenance tasks on the repository."""
    from aiida.repository.control import repository_maintain

    if deep:
        print('This should contain some sort of warning')

        if fast:
            print('does it make sense to do a fast + deep maintain?')

    repository_maintain(fast, deep)


# aiida.repository.backend.disk_object_store.py:DiskObjectStoreRepositoryBackend

    def maintain(self, fast: bool = False, deep: bool = False, control_dict: dict = dict()) -> None:

        if deep:
            self.container.repack()
            self.container.clean_storage(vacuum=True)
        
        else:
            self.container.pack_all_loose()


