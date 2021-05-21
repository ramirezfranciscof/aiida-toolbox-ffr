import lorem

from random import shuffle
from aiida import orm
from io import StringIO

from aiida.tools import delete_nodes

database_fraction = 0.3333

query = orm.QueryBuilder()
query.append(orm.Node, project=['id'])
print(f'Initial nodes: {query.count()}')

nodepk_list = [nodepk for nodepk, in query.all()]
numto_delete = int( database_fraction * len(nodepk_list) )
shuffle( nodepk_list )

delete_nodes( nodepk_list[0:numto_delete], dry_run=False )

query = orm.QueryBuilder()
query.append(orm.Node)
print(f'Final nodes: {query.count()}')

