
def get_repo_size():
    import subprocess
    from aiida_toolbox_ffr.internals.repo_location import get_repo_location

    output_object = subprocess.run(['du', '-sh', get_repo_location()], capture_output=True)
    return output_object.stdout.split(b'\t')[0].decode("utf-8")

