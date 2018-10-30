def get_top_wallets() -> list:
    lines = []
    with open("/var/www/data/top_wallets.txt") as file:
        for line in file:
            line = line.strip().split()[1].strip()
            lines.append(line)

    return lines


if __name__ == "__main__":
    print(get_top_wallets())
