################################################################################
#
#
################################################################################
def populatedb_folderdata(**kwargs):
    import lorem
    from numpy import random
    from aiida import orm
    from io import StringIO
    from copy import deepcopy

    nt_nodes = kwargs.get('nt_nodes', 1000) # Total number of nodes
    av_files = kwargs.get('nt_nodes', 5) # Average number of files
    sd_files = kwargs.get('nt_nodes', 2) # Std deviation of files
    av_fsize = kwargs.get('nt_nodes', 2048) # Average size of files (kb)
    sd_fsize = kwargs.get('nt_nodes', 1024) # Std deviation of sizes (kb)

    output_dict = {}

    # Generating instruction set
    node_filelist = []
    for k_node in range(nt_nodes):

        nt_files = max( 1, int(random.normal(av_files,sd_files)) )
        node_files = {}
        
        for k_file in range(nt_files):

            nt_size = max( 0, int(random.normal(av_fsize,sd_fsize)) )
            lorem_paragraphs = max( 0, 3 * nt_size - 1 )
            # Each Lorem paragraph is around 0.3kb (1kb = 3 paragraphs)

            file_name = 'file_' + str(k_file) + '.txt'
            node_files[file_name] = lorem_paragraphs

        node_filelist.append(deepcopy(node_files))
        counter = len(node_filelist)
        if counter % 100 == 0:
            print(counter)
        #print()
        #print(node_filelist)

    # Storing actual data
    counter = 0
    for node_files in node_filelist:
        
        counter = counter + 1
        data_node = orm.FolderData()

        for filename, numpara in node_files.items():

            #print(filename, numpara)
            file_cont = lorem.paragraph()
            for paragraph_number in range(numpara):
                file_cont = file_cont + '\n\n' + lorem.paragraph()
            file_cont = StringIO(file_cont)
            #print(file_cont)

            data_node.put_object_from_filelike(file_cont, filename)
        
        #print(data_node)
        data_node.store()
        if counter % 100 == 0:
            print(counter)
        print(data_node)
        #print()

    return output_dict


################################################################################
