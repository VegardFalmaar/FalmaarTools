import matplotlib as mpl
import matplotlib.pyplot as plt


def use_tex():
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "DejaVu Sans",
        "font.serif": ["Computer Modern"]}
    )
    # for e.g. \text command
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{amsmath}'


def set_ax_info(ax, xlabel, ylabel, title=None, zlabel=None, legend=True):
    """Write title and labels on an axis with the correct fontsizes.

    Args:
        ax (matplotlib.axis): the axis on which to display information
        xlabel (str): the desired label on the x-axis
        ylabel (str): the desired label on the y-axis
        title (str, optional): the desired title on the axis
            default: None
        zlabel (str, optional): the desired label on the z-axis for 3D-plots
            default: None
        legend (bool, optional): whether or not to add labels/legend
            default: True
    """
    if zlabel == None:
        ax.set_xlabel(xlabel, fontsize=20)
        ax.set_ylabel(ylabel, fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=15)
        # ax.ticklabel_format(style='plain')
    else:
        ax.set_xlabel(xlabel, fontsize=18)
        ax.set_ylabel(ylabel, fontsize=18)
        ax.set_zlabel(zlabel, fontsize=18)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.ticklabel_format(style='scientific', scilimits = (-2, 2))
    if title != None:
        ax.set_title(title, fontsize=20)
    if legend:
        ax.legend(fontsize=15)
