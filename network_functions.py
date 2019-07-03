# Compatible amb python 3.
# coding: utf-8

# In[ ]:


# ==============================================================================
# EXPORTING THE NETWORK FUNCTION
# ==============================================================================

def nxgraph_to_gdf(G,path, node_attr=None, edge_attr=None, giant=False):
    import networkx as nx
    import numpy as np
    
    # Keep Giant component if giant == True
    if giant==True:
        G  = sorted(nx.connected_component_subgraphs(G), key = len, reverse=True)[0]

    # get the info for the gdf node section header:
    # - define the type of node attributes and put them in a list
    node_attr_gdf = []
    if node_attr != None:
        for i in range(len(node_attr)):
            a=list(G.nodes())
            attr = G.nodes[a[0]][node_attr[i]]
            if type(attr) != int and type(attr) != float and type(attr) != np.float64:
                node_attr_gdf += ['VARCHAR']
                print ('node attr',i,': varchar')

            elif type(attr) == int:
                node_attr_gdf += ['INTEGER']
                print ('node attr',i,': int')

            elif type(attr) == float or type(attr) == np.float64:
                node_attr_gdf += ['DOUBLE']
                print ('node attr',i,': double')


            else:
                # Maybe there are more options to consider apart from the three above
                print ('ERROR: node attr type not recognized')
                print (attr, type(attr))

    # get the info for the gdf edge section header:
    # - define the type of edge attributes and put them in a list
    edge_attr_gdf = []
    if edge_attr != None:
        for i in range(len(edge_attr)):
            edg1=list(G.edges())

            edge = edg1[0]
            attr = G[str(edge[0])][str(edge[1])][edge_attr[i]]
            if type(attr) != int and type(attr) != float and type(attr) != np.float64:
                edge_attr_gdf += ['VARCHAR']
                print('edge attr',i,': varchar')

            elif type(attr) == int:
                edge_attr_gdf += ['INTEGER']
                print ('edge attr',i,': int')

            elif type(attr) == float or type(attr) == np.float64:
                edge_attr_gdf += ['DOUBLE']
                print ('edge attr',i,': double')

            else:
                print ('ERROR: edge attr type not recognized')
                print (attr, type(attr))

    print ('writing...')

    with open(path,'w') as f:

        # Write NODES section
        # Heading
        f.write('nodedef>name VARCHAR,label VARCHAR')
        if node_attr != None:
            for i in range(len(node_attr)):
                f.write(','+node_attr[i]+' '+node_attr_gdf[i])

        f.write('\n')
        print ('nodes header done')

        # Elements
        for item in G.nodes():

            if node_attr != None:

                f.write(str(item)+', '+str(item))
                for i in range(len(node_attr)):
                    if i < len(node_attr)-1:
                        f.write(', '+str(G.node[item][node_attr[i]]))
                    else:
                        f.write(', '+str(G.node[item][node_attr[i]])+'\n')
            else:
                f.write(str(item)+', '+str(item)+'\n')
        print ('nodes done')

        # Write LINK section
        # Heading
        f.write('edgedef>node1 VARCHAR,node2 VARCHAR')
        if edge_attr != None:
            f.write(',')
            for i in range(len(edge_attr)):
                f.write(edge_attr[i]+' '+edge_attr_gdf[i])
                if i < len(edge_attr)-1:
                    f.write(',')
                else:
                    f.write('\n')
        else:
            f.write('\n')
        print ('edges header done')

        # Elements
        for item in G.edges():
            if edge_attr != None:
                f.write(str(item[0])+' , '+str(item[1])+', ')
                for i in range(len(edge_attr)):
                    if i < len(edge_attr)-1:
                        f.write(str(G[item[0]][item[1]][edge_attr[i]])+',')
                    else:
                        f.write(str(G[item[0]][item[1]][edge_attr[i]])+'\n')

            else:
                f.write(str(item[0])+' , '+str(item[1])+'\n')


        print ('edges done')

    return


