# import matplotlib.pyplot as plt
# import pandas as pd
#
# episodes = pd.read_csv('./episodes.csv') 
# x = episodes.Season.astype(str) + episodes.Episode.astype(str)
#
# plt.ion()
# graph = plt.plot(x, episodes['episode_count'])[0]
#
#
# while True:
#     episodes = pd.read_csv('./episodes.csv') 
#     graph.ydata(episodes['episode_count'].values)
#     plt.draw()
#     plt.pause(0.5)
#

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

# Read data once initially
episodes = pd.read_csv('./episodes.csv')

# Create figure and axis
fig, ax = plt.subplots()
ax.set_xlabel('Episode')
ax.set_ylabel('Count')
ax.set_title('Episode Statistics')

# Initial plot
x = episodes['Season'].astype(str) + '_' + episodes['Episode'].astype(str)
y = episodes['episode_count']
line, = ax.plot(x, y)
plt.xticks(rotation=90)
plt.grid()

def animate(i):
    # Read updated data
    episodes_update = pd.read_csv('./episodes.csv')
    
    # Update x and y data
    x_update = episodes_update['Season'].astype(str) + '_' + episodes_update['Episode'].astype(str)
    y_update = episodes_update['episode_count']
    
    # Update the plot data
    line.set_xdata(x_update)
    line.set_ydata(y_update)
    plt.xticks(rotation=90)
    
    # Update labels and limits if needed
    ax.relim()
    ax.set_ylim(bottom=0, top=max(y_update) * 1.1)  # Add padding to y limits
    plt.tight_layout()
    fig.canvas.draw()

# Create animation
ani = FuncAnimation(fig, animate, interval=500)

plt.show()
