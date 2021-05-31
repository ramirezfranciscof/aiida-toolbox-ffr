
def get_database_nodecount():
    #import subprocess
    #output_object = subprocess.run(['verdi', 'database', 'summary'], capture_output=True)
    #output_lines = output_object.stdout.split(b'\n')
    #output_data = output_lines[5].decode("utf-8").split()
    #return int(output_data[1])
    from aiida import orm
    query = orm.QueryBuilder()
    query.append(orm.Node)
    return query.count()

