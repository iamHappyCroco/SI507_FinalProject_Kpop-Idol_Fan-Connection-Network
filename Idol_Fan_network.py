import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import difflib

# Load cleaned followers data
followers_df_clean = pd.read_csv("kpop_idol_followers.csv")
comments_df = pd.read_csv("kpop_youtube_comments.csv")
idols_df = pd.read_csv("kpop_idols.csv")

# Create Group to Member Mapping
group_to_members = idols_df.dropna(subset=["Group"]).groupby("Group")["Stage Name"].apply(list).to_dict()
all_group_names = list(group_to_members.keys())
all_group_names_lower = [g.lower() for g in all_group_names]

# Create Idol-Fan Graph
idol_fan_graph = nx.Graph()

# Add idol nodes
for idol in followers_df_clean["Stage.Name"]:
    idol_fan_graph.add_node(idol, type="idol")

# Add fan nodes and edges by matching video titles to groups
for row in comments_df.itertuples():
    fan = row.author
    video_title_artist = row.video_title.split("-")[0].strip().lower()
    matches = difflib.get_close_matches(video_title_artist, all_group_names_lower, n=1, cutoff=0.6)
    if matches:
        matched_group = all_group_names[all_group_names_lower.index(matches[0])]
        members = group_to_members.get(matched_group, [])
        idol_fan_graph.add_node(fan, type="fan")
        for member in members:
            if member not in idol_fan_graph:
                idol_fan_graph.add_node(member, type="idol")
            idol_fan_graph.add_edge(fan, member)
    else:
        continue

# Find the idol with most followers or most fan connections
def get_most_connected_idol(method="followers"):
    if method == "followers":
        top_idol = followers_df_clean.sort_values(by="Followers", ascending=False).iloc[0]
        print(f"Idol with most followers: {top_idol['Stage.Name']} ({top_idol['Followers']} followers)")
    elif method == "fans":
        idol_nodes = [n for n, d in idol_fan_graph.nodes(data=True) if d["type"] == "idol"]
        most_connected = max(idol_nodes, key=lambda x: idol_fan_graph.degree(x))
        print(f"Idol with most fan interactions: {most_connected} ({idol_fan_graph.degree(most_connected)} fans)")
    else:
        print("Invalid method. Use 'followers' or 'fans'.")

# Find idols who share the most fans with a given idol
def find_similar_idols(idol_name):
    if idol_name not in idol_fan_graph:
        print("Idol not found in graph.")
        return
    idol_fans = set(idol_fan_graph.neighbors(idol_name))
    idol_nodes = [n for n, d in idol_fan_graph.nodes(data=True) if d["type"] == "idol" and n != idol_name]
    similarity_scores = {}
    for other_idol in idol_nodes:
        other_fans = set(idol_fan_graph.neighbors(other_idol))
        shared_fans = idol_fans.intersection(other_fans)
        if shared_fans:
            similarity_scores[other_idol] = len(shared_fans)
    sorted_similar = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    if sorted_similar:
        print(f"Idols similar to {idol_name} based on shared fans:")
        for idol, count in sorted_similar[:5]:
            print(f"{idol} (shared fans: {count})")
    else:
        print(f"No idols share fans with {idol_name}.")

# Find the shortest fan-based connection path between two idols
def shortest_fan_path(idol1, idol2):
    if idol1 not in idol_fan_graph or idol2 not in idol_fan_graph:
        print("One or both idols not found in graph.")
        return
    try:
        path = nx.shortest_path(idol_fan_graph, source=idol1, target=idol2)
        print(f"Shortest fan path between {idol1} and {idol2}:")
        print(" -> ".join(path))
    except nx.NetworkXNoPath:
        print(f"No fan connection between {idol1} and {idol2}.")

