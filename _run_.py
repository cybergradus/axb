print("""
!!!<<<
#please make sure you imported the module's path into Maya like this code below before importing the module itself:
import sys
sys.path.append('E:/scripts_from_Git') #example path for the module's parent path
!!!>>>
    """)
import sys
sys.path.append('C:/myGit/public')
import importlib
import axb

importlib.reload(axb)
axb.run()
"""
axb.delete_controls_fk()
"""


