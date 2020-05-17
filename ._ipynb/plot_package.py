import matplotlib.pyplot as plt


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


def plot_multi(x_1,y_1,x_2,y_2,x_3,y_3,x_axis_label,label1,label2,label3,title):
    fig, host = plt.subplots()
    fig.subplots_adjust(right=0.75)

    par1 = host.twinx()
    par2 = host.twinx()

    # Offset the right spine of par2.  The ticks and label have already been
    # placed on the right by twinx above.
    par2.spines["right"].set_position(("axes", 1.2))
    # Having been created by twinx, par2 has its frame off, so the line of its
    # detached spine is invisible.  First, activate the frame but make the patch
    # and spines invisible.
    make_patch_spines_invisible(par2)
    # Second, show the right spine.
    par2.spines["right"].set_visible(True)

    p1, = host.plot(x_1, y_1, "b-", label=label1)
    p2, = par1.plot(x_2, y_2, "r-", label=label2)
    p3, = par2.plot(x_3, y_3, "g-", label=label3)

#     host.set_xlim(0, 2)
#     host.set_ylim(0, 2)
#     par1.set_ylim(0, 4)
#     par2.set_ylim(1, 65)

    host.set_xlabel(x_axis_label)
    host.set_ylabel(label1)
    par1.set_ylabel(label2)
    par2.set_ylabel(label3)

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())

    tkw = dict(size=1, width=0.1)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2, p3]

    host.legend(lines, [l.get_label() for l in lines])
    plt.title(title)
    plt.show()
    
def plot_multi_separate(df,title):
    # Plot
    fig, axes = plt.subplots(1, 5, figsize=(10,2.5), dpi=100, sharex=True, sharey=True)
    colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:pink', 'tab:olive']

    for i, (ax, cut) in enumerate(zip(axes.flatten(), df.cut.unique())):
        x = df.loc[df.cut==cut, 'depth']
        ax.hist(x, alpha=0.5, bins=100, density=True, stacked=True, label=str(cut), color=colors[i])
        ax.set_title(cut)

    plt.suptitle(title, y=1.05, size=16)
    ax.set_xlim(50, 70); ax.set_ylim(0, 1);
    plt.tight_layout();