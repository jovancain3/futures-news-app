import os
import sys

# Function to display colored text
def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def setup():
    print_colored("Setting up Futures Market News App...", "1;34")  # Blue text
    
    # Create the templates directory if it doesn't exist
    if not os.path.exists('templates'):
        print("Creating templates directory...")
        os.makedirs('templates')
    
    # Check if app.py exists in the current directory
    if not os.path.exists('app.py'):
        print_colored("Error: app.py file not found!", "1;31")  # Red text
        print("Please make sure you have created app.py in the current directory.")
        return False
    
    # Create index.html in templates directory if it doesn't exist
    if not os.path.exists('templates/index.html'):
        print("Creating index.html template...")
        try:
            # Prompt user to create the file
            print_colored("Please create the file 'templates/index.html' with the content provided.", "1;33")  # Yellow text
            print("You can copy-paste the HTML content from the index-html file.")
        except Exception as e:
            print_colored(f"Error creating template file: {str(e)}", "1;31")  # Red text
            return False
    
    # Install required packages
    print("Installing required packages...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "requests", "beautifulsoup4"])
    except Exception as e:
        print_colored(f"Error installing packages: {str(e)}", "1;31")  # Red text
        print("Please manually install the required packages:")
        print("pip install flask requests beautifulsoup4")
        return False
    
    print_colored("\nSetup completed successfully!", "1;32")  # Green text
    print_colored("\nTo run the application:", "1;36")  # Cyan text
    print("1. Make sure your current directory contains app.py")
    print("2. Run the following command:")
    print_colored("   python app.py", "1;36")  # Cyan text
    print("3. Open your web browser and go to: http://127.0.0.1:5000")
    
    return True

if __name__ == "__main__":
    setup()