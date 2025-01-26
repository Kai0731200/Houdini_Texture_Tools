import hou
import os

def setting_materialx_subnet(material_library: hou.Node, node_name: str) -> hou.Node:
    INHERIT_PARM_EXPRESSION = '''
    n = hou.pwd()
    n_hasFlag = n.isMaterialFlagSet()
    i = n.evalParm('inherit_ctrl')
    r = 'none'
    if i == 1 or (n_hasFlag and i == 2):
        r = 'inherit'
    return r
    '''

    subnetNode = material_library.createNode("subnet", node_name)
    subnetNode.moveToGoodPosition()
    subnetNode.setMaterialFlag(True)                  

    parameters = subnetNode.parmTemplateGroup()

    newParm_hidingFolder = hou.FolderParmTemplate("mtlxBuilder","MaterialX Builder",folder_type=hou.folderType.Collapsible)
    control_parm_pt = hou.IntParmTemplate('inherit_ctrl','Inherit from Class', 
                        num_components=1, default_value=(2,), 
                        menu_items=(['0','1','2']),
                        menu_labels=(['Never','Always','Material Flag']))

    newParam_tabMenu = hou.StringParmTemplate("tabmenumask", "Tab Menu Mask", 1, default_value=["MaterialX parameter constant collect null genericshader subnet subnetconnector suboutput subinput"])
    class_path_pt = hou.properties.parmTemplate('vopui', 'shader_referencetype')
    class_path_pt.setLabel('Class Arc')
    class_path_pt.setDefaultExpressionLanguage((hou.scriptLanguage.Python,))
    class_path_pt.setDefaultExpression((INHERIT_PARM_EXPRESSION,))   

    ref_type_pt = hou.properties.parmTemplate('vopui', 'shader_baseprimpath')
    ref_type_pt.setDefaultValue(['/__class_mtl__/`$OS`'])
    ref_type_pt.setLabel('Class Prim Path')               

    newParm_hidingFolder.addParmTemplate(newParam_tabMenu)
    newParm_hidingFolder.addParmTemplate(control_parm_pt)  
    newParm_hidingFolder.addParmTemplate(class_path_pt)    
    newParm_hidingFolder.addParmTemplate(ref_type_pt)             

    parameters.append(newParm_hidingFolder)
    subnetNode.setParmTemplateGroup(parameters)

    return subnetNode

def create_materialx_builder(layer_name: str, material_library: hou.Node, texture_file_path_list: list) -> hou.Node:
    # MaterialX Builder ノードを作成
    mtlx_material = setting_materialx_subnet(material_library,layer_name + "_mtlx_material")
    mtlx_material.setPosition(hou.Vector2(-2.5, 0))

    # Subinput ノードを作成
    #subinput = mtlx_material.createNode("subinput", "inputs")

    # Standard Surface Material ノードを作成
    mtlx_standard_surface = mtlx_material.createNode("mtlxstandard_surface", "mtlxstandard_surface")
    mtlx_standard_surface.setPosition(hou.Vector2(-0.3, 0))

    # Displacement Material ノードを作成
    mtlx_displacement = mtlx_material.createNode("mtlxdisplacement", "mtlxdisplacement")
    mtlx_displacement.setPosition(hou.Vector2(-0.3, -2.4))
    mtlx_displacement.parm("scale").set(0.001)

    # Surface Output ノードを作成
    surface_output = mtlx_material.createNode("subnetconnector", "surface_output")
    surface_output.setPosition(hou.Vector2(2.5, 0))
    surface_output.parm("connectorkind").set("output")
    surface_output.parm("parmname").set("surface")
    surface_output.parm("parmlabel").set("Surface")
    surface_output.parm("parmtype").set("surface")

    # Displacement Output ノードを作成
    displacement_output = mtlx_material.createNode("subnetconnector", "displacement_output")
    displacement_output.setPosition(hou.Vector2(2.5, -2.4))
    displacement_output.parm("connectorkind").set("output")
    displacement_output.parm("parmname").set("displacement")
    displacement_output.parm("parmlabel").set("Displacement")
    displacement_output.parm("parmtype").set("displacement")

    # 接続
    surface_output.setInput(0, mtlx_standard_surface)  # Standard Surface を Surface Output に接続
    displacement_output.setInput(0, mtlx_displacement)  # Displacement を Displacement Output に接続

    # UVノードの作成
    uv_node = mtlx_material.createNode("mtlxgeompropvalue", "UV")
    uv_node.parm("signature").set("vector2")
    uv_node.parm("geomprop").set("st")

    for texture_path in texture_file_path_list:
        texture_image = os.path.basename(texture_path).lower()
        
        # テクスチャを読み込むノードを作成
        texture_node = mtlx_material.createNode("mtlxtiledimage")

        # ノードのパラメータ設定と接続
        texture_node.parm("file").set(texture_path)
        texture_node.setInput(2, uv_node)
        
        if  "base_color" in texture_image:
            #ノードの名前を設定
            texture_node.setName("Base_Color")
            # 出力の型の設定
            texture_node.parm("signature").set("color3")
            # 接続
            mtlx_standard_surface.setInput(1, texture_node, 0)

        elif  "roughness" in texture_image:
            #ノードの名前を設定
            texture_node.setName("Roughness")
            # 出力の型の設定
            texture_node.parm("signature").set("float")
            # 接続
            mtlx_standard_surface.setInput(2, texture_node, 0)

        elif  "metalness" in texture_image:
            #ノードの名前を設定
            texture_node.setName("Metalness")
            # 出力の型の設定
            texture_node.parm("signature").set("float")
            # 接続
            mtlx_standard_surface.setInput(3, texture_node, 0)

        elif  "normal" in texture_image:
            #ノードの名前を設定
            texture_node.setName("Normal")
            # 出力の型の設定
            texture_node.parm("signature").set("vector3")
            # 接続
            mtlx_standard_surface.setInput(40, texture_node, 0)

        elif  "displacement" in texture_image:
            #ノードの名前を設定
            texture_node.setName("Displacement")
            # 出力の型の設定
            texture_node.parm("signature").set("float")
            # 接続
            mtlx_displacement.setInput(0, texture_node, 0)

        if "sRGB".lower() in texture_image:
            texture_node.parm("filecolorspace").set("srgb_texture")
        else:
            texture_node.parm("filecolorspace").set("Raw")
    # 作成したノードのレイアウトを調整
    mtlx_material.layoutChildren()

    return mtlx_material