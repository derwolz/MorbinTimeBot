
def get_credentials():
    result ={}
    with open("./secrets.txt") as file:
        for line in file:
            _l = line.split("=")
            result[_l[0]] = _l[1][0:-1] # removes /n for new line
        return result

def write_winning_block(morbtime, jackpot):
    entry = f"{morbtime}:{jackpot}"
    with open("./winningblock.log", 'w') as file:
        file.write(entry)
def get_last_winning_block():
    with open("./winningblock.log") as file:
        lines = file.readlines()
        result = lines[-1].strip("\n").split(":")
        return result
def update_credentials():
    get_credentials()