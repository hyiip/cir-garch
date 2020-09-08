def inputForm():
    region = ""
    print("input item type (stock/index/bond)")
    itemType = input().strip()
    if itemType == "stock":
        print("input item region eg.(US/HK)")
        region = input().strip()
    if "bond" in itemType:
        print("input item region eg.(GER)")
        region = input().strip()
    return itemType, region