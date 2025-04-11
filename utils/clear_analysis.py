import os

def clear_analysis(analysis_file, analysis_folder='./analysis'):
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
        os.remove(analysis_folder/'*.json')
        print(f"Cleared all analysis files in folder: {analysis_folder}")
    return True

clear_analysis()