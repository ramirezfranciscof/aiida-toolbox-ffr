################################################################################
#
#
################################################################################
def delete_database_proportion( fraction=0.0 ):
    """Description pending"""
    from random import shuffle
    from aiida import orm
    from aiida.tools import delete_nodes

    query = orm.QueryBuilder()
    query.append(orm.Node, project=['id'])
    initial_nodecount = query.count()

    nodepk_list = [nodepk for nodepk, in query.all()]
    shuffle( nodepk_list )

    numto_delete = int( fraction * len(nodepk_list) )
    numto_delete = min( numto_delete, initial_nodecount )

    delete_nodes( nodepk_list[0:numto_delete], dry_run=False )

    query = orm.QueryBuilder()
    query.append(orm.Node)
    final_nodecount = query.count()

    return {'initial_nodecount': initial_nodecount, 'final_nodecount': final_nodecount}

################################################################################
