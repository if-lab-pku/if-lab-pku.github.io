import fire

def matcher(text: str):
    i = 0
    buffer = ""
    ret = []
    tmp = {}
    state = 0
    while i < len(text):
        if state == 0:
            if text[i] == "\\":
                state = 1
                ret.append({"cmd": None, "content": buffer})
                buffer = ""
            else:
                buffer += text[i]
        elif state == 1:
            if text[i] == "{":
                state = 2
                tmp["cmd"] = buffer
                buffer = ""
            else:
                buffer += text[i]
        elif state == 2:
            if text[i] == "}":
                state = 0
                tmp["content"] = buffer
                buffer = ""
                ret.append(tmp.copy())
                tmp = {}
            else:
                buffer += text[i]
        i += 1
    return ret

def main(file: str):
    with open(file, "r") as f:
        lines = f.readlines()
    pubs: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith("\\makebox"):
            _lines = []
            while True:
                i += 1
                if i >= len(lines):
                    break
                if lines[i].startswith("\\makebox"):
                    break
                j = 0
                while j < len(lines[i]) - 1:
                    if lines[i][j] == "%" and (j == 0 or lines[i][j-1] != "\\"):
                        break
                    j += 1
                buffer = lines[i][:j].strip()
                if len(buffer) != 0:
                    _lines.append(buffer)
            pubs.append(" ".join(_lines).strip())
        else:
            i += 1
    print(len(pubs))
    import re
    for pub in pubs:
        pub = pub.replace("``", "“")
        pub = pub.replace("''", "”")
        pub = pub.replace("\\textquotesingle", "'")
        pub = pub.replace("\\@", "")
        pub = re.sub(r"\$\s*\^\\dagger\s*\$", "<sup>†</sup>", pub)
        pub = re.sub(r"\$\s*\^\\circ\s*\$", "<sup>◦</sup>", pub)
        pub = re.sub(r"\$\s*\^\\ast\s*\$", "<sup>*</sup>", pub)
        pub = re.sub(r"\$\s*\^\\ast\s*\$", "<sup>*</sup>", pub)
        pub = re.sub(r"\$\s*\\sim\s*\$", "~", pub)
        buffer = ""
        for shit in matcher(pub):
            match shit["cmd"]:
                case None:
                    buffer += shit["content"]
                case "textsl":
                    buffer += "<em>"+shit["content"]+"</em>"
                case "textbf":
                    buffer += "<strong>"+shit["content"]+"</strong>"
                case "vspace":
                    pass
                case "hspace":
                    pass
                case "stepcounter":
                    pass
                case _:
                    print(shit)
                    assert False
        print(buffer)

if __name__ == "__main__":
    fire.Fire(main)
