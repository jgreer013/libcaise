from util.file_loader import FileLoader

def main():
    fl = FileLoader()
    fn = "source/cpp_examples/bin/binary_search.b"
    fl.addFilename(fn)
    d = fl.getData()
    for data in d:
        print(data[0].getFullName(), len(data[1]))

main()
