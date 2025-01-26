import os
from pathlib import Path
from pxr import Usd

#Houdini内でUSDのレイヤーを探索してMeshレイヤーの名前を取得
def find_mesh_layers(target_node: str) -> list:
    # USD Stageを取得
    stage = target_node.stage()
    if not stage:
        raise ValueError(f"Failed to find USD Stage: {target_node}")

    # すべてのプリムを取得
    mesh_layers = [] 
    for prim in stage.Traverse():
        # プリムがGeomSubsetかどうかを確認
        if prim.GetTypeName() == "Mesh":
            mesh_layers.append(prim)

    return mesh_layers


#USDのレイヤーを探索してGeomSubsetレイヤーの名前を取得
def find_geomsubsets(file_path: str) -> list:
    # Stageを開く
    stage = Usd.Stage.Open(file_path)
    if not stage:
        raise ValueError(f"Failed to open USD file: {file_path}")

    # すべてのプリムを取得
    geomsubsets = [] 
    for prim in stage.Traverse():
        # プリムがGeomSubsetかどうかを確認
        if prim.GetTypeName() == "GeomSubset":
            geomsubsets.append(prim)

    return geomsubsets


#フォルダを探索して指定した名前のファイルを取得
def get_target_file(folder: str, target_name: str, extension: str) -> list:
    target_file_list = [file for file in os.listdir(folder) if target_name in file and file.endswith("." + extension)]
    return target_file_list

#USDのパスの表現をHoudini用に変更する、今後絶対パス、相対パスに対応したい
def change_usd_path_for_houdini(path: str, base_name: str) -> str:
    # Pathオブジェクトを作成
    p = Path(path)
    # パスをパーツに分割して最初の要素を変更
    parts = list(p.parts)
    parts[1] = base_name
    new_path = Path("/").joinpath(*parts[1:])

    new_path=str(new_path).replace("\\", "/")

    return new_path

#Meshレイヤーのパスの表現をHoudini用に変更する、今後絶対パス、相対パスに対応したい
def change_mesh_path_for_houdini(path: str, base_name: str) -> str:
    # Pathオブジェクトを作成
    p = Path(path)
    # パスをパーツに分割して最初の要素を変更
    parts = list(p.parts)
    parts[1] = base_name
    new_path = Path("/").joinpath(*parts[1:])

    new_path=str(new_path).replace("\\", "/")

    return new_path