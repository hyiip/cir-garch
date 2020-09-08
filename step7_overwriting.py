from distutils.dir_util import copy_tree
from garch_utils.inputForm import inputForm


def overwriting(itemType):

    # copy graph
    fromDirectory = itemType + "/updating/plotly"
    toDirectory = itemType + "/web/plotly"
    copy_tree(fromDirectory, toDirectory)
    print("graph updated")

    # update
    fromDirectory = itemType + "/updating"
    toDirectory = itemType + "/original"
    copy_tree(fromDirectory, toDirectory)
    print("original  updated")
    return 0


if __name__ == '__main__':
    itemType, region = inputForm()
    overwriting(itemType + region)