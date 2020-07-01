import json


def transget(key, lang="en"):
    filename = 'resources/translation/translations/' + str(lang) + '.json'

    try:
        langfile = open(filename, mode='r', encoding='utf-8')
        langdata = json.load(langfile)
        if key in langdata:
            langfile.close()
            return langdata[key]
        else:
            if lang == "en":
                langfile.close()
                return "{{textkey=" + key + ";lang=" + lang + "}}"
            else:
                langfile.close()
                return transget(key, "en")
    except IOError:
        if lang == "en":
            return "IO Error"
        return transget(key, "en")
    except Exception:
        print("UNKNOWN ERROR UFF!")
