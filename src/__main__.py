from .core import load_creds, list_files

def main():
    creds = load_creds()
    list_files(creds)

if __name__ == "__main__":
    main()