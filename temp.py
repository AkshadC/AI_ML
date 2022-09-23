def dictwords(text_input):
    counts = dict ()
    words = text_input.split(" ")
    for word in words:
        if word in counts:
            counts [word]+=1
        else:
            counts [word] = 1
    new_dict = dict()
    for i in counts:
        if counts[i] > 1:
            new_dict[i] = counts[i]
    result = []
    sorted_d = dict(sorted(new_dict.items(), key=lambda item: item[0]))
    for i in sorted_d:
        result.append(i)
    if result is not None:
        return result
    else:
        return "NA"


if __name__ == "__main__":
    result = dictwords("cat batman latt matter cat matter cat")
    print(" ".join([str(res) for res in result]))