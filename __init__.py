print('Hi, axb! I am Anton "cybergradus" Pleshkov')

import importlib
import maya.cmds as mc
import axb.makeIdentitySkinned
import axb.controls_fk
import axb.twists
import axb.controls_ik

[importlib.reload(i) for i in [
    axb.controls_fk,
    axb.twists,
    axb.controls_ik
]]

#print('imported: ' + str(rigtools.makeIdentitySkinned))

arm_left_joints = mc.listRelatives('LeftArm', ad=True)+['LeftArm']
arm_left_primary_joints = ['LeftArm', 'LeftForeArm', 'LeftHand'] #hierarchical order in this list is mandatory
fk_control_radiuses = {'LeftArm':12, 'LeftForeArm':8, 'LeftHand':6}

arm_left_twists = {'LeafLeftForeArmRoll1':0.25,
   'LeafLeftForeArmRoll2':0.5,
   'LeafLeftForeArmRoll3':0.75,
   'LeafLeftForeArmRoll4':1.0}

arm_left = {'joints':arm_left_joints,
    'primary_joints':arm_left_primary_joints,
    'fk_control_radiuses':fk_control_radiuses,
    'twists':arm_left_twists}

def run(*arg, keyed_controls_fk=True):
    
    if not arg: arg = arm_left

    axb.makeIdentitySkinned.makeIdentitySkinned(arg['joints'])

    primary_controls_fk = axb.controls_fk.build(arg) 
    axb.twists.connect(arg)
    axb.controls_ik.build(arg)
    if keyed_controls_fk: mc.setKeyframe(primary_controls_fk, at='rotate')
    
def delete_controls_fk(*arg):
    
    if not arg: arg = arm_left
    
    axb.controls_fk.delete(arg)
    axb.twists.delete(arg)
    