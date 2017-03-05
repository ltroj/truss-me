import numpy as np


def the_forces(truss_info):
    tj = np.zeros([3, np.size(truss_info["connections"], axis=1)])
    w = np.array([np.size(truss_info["reactions"], axis=0),
                  np.size(truss_info["reactions"], axis=1)])
    dof = np.zeros([3*w[1], 3*w[1]])
    deflections = np.ones(w)
    deflections -= truss_info["reactions"]

    # This identifies joints that can be loaded
    ff = np.where(deflections.T.flat == 1)[0]

    # Build the global stiffness matrix
    for i in range(np.size(truss_info["connections"], axis=1)):
        ends = truss_info["connections"][:, i]
        length_vector = truss_info["coordinates"][:, ends[1]] \
            - truss_info["coordinates"][:, ends[0]]
        length = np.linalg.norm(length_vector)
        direction = length_vector/length
        d2 = np.outer(direction, direction)
        ea_over_l = truss_info["elastic_modulus"][i]*truss_info["area"][i]\
            / length
        ss = ea_over_l*np.concatenate((np.concatenate((d2, -d2), axis=1),
                                       np.concatenate((-d2, d2), axis=1)),
                                       axis=0)
        tj[:, i] = ea_over_l*direction
        e = list(range((3*ends[0]), (3*ends[0] + 3))) \
            + list(range((3*ends[1]), (3*ends[1] + 3)))
        for ii in range(6):
            for j in range(6):
                dof[e[ii], e[j]] += ss[ii, j]

    SSff = np.zeros([len(ff), len(ff)])
    for i in range(len(ff)):
        for j in range(len(ff)):
            SSff[i, j] = dof[ff[i], ff[j]]

    flat_loads = truss_info["loads"].T.flat[ff]
    flat_deflections = np.linalg.solve(SSff, flat_loads)

    ff = np.where(deflections.T == 1)
    for i in range(len(ff[0])):
        deflections[ff[1][i], ff[0][i]] = flat_deflections[i]
    forces = np.sum(np.multiply(
        tj, deflections[:, truss_info["connections"][1, :]] -
        deflections[:, truss_info["connections"][0, :]]), axis=0)

    # Check the condition number, and warn the user if it is out of range
    cond = np.linalg.cond(SSff)

    # Compute the reactions
    # Important bugfix added: R=KU-F, this means nodal loads must be subtracted
    # from reactions. This bug already exists at the original matlab script.
    # Please see comment from Chris Jobes at
    # https://de.mathworks.com/matlabcentral/fileexchange/14313-truss-analysis
    reactions = np.sum(dof*deflections.T.flat[:], axis=1)\
        .reshape([w[1], w[0]]).T - truss_info["loads"]

    return forces, deflections, reactions, cond
