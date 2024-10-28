import maya.cmds as mc

def build(arg, debug=True):
    
    message_attr_name = 'axb_message_controlIK'
    
    if debug: print("axb.controls_ik.build(arg['primary_joints']):"+str(arg['primary_joints']))
    
    pv_loc = mc.spaceLocator(n='IK_'+arg['primary_joints'][0]+'_pole_vector')[0]
    mc.setAttr(pv_loc+'Shape.localScale', 4,4,4)
    mc.matchTransform(pv_loc, arg['primary_joints'][1])
    mc.move(0,0,-25, pv_loc, r=True, wd=True, os=True)
    
    start_joint = mc.listConnections(arg['primary_joints'][0]+'.axb_message_controlFK', type='joint')[0]
    end_joint = mc.listConnections(arg['primary_joints'][-1]+'.axb_message_controlFK', type='joint')[0]
    
    ik_handle = mc.ikHandle(
        startJoint=start_joint,
        endEffector=end_joint,
        n='IK_'+arg['primary_joints'][0]+'_handle',
        snapHandleFlagToggle=False
        )
    if debug: print(ik_handle)
    mc.poleVectorConstraint(pv_loc, ik_handle[0])
    ik_loc = mc.spaceLocator(n='IK_'+arg['primary_joints'][-1])[0]
    mc.setAttr(ik_loc+'Shape.localScale', 8,8,8)
    mc.matchTransform([ik_loc, ik_handle[0]], arg['primary_joints'][-1])
    mc.parent(ik_handle[0], ik_loc)
    
    mc.addAttr(ik_loc, ln='ikBlend', hidden=False, keyable=True, minValue=0, maxValue=1, defaultValue=1)
    mc.connectAttr(ik_loc+'.ikBlend', ik_handle[0]+'.ikBlend')
    
    oc = mc.orientConstraint(ik_loc, end_joint)[0]
    mc.setAttr(oc+'.interpType', 2)
    pair_blend = mc.createNode('pairBlend', n='pairBlend_'+ik_loc)
    mc.connectAttr(oc+'.constraintRotate', pair_blend+'.inRotate2')
    mc.connectAttr(pair_blend+'.outRotateX', end_joint+'.rotateX', force=True)
    mc.connectAttr(pair_blend+'.outRotateY', end_joint+'.rotateY', force=True)
    mc.connectAttr(pair_blend+'.outRotateZ', end_joint+'.rotateZ', force=True)
    mc.connectAttr(ik_handle[0]+'.ikBlend', pair_blend+'.weight')
    mc.addAttr(pair_blend, ln=message_attr_name, hidden=False, attributeType='message')
    mc.addAttr(arg['primary_joints'][-1], ln=message_attr_name, hidden=False, attributeType='message')
    mc.connectAttr(arg['primary_joints'][-1]+'.'+message_attr_name, pair_blend+'.'+message_attr_name)
    
    ik_parent_group = mc.group(n='IK_'+arg['primary_joints'][0]+'_parent_group', empty=True)
    mc.matchTransform(ik_parent_group, arg['primary_joints'][0])
    mc.parent([ik_loc, pv_loc], ik_parent_group)
    
    xformMatrix = mc.getAttr(ik_loc+'.xformMatrix')
    mc.setAttr(ik_loc+'.offsetParentMatrix', xformMatrix, type='matrix')
    mc.setAttr(ik_loc+'.offsetParentMatrix', lock=True)
    mc.xform(ik_loc, absolute=True, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])

    xformMatrix = mc.getAttr(pv_loc+'.xformMatrix')
    mc.setAttr(pv_loc+'.offsetParentMatrix', xformMatrix, type='matrix')
    mc.setAttr(pv_loc+'.offsetParentMatrix', lock=True)
    mc.xform(pv_loc, absolute=True, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])
    