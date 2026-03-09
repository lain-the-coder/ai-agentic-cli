from functions.get_files_info import get_files_info

# Test 1: Looking at the root of the calculator
print('get_files_info("calculator", "."):')
print('Result for current directory:')
print(get_files_info("calculator", "."))
print() # Add a blank line for readability

# Test 2: Looking inside the 'pkg' folder
print('get_files_info("calculator", "pkg"):')
print("Result for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))
print()

# Test 3: The "Security Attack" 1 (Trying to access system /bin)
print('get_files_info("calculator", "/bin"):')
print("Result for '/bin' directory:")
# Your code should catch this and return the "Error:..." string
print(f"    {get_files_info('calculator', '/bin')}") 
print()

# Test 4: The "Security Attack" 2 (Trying to climb up with ../)
print('get_files_info("calculator", "../"):')
print("Result for '../' directory:")
print(f"    {get_files_info('calculator', '../')}")