# Print basic statistics about an idol
def idol_stats(idol_name):
    if idol_name not in followers_df_clean["Stage.Name"].values:
        print("Idol not found in followers data.")
        return
    info = followers_df_clean[followers_df_clean["Stage.Name"] == idol_name].iloc[0]
    print(f"Stats for {idol_name}:")
    print(f"Group: {info['Group']}")
    print(f"Gender: {info['Gender.x']}")
    print(f"Instagram Followers: {info['Followers']}")

# Find top fans who commented on the most idols
def top_fans_by_comment_count(top_n=5):
    fan_nodes = [n for n, d in idol_fan_graph.nodes(data=True) if d['type'] == 'fan']
    fan_degrees = [(fan, idol_fan_graph.degree(fan)) for fan in fan_nodes]
    sorted_fans = sorted(fan_degrees, key=lambda x: x[1], reverse=True)[:top_n]
    print(f"Top {top_n} fans by number of idols commented on:")
    for fan, count in sorted_fans:
        print(f"{fan}: {count} idols")

# Plot distribution of number of fans per idol (only those with non-zero fans)
def plot_idol_degree_distribution():
    idol_nodes = [n for n, d in idol_fan_graph.nodes(data=True) if d['type'] == 'idol' and idol_fan_graph.degree(n) > 0]
    degrees = [idol_fan_graph.degree(idol) for idol in idol_nodes]
    plt.figure(figsize=(10,6))
    plt.hist(degrees, bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Idol Fan Connections')
    plt.xlabel('Number of Fans')
    plt.ylabel('Number of Idols')
    plt.show()

# Count total fans connected to each group
def group_fan_counts(idol_fan_graph, group_to_members):
    group_counts = {}
    for group, members in group_to_members.items():
        fan_set = set()
        for member in members:
            if member in idol_fan_graph:
                fan_set.update(idol_fan_graph.neighbors(member))
        group_counts[group] = len(fan_set)
    sorted_groups = sorted(group_counts.items(), key=lambda x: x[1], reverse=True)
    print("\nTop Groups by Total Fan Connections:")
    for group, count in sorted_groups:
        if count > 0:
            print(f"{group}: {count} fans")

# Find groups that share the most fans
def most_shared_fans_between_groups(idol_fan_graph, group_to_members):
    max_shared = 0
    top_pair = (None, None)
    group_fans = {}
    
    for group, members in group_to_members.items():
        fan_set = set()
        for member in members:
            if member in idol_fan_graph:
                fan_set.update(idol_fan_graph.neighbors(member))
        if fan_set:
            group_fans[group] = fan_set

    groups = list(group_fans.keys())
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            shared = group_fans[groups[i]].intersection(group_fans[groups[j]])  # <--- fixed here
            if len(shared) > max_shared:
                max_shared = len(shared)
                top_pair = (groups[i], groups[j])

    if top_pair[0] and top_pair[1]:
        print(f"\nGroups with Most Shared Fans: {top_pair[0]} and {top_pair[1]} ({max_shared} shared fans)")


# Rank groups by total network centrality
def group_centrality(idol_fan_graph, group_to_members):
    group_scores = {}
    for group, members in group_to_members.items():
        degree_sum = sum(idol_fan_graph.degree(member) for member in members if member in idol_fan_graph)
        if degree_sum > 0:
            group_scores[group] = degree_sum
    sorted_centrality = sorted(group_scores.items(), key=lambda x: x[1], reverse=True)
    print("\nGroup Centrality Rankings (based on total degrees):")
    for group, score in sorted_centrality:
        print(f"{group}: {score}")

# Example Usage Calls 
get_most_connected_idol("followers")
get_most_connected_idol("fans")
find_similar_idols("Lisa")
shortest_fan_path("Jennie", "Taeyong")
idol_stats("Taeyong")
top_fans_by_comment_count(5)
plot_idol_degree_distribution()
group_fan_counts(idol_fan_graph, group_to_members)
most_shared_fans_between_groups(idol_fan_graph, group_to_members)
group_centrality(idol_fan_graph, group_to_members)
