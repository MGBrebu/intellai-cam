import os
from pathlib import Path

# DEF: Clear specified file, or all JSON files in a specified folder
def clear_analysis(analysis_file=None, analysis_folder='./analysis'):
    if analysis_file:
        analysis_path = os.path.join(analysis_folder, analysis_file)
        if os.path.exists(analysis_path):
            os.remove(analysis_path)
            print(f"Cleared analysis file: {analysis_path}")
            return True
        else:
            print(f"Analysis file does not exist: {analysis_path}")
            return False
    else:
        if not os.listdir(analysis_folder):
            print(f"Analysis folder is empty: {analysis_folder}")
            return True
        for json_file in Path(analysis_folder).glob('*.json'):
            try:
                os.remove(json_file)
                print(f"Cleared analysis file: {json_file}")
            except Exception as e:
                print(f"Error clearing file {json_file}: {e}")
                return False
            print(f"Cleared all analysis files in folder: {analysis_folder}")
        return True

# Main
def main():
    clear_analysis()

if __name__ == "__main__":
    main()
