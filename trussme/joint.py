import numpy as np


class Joint(object):

    def __init__(self, coordinates):
        # Save the joint id
        self.idx = -1

        # Coordinates of the joint
        self.coordinates = coordinates

        # Allowed translation in x, y, and z
        self.translation = np.ones([3, 1])

        # Loads
        self.loads = np.zeros([3, 1])

        # Store connected members
        self.members = []

        # Loads
        self.reactions = np.zeros([3, 1])

        # Loads
        self.deflections = np.zeros([3, 1])

    def free(self, d=3):
        self.translation = np.zeros([3, 1])
        # If 2d, add out of plane support
        if d is 2:
            self.translation[2] = 1

    def pinned(self, d=3):
        # Restrict all translation
        self.translation = np.ones([3, 1])

    def roller(self, axis='y', d=3):
        # Only support reaction along denotated axis
        self.translation = np.zeros([3, 1])
        self.translation[ord(axis)-120] = 1

        # If 2d, add out of plane support
        if d is 2:
            self.translation[2] = 1
