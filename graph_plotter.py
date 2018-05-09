import plotly
from plotly.graph_objs import *
import re
import random as r
import networkx as nx


def init_graph(result_matrix):
    graph = nx.Graph()

    nx.random_geometric_graph(200, 0.125)


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


    edge_trace = Scatter(x=[], y=[], line=Line(width=0.5,color='#888'), hoverinfo='text', mode='lines')

    for edge in graph.edges():
        x0, y0 = graph.node[edge[0]]['pos']
        x1, y1 = graph.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]


    node_trace = Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text', marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
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

    for node in graph.nodes():
        x, y = graph.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(str(node))
        node_trace['marker']['color'].append(len(str(node)))



    fig = Figure(data=Data([edge_trace, node_trace]),
             layout=Layout(
                title='<br><b>7196 OPT Inter-project dependencies graph</b>',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))


    plotly.offline.plot(fig, filename='networkx.html')