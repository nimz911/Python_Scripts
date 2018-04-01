import pandas as pd
import networkx as nx
import collections
import matplotlib.pyplot as plt
import time
import numpy as np
import matplotlib.mlab as mlab

#%%
G=nx.Graph()
G = nx.read_edgelist('<EDGES list.txt>')  # Enter EDGES list file name
DiG = nx.DiGraph(G)

#%%
nx.number_of_nodes(DiG), nx.number_of_edges(DiG)

#%%
start_time = time.time()

centrality = nx.degree_centrality(DiG)
betweenness_centrality = nx.betweenness_centrality(DiG)
closeness_centrality = nx.closeness_centrality(DiG)
degree = nx.degree(DiG)

in_degree = DiG.in_degree()
out_degree = DiG.out_degree()


centrality_df = pd.DataFrame(centrality.items(),
                            columns=['node', 'degree_centrality']).sort_values('degree_centrality', ascending=False)
degree_df = pd.DataFrame(degree.items(),
                            columns=['node', 'degree']).sort_values('degree', ascending=False)
in_degree_df = pd.DataFrame(in_degree.items(),
                            columns=['node', 'in_degree']).sort_values('in_degree', ascending=False)
out_degree_df = pd.DataFrame(out_degree.items(),
                            columns=['node', 'out_degree']).sort_values('out_degree', ascending=False)
betweenness_df = pd.DataFrame(betweenness_centrality.items(),
                            columns=['node', 'betweenness_centrality']).sort_values('betweenness_centrality', ascending=False)
closeness_centrality_df = pd.DataFrame(closeness_centrality.items(),
                            columns=['node', 'closeness_centrality']).sort_values('closeness_centrality', ascending=False)

centrality_df = centrality_df.set_index('node')
in_degree_df = in_degree_df.set_index('node')
out_degree_df = out_degree_df.set_index('node')
betweenness_df = betweenness_df.set_index('node')
closeness_centrality_df = closeness_centrality_df.set_index('node')
degree_df = degree_df.set_index('node')

metrics = betweenness_df.join(centrality_df).join(in_degree_df).join(out_degree_df).join(closeness_centrality_df).join(degree_df)

end_time = time.time()
print end_time - start_time

#%%
#nx.diameter(DiG)
nx.average_degree_connectivity(DiG)
nx.node_connectivity(DiG)
nx.average_shortest_path_length(DiG)

#%%
InDegree_count = pd.DataFrame(metrics['in_degree'].value_counts())
InDegree_count = InDegree_count.reset_index()
InDegree_count = InDegree_count.rename(columns={'in_degree': 'count', 'index': 'in_degree'})
InDegree_count['P'] = InDegree_count['count'] / InDegree_count['count'].sum()

#%%
OutDegree_count = pd.DataFrame(metrics['out_degree'].value_counts())
OutDegree_count = OutDegree_count.reset_index()
OutDegree_count = OutDegree_count.rename(columns={'out_degree': 'count', 'index': 'out_degree'})
OutDegree_count['P'] = OutDegree_count['count'] / OutDegree_count['count'].sum()

#%%
OutDegree_count.to_csv('')  # Enter OutDegree_count list file name
InDegree_count.to_csv('')   # Enter InDegree_count list file name

#%%

fig = plt.figure(figsize=(30, 10), dpi=100)
mu, sigma = np.mean(metrics['in_degree']), np.std(metrics['in_degree'])
x = metrics['in_degree']

# the histogram of the data
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)

# add a 'best fit' line
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)
plt.xticks(fontsize=30)
plt.yticks(fontsize=30)
plt.xlabel('in degree')
plt.ylabel('Probability')
#plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
#plt.axis([40, 160, 0, 0.03])
plt.grid(True)

plt.show()

#%%
%matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

colors = {1:'green', 0:'yellow'}
x = InDegree_count['in_degree']
y = InDegree_count['P']

labels = x
s = 300
c = y
plt.rcParams["figure.figsize"] = (40,15)
plt.scatter(x, y,s=s, alpha=0.7, marker="h",c=c, cmap=cm.winter)
plt.xticks(x, labels, rotation=90,size=15, color='black')
plt.yticks(color='black', fontsize=30)
plt.title('IN degree distribution', fontsize=70, color='teal')
plt.xlabel('degree', fontsize=50, color='black')
plt.ylabel(' fraction of nodes', fontsize=50, color='black')

#plt.ylim((-3000,85000))
#plt.xlim((152,180))
#plt.margins(0.1)
plt.subplots_adjust(bottom=0.008)
plt.rcParams['axes.facecolor'] = 'gainsboro'
plt.gca().yaxis.grid(True,linewidth=2, color='grey',linestyle='-.')

plt.show()


#%%
colors = {1:'green', 0:'yellow'}
x = OutDegree_count['out_degree']
y = OutDegree_count['P']

labels = x
s = 300
c = y
plt.rcParams["figure.figsize"] = (40,15)
plt.scatter(x, y,s=s, alpha=0.7, marker="h",c=c, cmap=cm.winter)
plt.xticks(x, labels, rotation=90,size=15, color='black')
plt.yticks(color='black', fontsize=30)
plt.title('OUT degree distribution', fontsize=70, color='teal')
plt.xlabel('degree', fontsize=50, color='black')
plt.ylabel(' fraction of nodes', fontsize=50, color='black')

#plt.ylim((-3000,85000))
#plt.xlim((152,180))
#plt.margins(0.1)
plt.subplots_adjust(bottom=0.008)
plt.rcParams['axes.facecolor'] = 'gainsboro'
plt.gca().yaxis.grid(True,linewidth=2, color='grey',linestyle='-.')

plt.show()

#%%
import plotly.plotly as py
import plotly.graph_objs as go

trace = go.Heatmap(x = join_df_ym['month'].astype(float),
                   y = join_df_ym['year'],
                   z = join_df_ym['count'],
                   colorscale=[[0, 'rgb(166,206,227)'], [0.25, 'rgb(31,120,180)'], [0.45, 'rgb(178,223,138)'], [0.65, 'rgb(51,160,44)'], [0.85, 'rgb(251,154,153)'], [1, 'rgb(227,26,28)']])
data=[trace]

layout = go.Layout(
    title='reddit commits per year',
    xaxis = dict(ticks='', nticks=36),
    yaxis = dict(ticks='' )
)


py.iplot(data, filename='colorscales-custom-colorscale', layout=layout)




