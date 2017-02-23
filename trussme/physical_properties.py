# Gravitational constant for computing weight from mass
g = [0, -9806.65, 0]


# Material properties
materials = {"A36":     {"rho": 7800,
                         "E":   200*pow(10, 9),
                         "Fy":  250*pow(10, 6)},
             "A992":    {"rho": 7800,
                         "E":   200*pow(10, 9),
                         "Fy":  345*pow(10, 6)},
             "6061_T6": {"rho": 2700,
                         "E":   68.9*pow(10, 9),
                         "Fy":  276*pow(10, 6)},
             "zero_mat": {"rho": 0.0001,
                          "E":   200*pow(10, 9),
                          "Fy":  345*pow(10, 6)},
             "S460":     {"rho": 7.85*pow(10, -9),
                          "E":   210000,
                          "Fy":  345},
             "S460_L4":  {"rho": 1.9997*pow(10, -8), # t/mm^3
                          "E":   210000, # N/mm^2 = MPa
                          "Fy":  345},
             "S460_L3":  {"rho": 1.3656*pow(10, -8),
                          "E":   210000,
                          "Fy":  345},
             "S460_L2":  {"rho": 1.5853*pow(10, -8),
                          "E":   210000,
                          "Fy":  345},
             "S460_L1":  {"rho": 1.3556*pow(10, -8),
                          "E":   210000,
                          "Fy":  345},}


# Checks to see if material name is valid
def valid_member_name(name):
    if name in materials.keys():
        return True
    else:
        return False