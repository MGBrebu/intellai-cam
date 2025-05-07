### *** WSL2 + Tensorflow+CUDA BRANCH ***

# IntellAI_Cam
#### AI-Powered Surveillance Software

IntellAI_Cam is a CCTV-style camera system which uses [OpenCV](https://pypi.org/project/opencv-python/) and [Deepface](https://github.com/serengil/deepface) to detect and analyse human faces in real time. Analysis results are saved to an SQLite database and are easily searchable through the provided GUI, which also allows running the individual models and displays live analysis info as it is processed.

This system was created to assist in comparing the efficiency and accuracy differences between two possible face recognition and analysis implementations, and as such is not meant to be fully-featured nor used for any real workload. 

### Installation
> This is the **WSL2 + Tensorflow with CUDA support** branch. 

> TF with CUDA installation instructions are [here](https://www.tensorflow.org/install/pip#windows-wsl2). 

> WSL by default does not support USB cameras, the setup instructions I used to add support are [here](https://github.com/ctch3ng/Setting-up-Ubuntu-24.04-LTS-via-WSL-2-for-Google-s-Coral-USB-Accelerator/blob/main/WSL-Kernel-with-Web-Cam-Support.md). ***N.B.*** The resulting /dev/video0 ~ 1 cameras need regular user permissions to be accessed by non-sudo processes *(such as the venv IntellAi is using)*, you can do this using `chmod 777 /dev/video0` and `chmod 777 /dev/video1`.

> You **must** have ***Python 3.12*** installed and set as the current interpreter (for this project or globally). Python 3.13 has issues with the TensorFlow packages required.

1. Clone the repository

```
git clone https://github.com/your-username/your-project-name.git
cd your-project-name
```
2. Create a virtual environment (you can use Conda too)
```
python -m venv venv
venv\Scripts\activate
```
3. Install dependencies
```
pip install -r requirements.txt
```

### Usage
>The system can be used either through the provided GUI utility, or an individual model can be run manually.

**Recommended** | Run the GUI
```
python intellai_gui.py
```
Run an individual model
```
python intellai_single.py
OR
python intellai_hybrid.py
```


-----
Authored By **Mario G. Brebu**

`Created and submitted as a final year project and thesis to Technological University Dublin in partial fulfilment of the requirements for the degree of Bachelor of Science in Computing in Digital Forensics & Cyber Security`