def nxgraph_to_csv(G, path, node_attr=None, edge_attr=None, giant=False):
    import networkx as nx

    # Keep Giant component if giant == True
    if giant == True:
        G = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]

    # get the info for the gdf node section header:
    # - define the type of node attributes and put them in a list

    print ('writing...')

    node_table_file = path+'_nodes.csv'
    edge_table_file = path+'_edges.csv'

    with open(node_table_file, 'w') as f:

        # Write NODES section
        # Heading
        f.write('Name')
        if node_attr != None:
            f.write(',')
            for i in range(len(node_attr)):
                f.write(node_attr[i])
                if i < len(node_attr) - 1:
                    f.write(',')
                else:
                    f.write('\n')
        else:
            f.write('\n')

        print ('nodes header done')

        # Elements
        for item in G.nodes():

            if node_attr != None:

                f.write(str(item))
                for i in range(len(node_attr)):
                    if i < len(node_attr) - 1:
                        f.write(', ' + str(G.node[item][node_attr[i]]))
                    else:
                        f.write(', ' + str(G.node[item][node_attr[i]]) + '\n')
            else:
                f.write(str(item) + ', ' + str(item) + '\n')
        print ('nodes done')
    f.close()

        # Write LINK section
        # Heading
    with open(edge_table_file, 'w') as f:
        f.write('Node1, Node2')
        if edge_attr != None:
            f.write(',')
            for i in range(len(edge_attr)):
                f.write(edge_attr[i])
                if i < len(edge_attr) - 1:
                    f.write(',')
                else:
                    f.write('\n')
        else:
            f.write('\n')
        print ('edges header done')

        # Elements
        for item in G.edges():
            if edge_attr != None:
                f.write(str(item[0]) + ' , ' + str(item[1]) + ', ')
                for i in range(len(edge_attr)):
                    if i < len(edge_attr) - 1:
                        f.write(str(G.edge[item[0]][item[1]][edge_attr[i]]) + ',')
                    else:
                        f.write(str(G.edge[item[0]][item[1]][edge_attr[i]]) + '\n')

            else:
                f.write(str(item[0]) + ' , ' + str(item[1]) + '\n')

        print ('edges done')

    return


# In[ ]:


# ==============================================================================
# COORDINATES FUNCTION
# ==============================================================================

# ID 2.1
# baseline function: input = 2 pairs of ordered geographic coordinates
### VERSION MODIFIED BY ALESSIO TO IMPROVE COMPUTATION TIME ###
def coord_geodist(lat0, lon0, lat1, lon1):
    from math import sin, cos, radians, asin, sqrt
    lon0, lat0, lon1, lat1 = map(radians, [lon0, lat0, lon1, lat1])
    # haversine formula
    dlon = lon1 - lon0
    dlat = lat1 - lat0
    a = sin(0.5*dlat) ** 2 + cos(lat0) * cos(lat1) * sin(0.5*dlon) ** 2
    c = 2 * asin(sqrt(a))
    # 6367 is the radius of theEarth in km
    km = 6367 * c
    return km

# ==============================================================================


# ID 2.2
# baseline function: input = 2 dictonaries whose keys are "latitude" and "longitude"
### VERSION MODIFIED BY ALESSIO TO IMPROVE COMPUTATION TIME ###
def point_geodist(p1, p2):
    from math import sin, cos, radians, asin, sqrt
    lon0 = p1['longitude']
    lat0 = p1['latitude']
    lon1 = p2['longitude']
    lat1 = p2['latitude']
    lon0, lat0, lon1, lat1 = map(radians, [lon0, lat0, lon1, lat1])
    # haversine formula
    dlon = lon1 - lon0
    dlat = lat1 - lat0
    a = sin(0.5*dlat) ** 2 + cos(lat0) * cos(lat1) * sin(0.5*dlon) ** 2
    c = 2 * asin(sqrt(a))
    # 6367 is the radius of the Earth in km
    km = 6367 * c
    return km


# In[ ]:


# ==============================================================================
# DISTANCE MATRIX FUNCTIONS
# ==============================================================================

# ID 2.8
## output: matrix of distances.
## The element [i][j] = distance between node i and node j
## NEW VERSION OPTIMIZED BY ALESSIO ##
def dist_matrix(G, eucl=False):
    distances = []
    nod = list(G.nodes())
    N = len(nod)
    if eucl == False:
        for i in range(N):
            distances += [[]]
            p1 = G.nodes[str(nod[i])]
            for j in range(N):
                p2 = G.nodes[str(nod[j])]
                d = point_geodist(p1, p2)
                distances[i] += [d]
    else:
        for i in range(N):
            distances += [[]]
            p1 = G.node[nod[i]]
            for j in range(N):
                p2 = G.node[nod[j]]
                d = point_eucldist(p1, p2)
                distances[i] += [d]

    return distances


def node_geodist(G, node1, node2):
    p1 = G.node[node1]
    p2 = G.node[node2]
    km = point_geodist(p1, p2)
    return km

# Compute the length of a given path
def length_path(network,path ):
    length=0
    for p in range(0, len(path)-1):
        length=length+node_geodist(network,path[p], path[p+1] )
    return length 

