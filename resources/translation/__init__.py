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
            return "{{textkey=" + key + ";lang=" + lang + \
                ";unknown_io_error=true}}"
        return transget(key, "en")
    except ValueError:
        return "{{textkey=" + key + ";lang=" + lang + \
            ";malformed_translate_file=true}}"
    except Exception:
        return "{{textkey=" + key + ";lang=" + lang + \
            ";unknown_errror=true}}"
