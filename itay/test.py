from demo.webcam_demo import main
import os

if __name__ == "__main__":
    os.chdir("D:\MMLAB\mmhuman3d")
    main(cam_id="data/Samples/run_0_comp", output="data/Samples/run_0_out.mp4")
