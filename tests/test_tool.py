import json
import os
import re

from implementations.blackbox_s1s2 import BlackboxS1S2
from implementations.file_json import FileJSON
from implementations.blackbox_makefile import BlackboxMakefile
from implementations.file_makefile import FileMakefile


def create_test_jsons(workdir: str):
    # Creating 5 tests for 1000 and 5 for 10000 elements
    testsets_1000: list[list] = [list(range(1000)) for _ in range(5)]
    testsets_10000: list[list] = [list(range(10000)) for _ in range(5)]

    # 1000 elements 5 times.
    # 0: S1=1, S2=2
    # 1: S1=1, S2=500
    # 2: S1=1, S2=999
    # 3: S1=500, S2=600
    # 4: S1=550, S2=750
    testsets_1000[0][1] = testsets_1000[1][1] = testsets_1000[2][1] = testsets_1000[3][500] = testsets_1000[4][
        550] = "S1"
    testsets_1000[0][2] = testsets_1000[1][500] = testsets_1000[2][999] = testsets_1000[3][600] = testsets_1000[4][
        750] = "S2"

    # 10000 elements 5 times.
    # 0: S1=1, S2=1000
    # 1: S1=1, S2=5000
    # 2: S1=1, S2=9999
    # 3: S1=5000, S2=6000
    # 4: S1=7000, S2=7575
    testsets_10000[0][1] = testsets_10000[1][1] = testsets_10000[2][1] = testsets_10000[3][5000] = testsets_10000[4][
        7000] = "S1"
    testsets_10000[0][1000] = testsets_10000[1][5000] = testsets_10000[2][9999] = testsets_10000[3][6000] = \
        testsets_10000[4][7575] = "S2"

    print("Creating files: ")
    for i in range(5):
        with open(f"{workdir}/temp_out_1000_{i}.json", 'w') as out_f:
            print(f"{workdir}/temp_out_1000_{i}.json")
            json.dump(testsets_1000[i], out_f)
        with open(f"{workdir}/temp_out_10000_{i}.json", 'w') as out_f:
            json.dump(testsets_10000[i], out_f)
            print(f"{workdir}/temp_out_10000_{i}.json")
    print("Files were created.")


def clean_test_jsons(workdir: str):
    print("Removing files: ")
    for i in range(5):
        os.remove(f"{workdir}/temp_out_1000_{i}.json")
        print(f"{workdir}/temp_out_1000_{i}.json")
        os.remove(f"{workdir}/temp_out_10000_{i}.json")
        print(f"{workdir}/temp_out_10000_{i}.json")
    print("Files were removed.")


def test_file_json(workdir: str):
    print("Creating FileJSON objects from temp_out_1000_0.json and temp_out_10000_0.json")
    json_file_1000_0 = FileJSON('temp_out_1000_0.json', workdir)
    json_file_10000_0 = FileJSON('temp_out_10000_0.json', workdir)
    outfile_1000 = json_file_1000_0.create_file(list(range(1000)))
    outfile_10000 = json_file_10000_0.create_file(list(range(10000)))
    print(f"Created {outfile_1000}\n and {outfile_10000} with create_file functionality")

    with open(f"{workdir}/temp_out_1000_0.json") as original:
        with open(outfile_1000) as newly_created:
            if json.load(original) != json.load(newly_created):
                raise Exception("Created file by the json_file_1000_0 does not match the original")
            else:
                print(f"{outfile_1000} and temp_out_1000_0.json are matching!")

    with open(f"{workdir}/temp_out_10000_0.json") as original:
        with open(outfile_10000) as newly_created:
            if json.load(original) != json.load(newly_created):
                raise Exception("Created file by the json_file_10000_0 does not match the original")
            else:
                print(f"{outfile_10000} and temp_out_10000_0.json are matching!")

    print("Checking sizes...")
    assert (json_file_1000_0.get_original_size() == 1000)
    assert (json_file_10000_0.get_original_size() == 10000)
    print("Sizes are correct!")

    print("Removing ", outfile_1000)
    os.remove(outfile_1000)
    print("Removing ", outfile_10000)
    os.remove(outfile_10000)

    # in original json 1000 0 S1 is 1, S2 is 2
    # if indexes are reversed, the result file should contain S1 in index 998, and S2 at index 997
    outfile_1000 = json_file_1000_0.create_file(list(range(999, -1, -1)))
    print("Creating reversed ", outfile_1000, " to check for reversed S1 and S2")
    with open(outfile_1000, 'r') as reversed_file:
        reversed_list = json.load(reversed_file)
        assert (reversed_list[998] == 'S1')
        assert (reversed_list[997] == 'S2')
        print("Assertions were correct!")

    print("Removing ", outfile_1000)
    os.remove(outfile_1000)


