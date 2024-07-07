import networkx as nx
import plotly.graph_objs as go
import streamlit as st


# グラフの作成
G = nx.Graph()

# ノードとエッジの追加
G.add_node("A", title="Group 1")
G.add_node("B", title="Group 2")
G.add_node("C", title="Group 1")
G.add_edge("A", "B")
G.add_edge("A", "C")


import plotly.graph_objs as go
import streamlit as st

# カラーマップの設定
title_to_color = {"Group 1": "blue", "Group 2": "green"}
pos = nx.spring_layout(G)

# ノードの位置と色の設定
node_x = []
node_y = []
node_titles = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_titles.append(G.nodes[node]['title'])

# グループごとのノードを作成
node_traces = []
for title, color in title_to_color.items():
    trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes() if G.nodes[node]['title'] == title],
        y=[pos[node][1] for node in G.nodes() if G.nodes[node]['title'] == title],
        mode='markers',
        marker=dict(size=10, color=color),
        name=title,
        text=[node for node in G.nodes() if G.nodes[node]['title'] == title],
        hoverinfo='text'
    )
    node_traces.append(trace)

# エッジの位置の設定
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='black'),
    hoverinfo='none',
    mode='lines'
)

fig = go.Figure(data=[edge_trace] + node_traces)

# インタラクティブなズーム機能を有効にする
fig.update_layout(
    autosize=True,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        scaleanchor='y',
        scaleratio=1
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        scaleanchor='x',
        scaleratio=1
    ),
    plot_bgcolor='white',
    hovermode='closest',
    margin=dict(t=0, b=0, l=0, r=0),
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )
)

# Streamlitで表示
st.title("NetworkX Graph Visualization")
st.plotly_chart(fig, use_container_width=True)