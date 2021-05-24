import re


def read_file(file_name):
    with open(file_name, "r") as fd:
        return fd.read()


def increase_version(file_content):
    result = ""

    found_version = False
    for line in file_content.splitlines():
        if found_version:
            found_version = False
            if line.strip().startswith("return"):
                version = re.findall("[0-9]+", line)
                version[2] = str(int(version[2]) + 1)
                line = "    return \"{0}\"".format(".".join(version))
            else:
                print("Error, could not change version")

        if line == "def get_version():":
            found_version = True

        result += "{0}\n".format(line)

    return result


def write_file(file_name, file_content):
    with open(file_name, "w") as fd:
        return fd.write(file_content)


def main():
    file_name = "../src/__main__.py"
    file_content = read_file(file_name)
    file_content = increase_version(file_content)
    write_file(file_name, file_content)


if __name__ == '__main__':
    main()

