def buildStatus(names):
    """
    creates status array
    """
    status = [[0, "Downloading:"]]
    for name in names:
        status.append([name, 0])
    return status