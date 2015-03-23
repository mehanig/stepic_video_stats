def delete_entry_by_name(name, db_collection):
    print(name)
    try:
        if db_collection.find({'data.Name': name}).count() > 1:
            raise Exception("Name entries collapse. Names not unique at", db_collection, "data.Name:", name)
    except Exception as e:
        return e
    status = db_collection.remove({'data.Name': name})
    print('DELETED! ', status)
    return True