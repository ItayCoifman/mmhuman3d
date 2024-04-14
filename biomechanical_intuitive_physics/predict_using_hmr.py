import demo.estimate_smplx as script
import os
import argparse
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    '--mesh_reg_config',
    type=str,
    default='configs/expose/expose.py',
    help='Config file for mesh regression')

parser.add_argument(
    '--det_cat_id',
    type=int,
    default=1,
    help='Category id for bounding box detection model')

parser.add_argument(
    '--det_config',
    default='demo/mmdetection_cfg/faster_rcnn_r50_fpn_coco.py',
    help='Config file for detection')

parser.add_argument(
    '--det_checkpoint',
    default='https://download.openmmlab.com/mmdetection/v2.0/faster_rcnn/'
            'faster_rcnn_r50_fpn_1x_coco/'
            'faster_rcnn_r50_fpn_1x_coco_20200130-047c8118.pth',
    help='Checkpoint file for detection')
parser.add_argument(
    '--tracking_config',
    default='demo/mmtracking_cfg/'
            'deepsort_faster-rcnn_fpn_4e_mot17-private-half.py',
    help='Config file for tracking')

parser.add_argument(
    '--body_model_dir',
    type=str,
    default='data/body_models/',
    help='Body models file path')

parser.add_argument(
    '--render_choice',
    type=str,
    default='hq',
    help='Render choice parameters')
parser.add_argument(
    '--palette', type=str, default='segmentation', help='Color theme')
parser.add_argument(
    '--bbox_thr',
    type=float,
    default=0.99,
    help='Bounding box score threshold')
parser.add_argument(
    '--draw_bbox',
    action='store_true',
    help='Draw a bbox for each detected instance')
parser.add_argument(
    '--smooth_type',
    type=str,
    default=None,
    help='Smooth the data through the specified type.'
         'Select in [oneeuro,savgol].')
parser.add_argument(
    '--device',
    choices=['cpu', 'cuda'],
    default='cuda',
    help='device used for testing')
args = parser.parse_args()

if __name__ == "__main__":
    os.chdir("D:\MMLAB\mmhuman3d")

    script.main(args=args,
                mesh_reg_checkpoint='data/pretrained_models/hrnet_hmr_expose_body-d7db2e53_20220708.pth',
                input_path="data/Samples/run/input.mp4",
                single_person_demo=True,
                multi_person_demo=False,
                output="data/Samples/run",
                show_path="data/Samples/run",

                )
    #    script.main(cam_id="data/Samples/run_0_comp", output="data/Samples/run_0_out.mp4")
