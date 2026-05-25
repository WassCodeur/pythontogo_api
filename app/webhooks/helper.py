from urllib.parse import parse_qs, unquote_plus


def insert_nested(d, keys, value):
    """Insère une valeur dans un dictionnaire imbriqué en utilisant une liste de clés.
    Par exemple, insert_nested({}, ['data', 'invoice', 'items'], 'value')
    produira {'data': {'invoice': {'items': 'value'}}}
    """
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    d[keys[-1]] = value


def phpformat_to_json(data, result: dict):
    for key, values in data.items():
        value = values[0]

        # décoder les clés data[invoice][items]
        parts = []
        temp = ""

        for char in key:
            if char == "[":
                parts.append(temp)
                temp = ""
            elif char == "]":
                if temp:
                    parts.append(temp)
                temp = ""
            else:
                temp += char

        if temp:
            parts.append(temp)

        # nettoyage
        parts = [p for p in parts if p]

        insert_nested(result, parts, value)
