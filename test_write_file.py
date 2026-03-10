from functions.write_file import write_file

# Test 1: Overwriting (Fixed the internal apostrophe)
print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum"):')
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
print("-" * 30)

# Test 2: New Subfolder
print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"):')
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
print("-" * 30)

# Test 3: Security Breach
print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed"):')
print(f"    {write_file('calculator', '/tmp/temp.txt', 'this should not be allowed')}")
