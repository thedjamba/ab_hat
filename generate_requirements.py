import subprocess

def generate_requirements():
    try:
        result = subprocess.run(['pipreqs', '.', '--force'], check=True, text=True, capture_output=True)
        print(f"requirements.txt has been updated:\n{result.stdout}")
        print("Requirements file generation successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error generating requirements.txt: {e.stderr}")
        print("Requirements file generation failed.")

if __name__ == "__main__":
    generate_requirements()