def testing_blackbox_s1_s2_and_file_json(workdir: str):
    print("Creating BlackboxS1S2()")
    blackbox = BlackboxS1S2()
    for i in range(5):
        print(f"Asserting whether return_code from temp_out_1000_{i}.json is true(1)")
        assert (blackbox.get_return_code(f"{workdir}/temp_out_1000_{i}.json"))
    print("Assertions passed!")

    original = FileJSON("temp_out_1000_0.json", workdir)
    reversed_filename = original.create_file(list(range(999, -1, -1)))
    print("\nCreating reversed ", reversed_filename, " to check for reversed S1 and S2 !with blackbox!")

    assert (blackbox.get_return_code(reversed_filename) == 0)
    print(f"Assertion for {reversed_filename} passed (0)\n")

    print("Removing ", reversed_filename)
    os.remove(reversed_filename)


def testing_blackbox_makefile_and_file_makefile(workdir: str):
    print("Creating BlackboxMakefile()")
    blackbox = BlackboxMakefile()
    for i in range(5):
        print(f"Asserting whether return_code from test_makefile_1k_{i}.am is true(1)")
        assert (blackbox.get_return_code(
            os.path.abspath(os.path.join(os.curdir, workdir, f'test_makefile_1k_{i}.am'))))
    print("Assertions passed!")

    original = FileMakefile("test_makefile_1k_0.am", workdir)
    reversed_filename = original.create_file(list(range(999, -1, -1)))
    print("\nCreating reversed ", reversed_filename, " to check for reversed S1 and S2 !with blackbox!")

    assert (blackbox.get_return_code(reversed_filename) == 0)
    print(f"Assertion for {reversed_filename} passed (0)\n")

    print("Removing ", reversed_filename)
    os.remove(reversed_filename)


def read_makefile(filepath):
    with open(filepath, 'r') as file:
        content = file.read()
    return content


def extract_sources(content):
    # Get libmlsimplus_la_SOURCES value
    pattern = r'libmlsimplus_la_SOURCES\s*=\s*\\([\s\S]*?)\n\w'
    match = re.search(pattern, content, re.MULTILINE)
    if match:
        sources_section = match.group(1)
        sources = [line.strip() for line in sources_section.split('\\') if line.strip()]
        return sources
    else:
        raise ValueError("libmlsimplus_la_SOURCES not found in Makefile")


def stretch_array(original_array: list[int], new_length: int) -> list[int]:
    stretched_array = []
    original_length = len(original_array)

    for i in range(new_length):
        stretched_array.append(original_array[i % original_length])

    return stretched_array


def update_makefile(content, new_sources):
    # Replace libmlsimplus_la_SOURCES with new content
    new_sources_content = 'libmlsimplus_la_SOURCES = \\\n' + ' \\\n'.join(new_sources) + '\n'
    updated_content = re.sub(
        r'libmlsimplus_la_SOURCES\s*=\s*\\[\s\S]*?\n(\w|$)',
        new_sources_content + '\\1',
        content,
        flags=re.MULTILINE
    )
    return updated_content


def write_makefile(filepath, content):
    with open(filepath, 'w') as file:
        file.write(content)


