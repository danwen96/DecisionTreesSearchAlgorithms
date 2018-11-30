from copy import deepcopy

from anytree import Node, RenderTree

if __name__ == "__main__":
    # print("First commit")
    #
    # parent = Node("parent")
    #
    # child1 = Node("child1", parent=parent)
    # child2 = Node("child2", parent=parent)
    #
    # # for pre, fill, node in RenderTree(parent):
    # #     print("{0}{1}".format(pre, node.name))
    #
    # print(RenderTree(parent))

    a = [1,2,3,4]
    print(a)
    b = deepcopy(a)