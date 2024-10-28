import maya.cmds as mc

message_attr_name = 'axb_message_controlFK'

def build_circle(arg, radius=10):
    
    print(arg)
    maker = mc.createNode('makeNurbCircle', n='makeNurbCircle_FK_'+arg)
    shape = mc.createNode('nurbsCurve', n='FK_'+arg+'_Shape')
    mc.connectAttr(maker+'.outputCurve', shape+'.create')
    transform = mc.listRelatives(shape, p=True)[0]
    print(transform)
    mc.select(None, replace=True)
    joint = mc.joint(name='FK_'+arg)
    mc.parent(shape, joint, relative=True, shape=True)
    mc.matchTransform(joint, transform)
    mc.delete(transform)
    print(joint, transform)
    
    mc.setAttr(maker+'.radius', radius)
    mc.setAttr(maker+'.normal', 1,0,0)
    mc.setAttr(joint+'.displayLocalAxis', 1)
    mc.setAttr(joint+'.displayHandle', 1)
    mc.matchTransform(joint, arg)
    if not mc.ls(arg+'.'+message_attr_name):
        mc.addAttr(arg, ln=message_attr_name, hidden=False, attributeType='message')
    mc.addAttr(joint, ln=message_attr_name, hidden=False, attributeType='message')
    mc.connectAttr(arg+'.'+message_attr_name, joint+'.'+message_attr_name)
    

    return joint, shape


def build(inputs):

    primary_joints = inputs['primary_joints']
    fk_control_radiuses = inputs['fk_control_radiuses']
    
    res = []
    shapes = []
    for i in primary_joints:
        parent = mc.listRelatives(i, p=True)
        build_circle_result = build_circle(i, radius=fk_control_radiuses[i])
        control = build_circle_result[0]
        shapes.append(build_circle_result[1])
        res.append(control)
        if parent:
            print('joint name:parent joint name = '+i+':'+parent[0])
            parent_control = mc.listConnections(parent[0]+'.'+message_attr_name)
            if parent_control:
                mc.parent(control, parent_control[0])
    

    for control in res[1:]:

        xformMatrix = mc.getAttr(control+'.xformMatrix')
        print(control, 'xformMatrix = ', xformMatrix)

        mc.setAttr(control+'.offsetParentMatrix', xformMatrix, type='matrix')
        mc.setAttr(control+'.offsetParentMatrix', lock=True)

        mc.xform(control, absolute=True, matrix=[1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])

        attributes_to_lock = [control + '.' + a for a in ['tx', 'ty', 'tz', 'sx', 'sy', 'sz']]
        for a in attributes_to_lock:
            mc.setAttr(a, lock=True)
    
    mc.makeIdentity(res[1:], apply=True, r=True)
    
    #just to make cicle shapes not to interfere with joints while pickwalk we'll do this:
    print('shapes:', shapes)    
    for shape in shapes[::-1]:

        mc.reorder(shape, back=True) 
    mc.delete(mc.listConnections(shapes, type='transformGeometry')) #clear unnecessary nodes on shapes
    
    parent_group = mc.group(n=res[0]+'_parent_group', empty=True)
    mc.addAttr(parent_group, ln=message_attr_name, hidden=False, attributeType='message')
    mc.connectAttr(inputs['primary_joints'][0]+'.'+message_attr_name, parent_group+'.'+message_attr_name)
    mc.matchTransform(parent_group, res[0])
    mc.parent(res[0], parent_group)
    mc.setAttr(res[0]+'.jointOrient', 0,0,0)
    mc.setAttr(res[0]+'.rotate', 0,0,0)
    mc.pointConstraint(inputs['primary_joints'][0], parent_group)
    attributes_to_lock = [res[0] + '.' + a for a in ['tx', 'ty', 'tz', 'sx', 'sy', 'sz']]
    for a in attributes_to_lock:
        mc.setAttr(a, lock=True)
    
    for control, primary_joint in zip(res, primary_joints):
        pair_blend = mc.createNode('pairBlend', n='pairBlend_'+control)
        mc.addAttr(pair_blend, ln=message_attr_name, hidden=False, attributeType='message')
        mc.connectAttr(primary_joint+'.'+message_attr_name, pair_blend+'.'+message_attr_name)
        
        orient_constraint = mc.orientConstraint(control, primary_joint)[0]
        mc.connectAttr(orient_constraint+'.constraintRotate', pair_blend+'.inRotate2')
        mc.connectAttr(pair_blend+'.outRotateX', primary_joint+'.rotateX', force=True)
        mc.connectAttr(pair_blend+'.outRotateY', primary_joint+'.rotateY', force=True)
        mc.connectAttr(pair_blend+'.outRotateZ', primary_joint+'.rotateZ', force=True)
        """
        mc.connectAttr(control+'.rotateX', pair_blend+'.inRotateX2')
        mc.connectAttr(control+'.rotateY', pair_blend+'.inRotateY2')
        mc.connectAttr(control+'.rotateZ', pair_blend+'.inRotateZ2')
        mc.connectAttr(pair_blend+'.outRotateX', primary_joint+'.rotateX')
        mc.connectAttr(pair_blend+'.outRotateY', primary_joint+'.rotateY')
        mc.connectAttr(pair_blend+'.outRotateZ', primary_joint+'.rotateZ')
        """
        
    mc.setAttr(res[-1]+'.rotateOrder', 5)
        
    return res


def delete(arg):
    
    for i in arg['primary_joints']:
        fk_control = mc.listConnections(i+'.'+message_attr_name) 
        mc.deleteAttr(i, at=message_attr_name)
        print(fk_control)
        mc.delete(fk_control)
        
        
