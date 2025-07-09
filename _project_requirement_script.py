# Requirement used for the package used in the projectS

import subprocess

project_path = r"C:/Users/ayoba/PycharmProjects/AyobamiPythonProject/MyProject001"
pipreqs_path = r"C:/Users/ayoba/AppData/Roaming/Python/Python313/Scripts/pipreqs.exe"


subprocess.run([pipreqs_path, project_path])