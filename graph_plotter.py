#import plotly
#from plotly.graph_objs import *

import plotly.graph_objects as go
import re
import random as r
import networkx as nx


def init_graph(result_matrix):
    graph = nx.Graph()

    for project, file_matrix in result_matrix.iteritems():
        print ("I PROJECT: \t" + project)
        for file, lines in file_matrix.iteritems():
            graph.add_node(file, pos=[r.random(),r.random()], name=str(file))

            print ("I FILE: " + file)

            for line in lines:
                print ("I   " + line)
                nodes = re.findall('[a-zA-Z0-9_\-]{1,}.h', line)
                for node in nodes:
                    print ("I  Node: " + str(node))
                    graph.add_node(str(node), pos=[r.random(),r.random()], name=str(node))
                    graph.add_edge(file, str(node))
    print "Init Graph"
    print graph
    print ("Edges: " + str(graph.number_of_edges()))
    print ("Nodes: " + str(graph.number_of_nodes()))


    edge_trace = go.Scatter(x=[], y=[], line=go.scatter.Line(width=0.5,color='#888'), hoverinfo='text', mode='lines')

    for edge in graph.edges():
        x0, y0 = graph.node[edge[0]]['pos']
        x1, y1 = graph.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_x = []
    node_y = []

    for node in graph.nodes():
        x, y = graph.node[node]['pos']
        node_x.append(x)
        node_y.append(y)
        #node_trace['x'] += tuple([x])
        #node_trace['y'] += tuple([y])
        #node_trace.text = str(node)
        #node_trace.marker.color = len(str(node))

    node_trace = go.Scatter(x=node_x, y=node_y, text=[], mode='markers', hoverinfo='text', marker=go.scatter.Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=20,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(go.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text



    fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br><b>7196 OPT Inter-project dependencies graph</b>',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    )


    go.offline.plot(fig, filename='networkx.html')