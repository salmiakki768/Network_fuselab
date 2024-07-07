import os
import streamlit as st
import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from collections import deque
import math

# CSVファイルのパスを指定
data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
article_master_path = os.path.join(data_path, '記事マスタ_20240610.csv')
adjacency_matrix_path = os.path.join(data_path, '隣接行列_20240610.csv')

# データの読み込み
blog_masta = pd.read_csv(article_master_path)
df_matrix = pd.read_csv(adjacency_matrix_path)

# 隣接行列のインデックスとカラムを設定
df_matrix.set_index('記事タイトル', inplace=True)
df_matrix.index.name = None
df_matrix.columns = df_matrix.index

# 記事マスタの数値変換
blog_masta['Number'] = pd.to_numeric(blog_masta['Number'], errors='coerce')
blog_masta = blog_masta.dropna(subset=['Number'])
blog_masta['Number'] = blog_masta['Number'].astype(int)

# グラフの作成
G = nx.from_pandas_adjacency(df_matrix, create_using=nx.DiGraph)

# ノード属性の設定
node_labels = dict(zip(blog_masta['Number'], blog_masta['メタKW']))
node_categories = dict(zip(blog_masta['Number'], blog_masta['カテゴリー']))

# カテゴリーごとの色分けを設定
unique_categories = list(blog_masta['カテゴリー'].unique())
colors = px.colors.qualitative.Plotly
# カテゴリーの数に応じて色を繰り返す
color_map = {category: colors[i % len(colors)] for i, category in enumerate(unique_categories)}

# デフォルトの色を設定
default_color = '#888'

# 指定ノードからの前身または後身ノードを取得する関数
def get_nodes_by_depth(graph, node, depth, direction):
    related_nodes = set()
    queue = deque([(node, 0)])  # (current_node, current_depth)

    while queue:
        current_node, current_depth = queue.popleft()

        if current_depth < depth:
            if direction == "predecessors":
                neighbors = list(graph.predecessors(current_node))
            elif direction == "successors":
                neighbors = list(graph.successors(current_node))
            else:
                raise ValueError("direction must be 'predecessors' or 'successors'")

            for neighbor in neighbors:
                if neighbor not in related_nodes:
                    related_nodes.add(neighbor)
                    queue.append((neighbor, current_depth + 1))

    return list(related_nodes)

# 部分グラフを作成する関数
def create_subgraph_with_nodes_by_depth(graph, node, labels, sizes, depth, direction):
    if node not in graph:
        st.write("指定されたノードはグラフに存在しません。")
        return None

    related_nodes = get_nodes_by_depth(graph, node, depth, direction)

    subgraph_nodes = [node] + related_nodes
    subgraph = graph.subgraph(subgraph_nodes)

    if subgraph is None or len(subgraph_nodes) == 0:
        st.write("部分グラフの作成に失敗しました。")
        return None

    subgraph_labels = {n: labels.get(n, n) for n in subgraph.nodes()}
    subgraph_sizes = {n: sizes.get(n, 100) * 1000 for n in subgraph.nodes()}  # サイズを適当に設定
    subgraph_colors = {n: color_map.get(node_categories.get(n, ''), default_color) for n in subgraph.nodes()}

    return subgraph, subgraph_labels, subgraph_sizes, subgraph_colors

# ノードと深さ、方向の入力を受け取る
node = st.number_input('ノードを入力', value=3514)
depth = st.number_input('深さを入力', value=1)
direction = st.selectbox('方向を選択', ['predecessors', 'successors'])

# 部分グラフを作成
if st.button('部分グラフを作成'):
    subgraph, subgraph_labels, subgraph_sizes, subgraph_colors = create_subgraph_with_nodes_by_depth(G, node, node_labels, nx.degree_centrality(G), depth, direction)

    # グラフの描画
    if subgraph is not None:
        pos = nx.spring_layout(subgraph)

        # エッジを描画するためのヘルパー関数
        def create_edge_trace(x0, y0, x1, y1, width=2, color='#888', arrow_color='red'):
            arrow_length = 0.05  # 矢印の長さ
            arrow_width = 0.015  # 矢印の幅
            angle = math.atan2(y1 - y0, x1 - x0)
            arrow_x0 = x1 - arrow_length * math.cos(angle - math.pi / 9)
            arrow_y0 = y1 - arrow_length * math.sin(angle - math.pi / 9)
            arrow_x1 = x1 - arrow_length * math.cos(angle + math.pi / 9)
            arrow_y1 = y1 - arrow_length * math.sin(angle + math.pi / 9)

            edge_trace = go.Scatter(
                x=[x0, x1, None, x1, arrow_x0, None, x1, arrow_x1],
                y=[y0, y1, None, y1, arrow_y0, None, y1, arrow_y1],
                line=dict(width=width, color=color),
                hoverinfo='none',
                mode='lines',
                showlegend=False  # エッジの凡例を非表示にする
            )

            arrow_trace = go.Scatter(
                x=[x1, arrow_x0, x1, arrow_x1],
                y=[y1, arrow_y0, y1, arrow_y1],
                line=dict(width=width, color=arrow_color),
                hoverinfo='none',
                mode='lines',
                showlegend=False  # 矢印の凡例を非表示にする
            )

            return edge_trace, arrow_trace

        edge_traces = []
        arrow_traces = []
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_trace, arrow_trace = create_edge_trace(x0, y0, x1, y1)
            edge_traces.append(edge_trace)
            arrow_traces.append(arrow_trace)

        node_traces = []
        for category, color in color_map.items():
            node_trace = go.Scatter(
                x=[pos[n][0] for n in subgraph.nodes() if node_categories[n] == category],
                y=[pos[n][1] for n in subgraph.nodes() if node_categories[n] == category],
                mode='markers+text',
                text=[f'<b style="color:red;">{subgraph_labels[n]}</b>' if n == node else subgraph_labels[n] for n in subgraph.nodes() if node_categories[n] == category],
                textposition="top center",
                hoverinfo='text',
                marker=dict(
                    size=[subgraph_sizes[n] for n in subgraph.nodes() if node_categories[n] == category],
                    color=color,
                    showscale=False
                ),
                name=category
            )
            node_traces.append(node_trace)

        fig = go.Figure(data=edge_traces + arrow_traces + node_traces,
                     layout=go.Layout(
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

        fig.update_layout(
            dragmode='pan',  # デフォルトでPanが選ばれるように設定
        )

        st.plotly_chart(fig)
