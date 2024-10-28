import maya.cmds as mc

message_attr_name = 'axb_message_twist'

def connect(arg):
    
    fk_control_end_joint = mc.listConnections(arg['primary_joints'][-1]+'.'+'axb_message_controlFK', type='joint')[0]
    print('axb.connect fk_control_end_joint:', fk_control_end_joint)
    
    print("arg['twists'] =", arg['twists'])
    for k in arg['twists']:
        print(k, arg['twists'][k])
        if not mc.ls(k+'.twist'):
            mc.addAttr(k, ln='twist', keyable=True, hidden=False, minValue=-1, maxValue=1, defaultValue=arg['twists'][k])
            
        
        aim_constraint = mc.aimConstraint(
            fk_control_end_joint,
            k,
            wuo=arg['primary_joints'][-1],
            wut='objectrotation',
            u=[0,0,1],
            wu=[0,0,1]
            )[0]
        print(aim_constraint)
        pair_blend = mc.createNode('pairBlend', n='pairBlend_'+k)
        mc.connectAttr(pair_blend+'.outRotateX', k+'.rx', force=True)
        mc.connectAttr(pair_blend+'.outRotateY', k+'.ry', force=True)
        mc.connectAttr(pair_blend+'.outRotateZ', k+'.rz', force=True)
        mc.connectAttr(aim_constraint+'.constraintRotate', pair_blend+'.inRotate2')
        mc.connectAttr(k+'.twist', pair_blend+'.weight')
        
        if not mc.ls(arg['primary_joints'][-1]+'.'+message_attr_name):
            mc.addAttr(arg['primary_joints'][-1], ln=message_attr_name, hidden=False, attributeType='message')
        mc.addAttr(pair_blend, ln=message_attr_name, hidden=False, attributeType='message')
        mc.connectAttr(arg['primary_joints'][-1]+'.'+message_attr_name, pair_blend+'.'+message_attr_name)
        
def delete(arg, debug=True):
    
    if debug: print('axb.twists.delete('+arg['primary_joints'][-1]+'), debug='+str(debug))
    message_connections = mc.listConnections(arg['primary_joints'][-1]+'.'+message_attr_name)
    mc.delete(message_connections)