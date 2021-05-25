import lorem

from numpy import random
from aiida import orm
from io import StringIO

do_big_files = False
do_small_files = True

# BIG FILES (aroung 10GB)
if do_big_files:
    total_nodes = 200

    nfiles_avg = 5
    nfiles_std = 3

    nparas_avg = 40000
    nparas_std = 5000

# BIG SMALL (aroung 10GB)
if do_small_files:
    total_nodes = 20000

    nfiles_avg = 5
    nfiles_std = 3

    nparas_avg = 400
    nparas_std = 200



instruction_setlist = []
for node_k in range(total_nodes):

    file_datadict = {}
    total_files = max(1,int(random.normal(nfiles_avg,nfiles_std)))
    for file_k in range(total_files):
        file_name = 'file_' + str(file_k) + '.txt'
        file_datadict[file_name] = int(max(1,random.normal(nparas_avg,nparas_std)))

    instruction_setlist.append( {'file_datadict': file_datadict} )


for instruction_set in instruction_setlist:
    data_node = orm.FolderData()

    for file_name, file_pars in instruction_set['file_datadict'].items():
        file_cont = lorem.paragraph()
        for paragraph_number in range(file_pars):
            file_cont = file_cont + '\n\n' + lorem.paragraph()
        file_cont = StringIO(file_cont)
        data_node.put_object_from_filelike(file_cont, file_name)

    data_node.store()
