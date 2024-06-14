import subprocess

def execute_powershell_command(command, timeout):
    try:
        # Execute the PowerShell command with a timeout
        result = subprocess.run(
            ["powershell", "-Command", command], 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        
        # Check if there were any errors
        if result.returncode != 0:
            return f"Error: {result.stderr}"
        
        # Return the output of the command
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds"
    except Exception as e:
        return str(e)

def main():
    print("Welcome to the PowerShell Agent Terminal Tool with Timeout")

    # Get the timeout value from the user
    timeout = 1
    while True:
        # Get the command from the user
        command = input("Enter PowerShell command (or 'exit' to quit): ")
        
        if command.lower() == 'exit':
            break
        
        # Execute the command with the specified timeout and get the output
        output = execute_powershell_command(command, timeout)
        
        # Display the output
        print(output)

if __name__ == "__main__":
    main()
