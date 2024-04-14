import matplotlib.pyplot as plt


def visualize_3d_keypoints(keypoints, M=None, bound=True):
    """

    Args:
        keypoints: 3D keypoints (N,K,3)
        M: center of mass (N,3 )
        bound: if True the axis limits are set to [-1,1] else the limits are set to the min and max of the keypoints

    Returns:

    """
    # Extracting dimensions
    k, _ = keypoints.shape
    # Initialize figure and 3D axis
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    if bound:
        # Setting axis limits (You might need to adjust these based on your data)
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        ax.set_zlim([-1, 1])
    else:
        ax.set_xlim([keypoints[:, 0].min(), keypoints[:, 0].max()])
        ax.set_ylim([keypoints[:, 1].min(), keypoints[:, 1].max()])
        ax.set_zlim([keypoints[:, 2].min(), keypoints[:, 2].max()])

    # rotate the 3d plot x zero, y zero is at the bottom left
    #
    # set origin top left corner
    ax.invert_yaxis()
    current_view = ax.view_init()
    ax.view_init(elev=80, azim=-90, roll=0)

    # Plot keypoints
    for i in range(k):
        ax.scatter(keypoints[i, 0], keypoints[i, 1], keypoints[i, 2])
        # add number to each keypoint
        # ax.text(keypoints[i,0], keypoints[i,1], keypoints[i,2], '%s' % (str(keypoints_dict[i])), size=10, zorder=1, color='k')
    if M is not None:
        ax.scatter(M[0], M[1], M[2], c='r', marker='o')
        ax.text(M[0], M[1], M[2], 'CoM', size=10, zorder=1, color='k')

    return fig


import plotly.graph_objects as go
import webbrowser


def scatter_3d(data_list, output_html="", names=None, colors=None, size=5):
    if isinstance(size, int):
        size = [size] * len(data_list)
    if not isinstance(size, list):
        raise ValueError("size should be an integer or a list of integers")
    if colors is None:
        colors = ["blue", "red", "green", "yellow", "black", "purple", "orange", "pink", "brown", "cyan", "magenta",
                  "grey", "lightblue"]
    if names is None:
        names = [f"Data {i}" for i in range(len(data_list))]

    # Create figure
    fig = go.Figure()
    for j, data in enumerate(data_list):
        fig.add_trace(go.Scatter3d(x=data[0, :, 0], y=data[0, :, 1], z=data[0, :, 2],
                                   mode="markers", marker=dict(size=size[j], color=colors[j]),
                                   name=names[j]),
                      )
    # Combine frames alternately
    max_length = max([len(data) for data in data_list])

    # Define frames where both data and M are updated
    all_frames = []
    for i in range(max_length):
        frame_data = []
        for j, data in enumerate(data_list):
            if i < len(data):
                frame_data.append(go.Scatter3d(x=data[i, :, 0], y=data[i, :, 1], z=data[i, :, 2],
                                               mode="markers", marker=dict(size=size[j], color=colors[j]), )
                                  )

        all_frames.append(go.Frame(data=frame_data, name=f'frame{i}'))

    # Update frames
    fig.update(frames=all_frames)

    def frame_args(duration):
        return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
        }

    sliders = [
        {"pad": {"b": 10, "t": 60},
         "len": 0.9,
         "x": 0.1,
         "y": 0,

         "steps": [
             {"args": [[f.name], frame_args(0)],
              "label": str(k),
              "method": "animate",
              } for k, f in enumerate(fig.frames)
         ]
         }
    ]

    fig.update_layout(
        updatemenus=[{"buttons": [
            {
                "args": [None, frame_args(50)],
                "label": "Play",
                "method": "animate",
            },
            {
                "args": [[None], frame_args(0)],
                "label": "Pause",
                "method": "animate",
            }],
            "direction": "left",
            "pad": {"r": 10, "t": 70},
            "type": "buttons",
            "x": 0.1,
            "y": 0,
        }
        ],
        sliders=sliders,
        scene=dict(xaxis=dict(range=[-1.2, 1.2], autorange=False),
                   yaxis=dict(range=[-1.2, 1.2], autorange=False),
                   zaxis=dict(range=[-1.2, 1.2], autorange=False),
                   aspectmode="cube"

                   )
    )
    # invert the y axis (ax.invert_yaxis())

    # setup the initial view of the 3d plot so the top left corner is -1,-1
    fig.update_layout(scene=dict(camera=dict(up=dict(x=0, y=0, z=0),
                                             center=dict(x=0, y=0, z=0),
                                             eye=dict(x=1, y=-1, z=-2)
                                             )
                                 )
                      )
    # change to white theme
    fig.update_layout(template="plotly_white")

    # Save the figure as an HTML file
    if output_html:
        if not output_html.endswith(".html"):
            output_html += ".html"
        fig.write_html(output_html)
        webbrowser.open(output_html)

    return fig
