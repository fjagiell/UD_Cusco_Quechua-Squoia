import os
import subprocess


def main():
    IN_FILE = "test.conllu"
    subprocess.run(["python", "conversion.py", "-i", "conllu/"+IN_FILE,
                    "-o", "conversion_out/" + IN_FILE])
    subprocess.run(["grew", "transform", "-grs", "main.grs", "-i",
                    "conversion_out/" + IN_FILE, "-o", "grew_out/" + IN_FILE])
    subprocess.run(["python", "cleanup.py", "-all"])
    subprocess.run(["column", "-t", "cleanup_out/" + IN_FILE])


if __name__ == '__main__':
    main()
