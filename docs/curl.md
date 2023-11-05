## Create a Service Account Password
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin -d '{"password_threshold":3, "user_passwords":{"hi":"1", "bye":"2", "other":"3", "next":"4", "final":"5"}}'

## Regenerate a Service Account Password
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/regen -d '{"user_passwords":{"hi":"1", "bye":"2", "other":"3"}, "new":{"password_threshold":2, "user_passwords":{"other":"password123", "thing":"qwerty", "different":"cool_password", "first":"battery-horse-staple", "second":"last_pass"}}}'

## Login
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"hi":"1", "bye":"2", "other":"3"}}'

### Login After Regeneration
curl -i -X POST -H "Content-Type:application/json; charset=utf-8" http://localhost:8080/api/service/example/account/example-admin/login -d '{"user_passwords":{"different":"cool_password", "first":"battery-horse-staple", "second":"last_pass"}}'