
def get_credentials():
    result ={}
    with open("./secrets.txt") as file:
        for line in file:
            _l = line.split("=")
            result[_l[0]] = _l[1][0:-1] # removes /n for new line
        return result