def create_test_makefiles(workdir: str):
    original_makefile_path = 'tests/makefile_test.am'
    os.makedirs(workdir, exist_ok=True)

    content = read_makefile(original_makefile_path)
    sources = extract_sources(content)

    # Creating 5 tests for 1000 and 5 for 10000 elements
    testsets_1000: list[list] = [stretch_array(sources, 1000) for _ in range(5)]
    testsets_10000: list[list] = [stretch_array(sources, 10000) for _ in range(5)]

    # 1000 elements 5 times.
    # 0: S1=1, S2=2
    # 1: S1=1, S2=500
    # 2: S1=1, S2=999
    # 3: S1=500, S2=600
    # 4: S1=550, S2=750
    testsets_1000[0][1] = testsets_1000[1][1] = testsets_1000[2][1] = testsets_1000[3][500] = testsets_1000[4][
        550] = "./S1.cpp"
    testsets_1000[0][2] = testsets_1000[1][500] = testsets_1000[2][999] = testsets_1000[3][600] = testsets_1000[4][
        750] = "./S2.cpp"

    # 10000 elements 5 times.
    # 0: S1=1, S2=1000
    # 1: S1=1, S2=5000
    # 2: S1=1, S2=9999
    # 3: S1=5000, S2=6000
    # 4: S1=7000, S2=7575
    testsets_10000[0][1] = testsets_10000[1][1] = testsets_10000[2][1] = testsets_10000[3][5000] = testsets_10000[4][
        7000] = "./S1.cpp"
    testsets_10000[0][1000] = testsets_10000[1][5000] = testsets_10000[2][9999] = testsets_10000[3][6000] = \
        testsets_10000[4][7575] = "./S2.cpp"

    print("Creating files: ")

    # Save Makefiles
    for i in range(5):
        output_path = os.path.join(workdir, f'test_makefile_1k_{i}.am')
        write_makefile(output_path, update_makefile(content, testsets_1000[i]))
        print(output_path)

        output_path = os.path.join(workdir, f'test_makefile_10k_{i}.am')
        write_makefile(output_path, update_makefile(content, testsets_10000[i]))
        print(output_path)

    print("Files were created.")


def clean_test_makefiles(workdir: str):
    print("Removing files: ")
    for i in range(5):
        os.remove(f"{workdir}/test_makefile_1k_{i}.am")
        print(f"{workdir}/test_makefile_1k_{i}.am")
        os.remove(f"{workdir}/test_makefile_10k_{i}.am")
        print(f"{workdir}/test_makefile_10k_{i}.am")
    # if os.path.exists(workdir) and os.path.isdir(workdir):
    #     os.rmdir(workdir)

    print("Files were removed.")


def test_file_makefile(workdir: str):
    print("Creating Makefile objects from test_makefile_1k_0.am and test_makefile_10k_0.am")

    json_file_1000_0 = FileMakefile('test_makefile_1k_0.am', workdir)
    json_file_10000_0 = FileMakefile('test_makefile_10k_0.am', workdir)
    outfile_1000 = json_file_1000_0.create_file(list(range(1000)))
    outfile_10000 = json_file_10000_0.create_file(list(range(10000)))
    print(f"Created {outfile_1000}\n and {outfile_10000} with create_file functionality")

    print("Checking sizes...")
    assert (json_file_1000_0.get_original_size() == 1000)
    assert (json_file_10000_0.get_original_size() == 10000)
    print("Sizes are correct!")

    print("Removing ", outfile_1000)
    os.remove(outfile_1000)
    print("Removing ", outfile_10000)
    os.remove(outfile_10000)

    # in original json 1000 0 S1 is 1, S2 is 2
    # if indexes are reversed, the result file should contain S1 in index 998, and S2 at index 997
    outfile_1000 = json_file_1000_0.create_file(list(range(999, -1, -1)))
    print("Creating reversed ", outfile_1000, " to check for reversed S1 and S2")

    content = read_makefile(outfile_1000)
    source = extract_sources(content)

    assert (source[998] == './S1.cpp')
    assert (source[997] == './S2.cpp')

    print("Assertions were correct!")

    print("Removing ", outfile_1000)
    os.remove(outfile_1000)


def run_tests(workdir: str):
    create_test_jsons(workdir)

    test_file_json(workdir)

    testing_blackbox_s1_s2_and_file_json(workdir)

    clean_test_jsons(workdir)

    create_test_makefiles(workdir)

    test_file_makefile(workdir)

    testing_blackbox_makefile_and_file_makefile(workdir)

    clean_test_makefiles(workdir)

    print("ALL TESTS PASSED!!!!")
