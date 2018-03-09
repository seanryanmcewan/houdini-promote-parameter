# GET CURRENT NODE AND PARENT NODE
parms = kwargs["parms"]
node = parms[0].node()
parent_node = node.parent()

# HANDLE SOP SOLVERS' HIDDEN PARENTS
if parent_node.type().name() == 'sopsolver':
    parent_node = parent_node.parent().parent()
    
# DEFINE ALL ROOT DIRECTORIES    
top_level = ["/ch","/img","/obj","/out","/shop","/vex"]

# ONLY RUN IF THERE IS A PARENT TO PROMOTE TO
if parent_node.path() not in top_level:
    
    
    # IF PARM HAS SINGLE FIELD (I.E. NOT A TUPLE)
    if len(parms) == 1:
                
        # GET PARAMETER DETAILS
        set_expr = False
        parm = parms[0]
        parmTmp = parm.parmTemplate()
        parm_label = parm.parmTemplate().label()
        parm_name = parm.name()

        # IF PARM IS STRING
        if type(parm.parmTemplate()) is hou.StringParmTemplate:  
            
            # IF KEYFRAMED, GET EXPRESSION
            if parm.keyframes():
                parm_eval = parm.expression()
                set_expr = True
                
            # OTHERWISE GET UNEXPANDED STRING
            else:
                parm_eval = parm.unexpandedString()    
        
        # IF PARM IS NOT STRING AND HAS KEYFRAMES, GET EXPRESSION
        elif parm.keyframes():
            parm_eval = parm.expression()
            set_expr = True
        
        # OTHERWISE JUST GET VALUE OF PARAMETER
        else:
            parm_eval = parm.eval()
        
        # GET EXISTING PARM TEMPLATES
        parmGroup = parent_node.parmTemplateGroup()
        parentParmTemplates = parmGroup.parmTemplates()
        allParentParmNames = []
        for parent_parm_name in parentParmTemplates:
            allParentParmNames.append(parent_parm_name.name())
        
        # CREATE NEW PARM TEMPLATE
        newParm = parm.parmTemplate()
        new_parm_name = "%s_%s" % (node.name(), newParm.name())
        newParm.setName(new_parm_name)
        
        print new_parm_name
        
        print allParentParmNames

        # IF NEW PARM TEMPLATE NOT ALREADY ON PARENT NODE
        if new_parm_name not in allParentParmNames:
            
            print "ADDING"
            
            # ADD NEW PARM TEMPLATE TO PARENT NODE
            parmGroup.addParmTemplate(newParm)
            parent_node.setParmTemplateGroup(parmGroup)
            parent_parm = parent_node.parm(new_parm_name)
            
            # SET VALUE DIRECTLY
            if not set_expr:
                parent_parm.set(parm_eval)
                
            # SET EXPRESSIONS
            else:
                parent_parm.setExpression(parm_eval)
                parm.deleteAllKeyframes()
                
            # LINK TO PARENT PARM
            parm.set(parent_parm)
                
    # IF PARM HAS MULTIPLE FIELDS
    else:
        
        # GET EXISTING PARM TEMPLATES        
        parmGroup = parent_node.parmTemplateGroup()
        parentParmTemplates = parmGroup.parmTemplates()
        allParentParmNames = []
        for parent_parm_name in parentParmTemplates:
            allParentParmNames.append(parent_parm_name.name())
            
        # CREATE NEW PARM TEMPLATE       
        newParm = parms[0].parmTemplate()
        new_parm_name = "%s_%s" % (node.name(), newParm.name())
        newParm.setName(new_parm_name)
        
        # IF NEW PARM TEMPLATE NOT ALREADY ON PARENT NODE            
        if new_parm_name not in allParentParmNames:
            
            # ADD NEW PARM TEMPLATE TO PARENT NODE    
            parmGroup.addParmTemplate(newParm)
            parent_node.setParmTemplateGroup(parmGroup)
            parm_name = newParm.name()
            parent_parm = parent_node.parmTuple(new_parm_name)                

            # HANDLE EACH FIELD OF SOURCE PARAMETER
            for i in range(len(parms)):
                # GET PARAMETER DETAILS                
                set_expr = False
                child_parm = parms[i]
                
                # IF PARM IS STRING
                if type(child_parm.parmTemplate()) is hou.StringParmTemplate:  
                    
                    # IF KEYFRAMED, GET EXPRESSION                    
                    if child_parm.keyframes():
                        parm_eval = child_parm.expression()
                        set_expr = True
                        
                    # OTHERWISE, GET UNEXPANDED STRING
                    else:
                        parm_eval = child_parm.unexpandedString()    
                        
                # IF PARM IS NOT STRING AND HAS KEYFRAMES, GET EXPRESSION    
                elif child_parm.keyframes():
                    parm_eval = child_parm.expression()
                    set_expr = True
                    
                # OTHERWISE JUST GET VALUE OF PARAMETER                    
                else:
                    parm_eval = child_parm.eval()
                    
                # GET CURRENT INDEX OF PARENT PARM
                parent_child_parm = parent_parm.__getitem__(i)
                
                # SET VALUE DIRECTLY
                if not set_expr:
                    parent_child_parm.set(parm_eval)
                    
                # SET EXPRESSION
                else:
                    parent_child_parm.setExpression(parm_eval)
                    child_parm.deleteAllKeyframes()
                    
            # LINK TO PARENT PARM
            child_parm.set(parent_child_parm)

