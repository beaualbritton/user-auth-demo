"""
Beau Albritton 
generate_password.py
"""

import random

#List of potential characters that satisify password strength requirements
uppercase_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lowercase_chars = 'abcdefghijklmnopqrstuvwxyz'
number_chars = '0123456789'
special_chars = '!@#$^&()?'

"""
This function generates a 'strong' password following these requirements:
    8-25 characters
    1 uppercase letter
    1 lowercase letter
    1 number
    1 special character ('!', '@', '#', '$', '^', '&', '(', ')', '?')
Function iterates through a loop twelve times, appends all variety of chars, then shuffles for extra security
"""
def generate_strong_password():
    # Initialize an empty password string to be appended
    password = ''
    
    # For loop to build password with length 12
    for i in range(12):
        # Generate a random index for this iteration using pythons random module
        r = random.random()
    
        #Each of these append a random character in their respective strings.
        if i < 4:
            #This gauruntees a character in index 0-25 inclusive
            password += uppercase_chars[int(r * len(uppercase_chars))]
        elif i < 8:
            password += lowercase_chars[int(r * len(lowercase_chars))]
        elif i < 10:
            password += number_chars[int(r * len(number_chars))]
        elif i < 12:
            password += special_chars[int(r * len(special_chars))]
    
    # Convert to list and shuffle
    password_list = list(password)
    random.shuffle(password_list)
    
    #list to-string using python's join method
    return ''.join(password_list)

"""
This method checks the strength of a given password, iterating through each index in the string,
checking for the following requirements:
    8-25 characters
    1 uppercase letter
    1 lowercase letter
    1 number
    1 special character ('!', '@', '#', '$', '^', '&', '(', ')', '?')

Returns true if all of the password requirements are met, uppercase, lowercase, number, char, and length requirements
"""

def check_password_strength(string):
    #Setting these to false initially
    has_upper = False
    has_lower = False
    has_number = False
    has_special = False

    #Then updating them (flagged) if a desired character is found in a string.
    for char in string:
        if char in uppercase_chars:
            has_upper = True
        if char in lowercase_chars:
            has_lower = True
        if char in number_chars:
            has_number = True
        if char in special_chars:
            has_special = True

    #Might be unintuitive but instead of having multiple if statements, just return all booleans in one grouping
    return has_upper and has_lower and has_number and has_special and not (len(string) < 8 or len(string) > 25)