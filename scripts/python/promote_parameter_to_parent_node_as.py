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
        parm_template = parm.parmTemplate()
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
        parm_group = parent_node.parmTemplateGroup()
        parent_parm_templates = parm_group.parmTemplates()
        all_parent_parm_names = []
        for parent_parm_name in parent_parm_templates:
            all_parent_parm_names.append(parent_parm_name.name())
        
        # CREATE NEW PARM TEMPLATE
        new_parm = parm.parmTemplate()
        new_parm_name = "{0}_{1}".format(node.name(), new_parm.name())
        new_parm.setName(new_parm_name)
        new_parm_label = ''
        
        # QUERY USER FOR NEW PARM LABEL
        do_continue, new_parm_label = hou.ui.readInput('Parameter Name:',buttons=('Cancel','OK'),default_choice=1)
        if do_continue:
            if new_parm_label:
                new_parm.setLabel(new_parm_label)

        # IF NEW PARM TEMPLATE NOT ALREADY ON PARENT NODE
        if new_parm_name not in all_parent_parm_names:
            
            # ADD NEW PARM TEMPLATE TO PARENT NODE
            parm_group.addParmTemplate(new_parm)
            parent_node.setParmTemplateGroup(parm_group)
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
        parm_group = parent_node.parmTemplateGroup()
        parent_parm_templates = parm_group.parmTemplates()
        all_parent_parm_names = []
        for parent_parm_name in parent_parm_templates:
            all_parent_parm_names.append(parent_parm_name.name())
            
        # CREATE NEW PARM TEMPLATE       
        new_parm = parms[0].parmTemplate()
        new_parm_name = "{0}_{1}" % (node.name(), new_parm.name())
        new_parm.setName(new_parm_name)
        
        # QUERY USER FOR NEW PARM LABEL
        do_continue, new_parm_label = hou.ui.readInput('Parameter Name:',buttons=('Cancel','OK'),default_choice=1)
        if do_continue:
            if new_parm_label:
                new_parm.setLabel(new_parm_label)        
        
        # IF NEW PARM TEMPLATE NOT ALREADY ON PARENT NODE            
        if new_parm_name not in all_parent_parm_names:
            
            # ADD NEW PARM TEMPLATE TO PARENT NODE    
            parm_group.addParmTemplate(new_parm)
            parent_node.setParmTemplateGroup(parm_group)
            parm_name = new_parm.name()
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

