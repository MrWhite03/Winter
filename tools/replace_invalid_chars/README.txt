1.  Place all snowball scripts into their own directory.
2.  Place 'replace_invalid_chars.py' in the same directory.
3.  Ensure current working directory is the same directory.
4.  Run 'replace_invalid_chars.py' with no arguments.

NOTES:
=============================================================
'replace_invalid_chars.py' operates as follows:

- Creates a new directory in current working directoy 
  name 'original_scripts' (if directory already exists
  'replace_invalid_chars.py' will print a message to console
  and immediately exit.  This is to prevent accidentally 
  overwrite of original snowball scripts)
- All original scripts are copied into this folder and remain
  untouched
- Creates new scripts with the appropriate replacements