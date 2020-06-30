import json

def transget(key, lang="en"):
    filename = 'resources/translation/translations/' + str(lang) + '.json'

    try:
        langfile = open(filename, mode='r', encoding='utf-8')
        langdata = json.load(langfile)
        if key in langdata:
            return langdata[key]
        else:
            if lang == "en":
                return "{{textkey=" + key +";lang=" + lang +"}}"
            else:
                return transget(key)
    except IOError:
        return transget(key)
        return "IO Error"
