

def get_uniprot_id(header):
    # header_items = header.split("|")
    # if len(header_items) > 1:
    #     return header_items[1].replace(">", "").replace(";", "|")

    return header.replace(">", "").replace(";", "|")




