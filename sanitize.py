"""
Beau Albritton
Quick Sanitize Script
"""

"""
This method returns a sanitized string based on user input. Function scans the string and removes any dangerous characters that would result in SQL INJECTION
"""
def sanitize(string):
    # Characters to remove
    dangerous_chars = '"%*/'
    
    # String to be appended
    sanitized_term = ''
    
    # Iterate through each character in the search term
    for char in string:
        # Append the character only if it's not in dangerous_chars
        if char not in dangerous_chars:
            sanitized_term += char    
    return sanitized_term
