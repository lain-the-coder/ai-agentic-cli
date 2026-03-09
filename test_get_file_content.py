from functions.get_file_content import get_file_content

# --- LOREM IPSUM TRUNCATION TEST ---
print('Testing "lorem.txt" truncation:')
lorem_content = get_file_content("calculator", "lorem.txt")
print(f"Total length returned: {len(lorem_content)} characters")
# Check if the "truncated" message is at the end of the string
if "truncated" in lorem_content:
    print("SUCCESS: Truncation message found at the end of the content.")
else:
    print("FAILURE: Truncation message NOT found.")
print("-" * 30)

# --- STANDARD FILE READS ---
print('get_file_content("calculator", "main.py"):')
print(get_file_content("calculator", "main.py"))
print("-" * 30)

print('get_file_content("calculator", "pkg/calculator.py"):')
print(get_file_content("calculator", "pkg/calculator.py"))
print("-" * 30)

# --- ERROR CASE: SECURITY BREACH ---
print('get_file_content("calculator", "/bin/cat"):')
# Indent the error slightly to match the assignment's visual style
print(f"    {get_file_content('calculator', '/bin/cat')}")
print("-" * 30)

# --- ERROR CASE: MISSING FILE ---
print('get_file_content("calculator", "pkg/does_not_exist.py"):')
print(f"    {get_file_content('calculator', 'pkg/does_not_exist.py')}")
