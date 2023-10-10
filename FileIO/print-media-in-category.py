"""Name-en-US: Print Media in Category
Description-en-US: Prints a list of all media assets belonging to a category ID to the console.

References:
https://plugincafe.maxon.net/topic/14214/get-asset-from-asset-browser-python/4

## License

MIT No Attribution

Copyright 2022 Donovan Keith

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Imports

from importlib.metadata import metadata
from multiprocessing.sharedctypes import Value
import c4d
import maxon
from typing import Optional

# Helper Functions


def FindAssetsByType(type) -> Optional[list[maxon.Asset]]:
    repository = maxon.AssetInterface.GetUserPrefsRepository()
    if not repository:
        raise RuntimeError("Unable to get User Repository.")

    # Find Assets:
    # https://developers.maxon.net/docs/Cinema4DPythonSDK/html/modules/maxon_generated/frameworks/asset/interface/maxon.AssetRepositoryInterface.html?highlight=findassets#maxon.AssetRepositoryInterface.FindAssets
    assets = repository.FindAssets(
        assetType=maxon.AssetTypes.File(),
        aid=maxon.Id(),
        version=maxon.Id(),
        findMode=maxon.ASSET_FIND_MODE.LATEST,
        receiver=None
    )

    return assets


def FindFileAssets():
    return FindAssetsByType(type=maxon.AssetTypes.File())


def GetAssetCategory(asset: maxon.AssetInterface):
    if not asset:
        raise ValueError("No asset provided.")

    meta_data = asset.GetMetaData()
    if not meta_data:
        raise ValueError("Unable to get asset meta data.")

    return meta_data.Get(maxon.ASSETMETADATA.Category)


def GetAssetName(asset: maxon.AssetDescription) -> Optional[str]:
    if not asset:
        return

    metadata: maxon.AssetMetaData = asset.GetMetaData()
    if metadata is None:
        return

    name: str = asset.GetMetaString(
        maxon.OBJECT.BASE.NAME, maxon.Resource.GetCurrentLanguage(), "")

    return name


def IsAssetAnImage(asset: maxon.AssetDescription) -> bool:
    if not asset:
        return

    metadata: maxon.AssetMetaData = asset.GetMetaData()
    if metadata is None:
        return

    sub_type: maxon.Id = metadata.Get(maxon.ASSETMETADATA.SubType, None)
    if (sub_type is None or maxon.InternedId(sub_type) != maxon.ASSETMETADATA.SubType_ENUM_MediaImage):
        return False

    return True


def GetCategoryIdFromUser() -> str:
    imperfections_id_string = "category@e780d216ed404547942dcbfcbbe009e5"

    category_id_string = c4d.gui.InputDialog(
        "Input Category ID", preset=imperfections_id_string)
    if not category_id_string:
        raise ValueError("Invalid ID String")

    return maxon.Id(category_id_string)


def main():
    category_id = GetCategoryIdFromUser()
    file_assets = FindFileAssets()
    imperfections_assets = [asset for asset in file_assets if (
        IsAssetAnImage(asset) and GetAssetCategory(asset) == category_id)]
    for asset in imperfections_assets:
        print(GetAssetName(asset))


if __name__ == "__main__":
    main()
