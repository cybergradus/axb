import maya.cmds as mc
import rigtools.cleanArg

def makeIdentitySkinned(*arg):
    
    ns = ':_tmp_makeIdentitySkinned'
    arg = rigtools.cleanArg.cleanArg(arg)
    ns_init = mc.namespaceInfo(currentNamespace=True)
    
    #print('ns_init: '+ns_init)
    
    mc.namespace(setNamespace = ':')
    
    #print(arg)
    
    while mc.namespace(exists=ns):
        print(mc.namespace(removeNamespace=ns, deleteNamespaceContent=True))
    mc.namespace(addNamespace=ns)
    mc.namespace(setNamespace=ns)
    
    duplicates = set(mc.duplicate(arg))
    
    if duplicates:
        children = mc.listRelatives(duplicates, allDescendents=True, type='joint')
        
        if children:
            children = list(set(children))
            children += list(duplicates)
    
            mc.makeIdentity(children, apply=True, translate=True, rotate=True, scale=True)
    
            for i in children:
                for a in arg:
                    if i.split(':')[-1]==a.split(':')[-1]:
                        mc.copyAttr(i,a,values=True)
                
    #print(mc.namespace(exists=ns))
    mc.namespace(setNamespace=ns_init)
    mc.namespace(removeNamespace=ns,deleteNamespaceContent=True)