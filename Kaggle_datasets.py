import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("kpop_idol_followers.csv")

# Clean and filter relevant columns
df_clean = df.dropna(subset=["Stage.Name", "Followers"])
df_clean = df_clean[["Stage.Name", "Followers", "Group", "Gender.x"]]
df_clean = df_clean.rename(columns={
    "Stage.Name": "Idol",
    "Followers": "Instagram_Followers",
    "Gender.x": "Gender"
})

# Create a bipartite network: Idols ↔ Instagram
B = nx.Graph()

# Add Instagram platform node
B.add_node("Instagram", bipartite=0)

# Add idol nodes and edges with follower count as weight
for row in df_clean.itertuples():
    idol = row.Idol
    followers = row.Instagram_Followers
    B.add_node(idol, bipartite=1, gender=row.Gender, group=row.Group)
    B.add_edge(idol, "Instagram", weight=followers)

# Visualize Top 20 Idols by Instagram Followers
top_20 = df_clean.sort_values(by="Instagram_Followers", ascending=False).head(20)["Idol"].tolist()
subgraph = B.subgraph(top_20 + ["Instagram"])

# Draw the subgraph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(subgraph, seed=42)  # consistent layout

# Draw nodes and edges separately for better control
nx.draw_networkx_nodes(subgraph, pos, node_size=1000, node_color='skyblue')
nx.draw_networkx_edges(subgraph, pos)
nx.draw_networkx_labels(subgraph, pos, font_size=9, font_weight='bold')

# Get and format edge labels (followers shown in 'K')
edge_labels = nx.get_edge_attributes(subgraph, 'weight')
edge_labels_formatted = {k: f"{v//1000}K" for k, v in edge_labels.items()}
nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_labels_formatted, font_size=8)

plt.title("Top 20 K-Pop Idols by Instagram Followers", fontsize=14)
plt.axis('off')
plt.show()
