import hou
import sys
import glob
sys.path.append("E:\Houdini\my_tools") #自作ライブラリCreatematerialNodes.py、UsdTools.pyのパスを通すための処理です。変更よろしくお願いします。
import CreateMaterialNodes
import UsdTools

# このコードをコピペしてHoudiniのPython Sorce Editer上で実行、またはshelfのツールとして登録してください。
# パスを適宜変更する必要があるのは5、12、19行目です

tex_folders_path = "E:/Houdini/textures_test"#テクスチャ画像フォルダをGUIで探す時の初期フォルダです、適切に変更よろしくお願いします。
extension = "png"

#Houdini内のノードの操作
stage = hou.node("/stage")
parm_prefix = '_reference'

# objで選択しているノードをsop importでstageに持っていく
for node in hou.selectedNodes():
    sop_name = node.name()
    sop_import = stage.createNode("sopimport", sop_name)
    sop_import.parm("soppath").set(node.path())

    # 現在選択しているノードとして設定
    sop_import.setDisplayFlag(True)
    sop_import.setCurrent(True, clear_all_selected = True)

    group = node.parmTemplateGroup()

    # パラメータの再設定
    parms = group.entries()
    for p in parms:
        if p.name().startswith(parm_prefix): group.remove(p)

    # 参照の確認
    node.setParmTemplateGroup( group )

    depNodes = node.dependents()
    num = 0
    for depNode in depNodes:
        parmName = parm_prefix+str(num)
        num += 1
        parm = hou.StringParmTemplate(parmName, "",1,string_type=hou.stringParmType.NodeReference)
        path = depNode.path()
        node.addSpareParmTuple(parm)
        node.parm(parmName).set(path)

    p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    p.setCurrentNode(sop_import)
    p.homeToSelection()

    # Material Library ノードを選択、もしなければ自動で作成する
    material_library = None
    for node in stage.children():
        if node.type().name() == "materiallibrary":
            material_library = node
            break

    if material_library is None:
        # materiallibraryタイプのノードが存在しない場合、新しく1つ作成
        material_library = stage.createNode("materiallibrary", "material_library")

    material_library_path = hou.ui.selectNode(relative_to_node=None, initial_node=None, node_type_filter=None, title="Select Material Library", width=0, height=0, multiple_select=False, custom_node_filter_callback=None)
    material_library = hou.node(material_library_path)

    if material_library.type().name() != "materiallibrary":
        hou.ui.displayMessage("materiallibraryノードがステージ内に存在しません。スクリプトを終了します。", severity=hou.severityType.Error)
        sys.exit()

    #ノードの接続
    material_library.setFirstInput(sop_import)
    material_library.moveToGoodPosition()

    # 現在選択しているノードとして設定
    material_library.setDisplayFlag(True)
    material_library.setCurrent(True, clear_all_selected = True)

    # sop_importからmeshレイヤーを取得
    mesh_layers = UsdTools.find_mesh_layers(material_library)
    mesh_layer_num = len(mesh_layers)

    #割り当てるマテリアルの数(Meshレイヤーの数)の設定
    material_library.parm("materials").set(mesh_layer_num)
    material_library.parm("matnode1").set("")

    # テクスチャ画像があるフォルダを指定する
    tex_folder_path = hou.ui.selectFile(file_type = hou.fileType.Directory, start_directory = tex_folders_path, title = "Select Texture Image Folder")
    
    # マテリアルの作成と割り当て
    for mesh_layer in mesh_layers: 
        mesh_layer_path = str(mesh_layer.GetPath())

        texture_files = glob.glob(tex_folder_path + "/*")
        texture_file_path_list = [file_path for file_path in texture_files if file_path.endswith("." + extension)]
        mtlx_material = CreateMaterialNodes.create_materialx_builder(sop_name, material_library, texture_file_path_list)

        # 作成したマテリアルの割り当て
        material_library.parm("matnode" + str(mesh_layer_num)).set(mtlx_material.path())
        material_library.parm("assign" + str(mesh_layer_num)).set(True)
        material_library.parm("geopath" + str(mesh_layer_num)).set(mesh_layer_path)

    material_library.layoutChildren()