# K-Pop Idol–Fan Interaction Network  
**SI 507 Final Project**

## Overview

This project explores the interaction between K-pop idols and their fans by building a fan-idol network graph based on YouTube comment data and idol follower data.  
The goal is to visualize fan engagement patterns, identify shared fanbases between different groups, and practice real-world data collection, processing, and network analysis.

## Project Structure

```plaintext
kpop_idol_followers.csv        # Kaggle dataset: idol names, groups, Instagram followers
kpop_youtube_comments.csv      # Scraped dataset: fan comments from K-pop music videos
kpop_idols.csv                 # Kaggle dataset: idol basic information (stage names, groups)
Kaggle_datasets.py             # Script to build a simple idol ↔ Instagram followers network
YouTube_scraper.py             # Script to collect YouTube comment data using YouTube API
Idol_Fan_Network.py            # Main script building and analyzing the fan-idol network graph
```

## Methodology

1. **Data Collection**  
   - Kaggle datasets: K-pop idol profiles and Instagram follower counts  
   - YouTube Data API: Comments from 200+ official K-pop music videos across 30+ groups

2. **Data Processing**  
   - Built a group-to-members mapping from idol data
   - Matched YouTube commenters to idol groups using fuzzy matching
   - Constructed a bipartite network (fans ↔ idols)

3. **Network Analysis**  
   - Found the idol with the most fans or followers
   - Identified idols with shared fans
   - Calculated shortest fan paths between idols
   - Summarized top multi-fandom fans
   - Analyzed group-level fan counts and centrality

4. **Visualization**  
   - Visualized top 20 idols by Instagram followers
   - Plotted distribution of fan connections across idols


## Key Insights

- BLACKPINK and BTS dominate the network in terms of fan base size and shared fans.
- Groups like SEVENTEEN and TWICE show high fan network centrality.
- Some fans are highly multi-fandom, actively engaging across many different groups.

## Example Visualizations

- Network graph: Top idols connected to Instagram
- Histogram: Distribution of number of fans per idol

## Future Improvements

- Expand YouTube comment collection to larger volumes
- Integrate Twitter and Instagram fan engagement data
- Apply community detection algorithms to find hidden fan communities

## 📧 Contact

Created by **Zhile Wu** for SI 507 Final Project  
