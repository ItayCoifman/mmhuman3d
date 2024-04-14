import pandas as pd
import numpy as np



keypoints_dict = {0: "right ankle", 1: "right knee", 2: "right hip", 3: "left hip", 4: "left knee", 5: "left ankle",
                  6: "right wrist", 7: "right elbow", 8: "right shoulder", 9: "left shoulder", 10: "left elbow",
                  11: "left wrist", 12: "neck", 13: "head top"}


class Biomechanics(object):
    anthropometric_coefficients = {
        "Pelvis": {"CoM": 0.5, "Mass": 0.142, "Radius of gyration": 0.31, "proximal": "right hip",
                   "distal": "left hip"},
        "Thorax_a": {"CoM": 0.63, "Mass": 0.355 / 2, "Radius of gyration": 0.31, "proximal": "left hip",
                     "distal": "neck"},
        "Thorax_b": {"CoM": 0.63, "Mass": 0.355 / 2, "Radius of gyration": 0.31, "proximal": "right hip",
                     "distal": "neck"},
        "Head": {"CoM": 0.5, "Mass": 0.081, "Radius of gyration": 1.116, "proximal": "neck", "distal": "head top"},
        "Right Femur": {"CoM": 0.567, "Mass": 0.1, "Radius of gyration": 0.54, "proximal": "right hip",
                        "distal": "right knee"},
        "Left Femur": {"CoM": 0.567, "Mass": 0.1, "Radius of gyration": 0.54, "proximal": "left hip",
                       "distal": "left knee"},
        "Right Tibia": {"CoM": 0.567, "Mass": 0.0465, "Radius of gyration": 0.528, "proximal": "right knee",
                        "distal": "right ankle"},
        "Left Tibia": {"CoM": 0.567, "Mass": 0.0465, "Radius of gyration": 0.528, "proximal": "left knee",
                       "distal": "left ankle"},
        "Right Humorous": {"CoM": 0.564, "Mass": 0.028, "Radius of gyration": 0.542, "proximal": "right shoulder",
                           "distal": "right elbow"},
        "Left Humorous": {"CoM": 0.564, "Mass": 0.028, "Radius of gyration": 0.542, "proximal": "left shoulder",
                          "distal": "left elbow"},
        "Right Radius": {"CoM": 0.57, "Mass": 0.016, "Radius of gyration": 0.526, "proximal": "right elbow",
                         "distal": "right wrist"},
        "Left Radius": {"CoM": 0.57, "Mass": 0.016, "Radius of gyration": 0.526, "proximal": "left elbow",
                        "distal": "left wrist"},
        # "Foot": {"CoM": 0.5, "Mass": 0.0145, "Radius of gyration": 0.69, "proximal": "L5/S1" , "distal": "Hip"},
        # "Hand": {"CoM": 0.6205, "Mass": 0.006, "Radius of gyration": 0.44, "proximal": "L5/S1" , "distal": "Hip"},
    }

    def __init__(self, keypoints_dict=keypoints_dict):
        self.keypoints_dict = keypoints_dict
        self.segments_mat = self.create_segments_mat(keypoints_dict)

    def create_segments_mat(self, keypoints_dict):
        """

        Args:
            keypoints_dict: a dictionary that maps the index of the keypoints to the name of the keypoints

        Returns:
            segments_mat: a pandas dataframe that contains the anthropometric coefficients of each segment
        """
        segments_mat = pd.DataFrame(self.anthropometric_coefficients).T
        # redistribute the Mass so the sum will be 1
        segments_mat['Mass'] = segments_mat['Mass'] / segments_mat['Mass'].sum()
        # add to each segment the index of the proximal and distal segment from the keypoints_dict
        segments_mat['proximal_idx'] = segments_mat['proximal'].apply(
            lambda x: list(keypoints_dict.keys())[list(keypoints_dict.values()).index(x)])
        segments_mat['distal_idx'] = segments_mat['distal'].apply(
            lambda x: list(keypoints_dict.keys())[list(keypoints_dict.values()).index(x)])
        return segments_mat

    def compute_CoM(self, keypoints):
        l = self.segments_mat.CoM.values
        w = self.segments_mat.Mass.values

        proximal, distal = keypoints[:, self.segments_mat.proximal_idx.values, :], keypoints[:, self.segments_mat.distal_idx.values,
                                                                              :]
        p_com = (proximal * l[:, None] + distal * (1 - l)[:, None])
        # M is the matrix that average over the keypoints using the weights (w)
        M = np.sum(p_com * w[None, :, None], axis=1)

        return M






