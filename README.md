# py-sss-encrypt-service
A University coursework project for the University of Hertfordshire.

## Interacting with this codebase
If you are loading this from GitHub run the following in an empty folder:
```
git clone https://github.com/Banchee16931/py-sss-encrypt-service.git
```

Once you have this codebase in a folder cd to that folder to get started.  
This tutorial assumes you have python at least Python 3.10 installed.

Run the following python installation commands:
```
py -m ensurepip --upgrade
py -m pip install pycryptodome
py -m pip install bcrypt
```

To test the system run the following commands:
### Starting the server
```
py main.py
```

Ensure that all following commands are ran in a different terminal.

### Generating a master password:
First to prove it doesn't let you login straight away run:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"hi":"1", "bye":"2", "other":"3"}}'
```

Which should fail. Then run this to create it:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin -d '{"password_threshold":3, "user_passwords":{"hi":"1", "bye":"2", "other":"3", "next":"4", "final":"5"}}'
```

And run that first command again to prove it now exists:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"hi":"1", "bye":"2", "other":"3"}}'
```

### Regenerating a master password
After doing "Generating a master password", you can try out regenerating it. First check that you cannot use the new credentials:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"different":"cool_password", "first":"battery-horse-staple", "second":"last_pass"}}'
```

Which should fail, then regenerate the password:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/regenerate -d '{"user_passwords":{"hi":"1", "bye":"2", "other":"3"}, "new":{"password_threshold":2, "user_passwords":{"other":"password123", "thing":"qwerty", "different":"cool_password", "first":"battery-horse-staple", "second":"last_pass"}}}'
```

Now the new credentials should work:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"different":"cool_password", "first":"battery-horse-staple", "second":"last_pass"}}'
```

And the old ones won't:
```
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"hi":"1", "bye":"2", "other":"3"}}'
```

## If you have any issues
If you are the University assessor, I have attached a demo video to my submission, just in-case, in the backup_demo.zip folder.
