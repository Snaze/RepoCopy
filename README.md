# RepoCopy
This is a quick and dirty utility to copy multiple remote repositories from GitHub Enterprise to Github, from GitHub to GitHub Enterprise, or Github Enterprise to Github Enterprise.  It will copy all history and all branches.  

## References

This utility depends on [github3.py](https://github3py.readthedocs.io/en/master/).  To install, simply run the following on the command line:
 
 ```
 pip install github3.py
 ```

## Usage

Simply enter the connection information in Credentials.json and run RepoCopy.py.  Note that in Credentials.json, leave the "url" field blank to designate https://github.com/.  Otherwise, if you specify a specific URL it will be assumed to be GitHub Enterprise.

Below is an example configuration to copy all repositories from a GitHub Enterprise at https://github.somecompany.com/ (for a specific user) to the official GitHub. 

```javascript
{
  "from": {
    "login": "**LOGIN_FOR_SOMECOMPANY**",
    "password": "**PASSWORD_FOR_SOMECOMPANY**",
    "url": "https://github.somecompany.com/"
  },
  "to": {
    "login": "**LOGIN_FOR_GITHUB.COM**",
    "password": "**PASSWORD_FOR_GITHUB.COM**",
    "url": ""
  }
}
```

Note, that the following properties from the source repository will be preserved in the newly created destination repository:

* name
* description 
* homepage
* private
* has_issues
* has_wiki 
* has_downloads

Also, note that RepoCopy.py will need appropriate file permissions to the parent directory of where RepoCopy.py lives.  RepoCopy will clone each source repository to ..\RepoCopyTemp, create the destination repository, then will push up all the branches and history to the new repository.  Finally, ..\RepoCopyTemp will be deleted.  It will iterate over this process 1-by-1, until all the repositories have been copied.


Final note:

Use this at your own risk.  While I tested and used this myself, I am not responsible for any unforeseen bugs.  Review the code before using.

 
 
