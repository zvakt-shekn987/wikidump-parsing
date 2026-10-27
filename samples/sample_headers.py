from extraction.functions_headers import read_headers

def main():
    for item in read_headers():
        print(item)
        
if __name__ == "__main__":
    main()