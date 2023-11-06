# Definitions
| Word or Phrase           | Definition                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------- |
| User Password            | The passwords that admin users enter into the system. |
| Master Password          | The per tool password that is actually sent to the tool for access. |
| Intermediate Password    | Passwords that is decrypted with the user password and through SSS encryption is assembled to create the master password for a tool |
| SSS | Shamir's Secret Sharing Algorithm |
| AES | Advanced Encryption Standard |

# Document Layout
This document is has the following requirements structure: numbered headings are used to categorise requirements. Requirements are in the numbered in the format "X.Y." where "X" is the category (defined by the numbered heading) and "Y" is a number to distinctly identify that requirement within that category. 

Individual requirements are structured using the EARS convention ([info](https://alistairmavin.com/ears/#:~:text=The%20EARS%20ruleset%20states%20that,the%20clauses%20that%20are%20used.)).

Requirements are tagged to add extra information about them. The tags are as follows:
| Tag | Definition |
| --- | --- |
| Type (only for non-functional requirements) | Defines a further breakdown of what a non-function requirement is categorised as, such as security, usability, performance, maintainability, portability, reliability and availability |
| Completion | The specific test or part of the code that meets this requirement |
| Rationale (optional) | Explaining why a requirement exists |

_Example:_
### Example Category
1.1. My system shall perform this action.

# Functional Requirements
## 1. General Format Definitions
1.1. When handling a request sent to a JSON based endpoint (defined by the path starting with `/api`), If the server is responding with an error code (400-499), then the server shall return a response whose body contains the following:
| Field Name | Type | Definition | 
| --- | --- | --- |
| message | string | An error message that explains why that specific request failed |

## 2 HTTP Server Operation
2.1. If the server receives a path that is not defined in these requirements to be handled, then the server shall respond with a 400 (Bad Request) HTTP Status Code.

## 3 Server Start-up
3.1. When ran, the system must start-up a HTTP Server.

3.2. When ran, the system shall ensure that a table called "passwords" with the following schema exists in the connected database:
| Column Name | Type | Primary Key? |
| --- | --- | --- |
| service_name | text | yes |
| account_id | text | yes |
| user_id | text | no |
| hashed_password | text | no |
| encrypted_share | text | no |

3.3. The HTTP Server shall be multi-threaded, so that two request can be handled simultaneously if the connected database allows for it.

## 4 Master Password Generation
4.1. When the a HTTP POST request with the following path is received by the server `/api/service/{service name}/account/{account id}`, the server shall treat it as a password generation request.

4.2. When receiving a password generation request, If the body does not follow the format defined below, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 1.1.
| Field Name | Type | Definition | 
| --- | --- | --- |
| password_threshold | integer | The amount of user passwords required to reconstruct the master password being generated |
| user_passwords | Map[string, string] | The full list of user ids mapped to their respective user passwords that can be given to reconstruct the master password |

4.3. When receiving a password generation request, If the given password_threshold field is greater than the number of items in the user_passwords field, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 1.1.

4.4. When handling a password generation request, the server shall generate a new master password that can be reconstructed using the request's given user passwords.

4.5. When storing intermediate passwords during a password generation request, the following must be stored:
| Column Name | Value Stored |
| --- | --- |
| service_name | The service name given in the path of the request. |
| account_id | The account id given in the path of the request. |
| user_id | The user id of the password used to encrypt the intermediate password. |
| hashed_password | A hash of the user password used to encrypt the intermediate password. |
| encrypted_share | An intermediate password encrypted using a user password given in the user_passwords field. |

4.6. When responding to a successful password generation request, the response's header must abide by the following:
```yaml
HTTP Status Code: 201 (Created)
Headers:
  Content-Type: application/json; charset=utf-8
```

4.7. When returning the response to a successful password generation request, the body of the response shall be in the following JSON format:
```json
{
  password: "{generated master password goes here}"
}
```

## 5 Account Login
5.1. When the a HTTP POST request with the following path is received by the server `/api/service/{service name}/account/{account id}/login`, the server shall treat it as a login request.

5.2. When receiving a login request, If the body does not follow the format defined below, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 1.1.
| Field Name | Type | Definition | 
| --- | --- | --- |
| user_passwords | Map[string, string] | A list of user ids mapped to their respective user passwords that can be given to reconstruct the master password |

5.3. When receiving a login request, If the number of items in the user_passwords field is less than the number of user passwords that are required to reconstruct the relevant master password, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 

5.4. When receiving a login request, the server shall reconstruct the service account's master password using the request's user_passwords field.

5.5. When a master password is reconstructed during a login request, the server shall send it to the relevant service to get a session token for that account in that service.

5.6. When responding to a successful login request, the response's header must abide by the following:
```yaml
HTTP Status Code: 201 (Created)
Headers:
  Authorization: Bearer {session token}
```

## 6 Regenerating A Service Account's Password
6.1. When the a HTTP POST request with the following path is received by the server `/api/service/{service name}/account/{account id}/regenerate`, the server shall treat it as a password regeneration request.

6.2. When receiving a password regeneration request, If the body does not follow the format defined below, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 1.1.
| Field Name | Type | Definition | 
| --- | --- | --- |
| user_passwords | Map[string, string] | A list of user ids mapped to their respective user passwords that can be given to reconstruct the service account's current master password |
| new | NewPasswordObject | The data required to generate a new master password. |
Definition of a NewPasswordObject:
| Field Name | Type | Definition | 
| --- | --- | --- |
| password_threshold | integer | The amount of user passwords required to reconstruct the new master password being generated |
| user_passwords | Map[string, string] | The full list of user ids mapped to their respective user passwords that can be given to reconstruct the new master password |

6.3. When receiving a password regeneration request, If the number of items in the user_passwords field is less than the number of user passwords that are required to reconstruct the relevant master password, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 1.1.

6.4. When receiving a password generation request, If the given new.password_threshold field is greater than the number of items in the new.user_passwords field, then the server shall give a response with the 400 (Bad Request) HTTP status code obeying the content requirements outlined in requirement 1.1.

6.5. When receiving a password regeneration request, the server shall reconstruct the service account's master password using the request's user_passwords field.

6.6. When a master password is reconstructed during a password regeneration request, the server shall send it to the relevant service to get a session token for that account in that service.

6.7. When a session token is received from a service deeming the inputted user_passwords as valid, the server shall generate a new master password that can be reconstructed using the request's given new.user_passwords field.

6.8. When storing the new intermediate passwords during a password generation request, the old intermediate passwords must be deleted for the database.

6.9. When storing the new intermediate passwords during a password generation request, the following data must be stored:
| Column Name | Value Stored |
| --- | --- |
| service_name | The service name given in the path of the request. |
| account_id | The account id given in the path of the request. |
| user_id | The user id of the password used to encrypt the intermediate password. |
| hashed_password | A hash of the user password used to encrypt the intermediate password. |
| encrypted_share | An intermediate password encrypted using a user password given in the new.user_passwords field. |

6.10. When responding to a password regeneration request, the response's header must abide by the following:
```yaml
HTTP Status Code: 201 (Created)
Headers:
  Content-Type: application/json; charset=utf-8
```

## 7 Tool interaction
For this project tools will be swapped out for an interface that represents them (this is because all the tools are hosted on an air-gapped environment so for the sake of this assignment they have to be mocked). As such the following requirements are meant to ensure that the mocked tool interfaces will perform the same actions as an actual interface would.

7.1. The mocked tool interface shall return a session id given the correct account id and master password.  

7.2. When the master password for an account, during the process of getting a session token, isn't stored, the mocked tool interface should store the master password given by the system as the master password for this account, continuing the request as if that master password was the correct one all along.
**Rationale:** When initially generating a master password it is supposed to be given to the user to allow them to update it for that service. During this there is no communication with the service itself, as the system currently doesn't have the correct master password for that service. This means when our service mock is asked for a session token for the first time it doesn't have the master password, therefore we use the one that is given as the master password.

7.3. The mocked tool interface shall allow a master password to be changed given the correct old master password and account id.  

7.4. When the old master password isn't stored during the process of changing it, the mocked tool interface should accept the new master password and store it as the master password for that service and account id.
**Rationale:** When initially generating a master password it is supposed to be given to the user to allow them to update it for that service. During this there is no communication with the service itself, as the system currently doesn't have the correct master password for that service. This means when our service mock is asked to change the master password for the first time it doesn't have the master password, therefore we use the new one that is given as the master password.

# Non-Functional Requirements
## 8 User Password Handling
8.1. When storing user passwords, the system shall never store them in a non hashed state.  
__Type:__  _security_
 
8.2. When ensuring user passwords are correct, the system shall use the bcrypt standard.
__Type:__  _security_

## 9 Intermediate Password Handling
9.1. When encrypting intermediate passwords, the system shall use the AES standard.  
__Type:__  _security_

9.2. When storing intermediate passwords, the system shall always ensure they are encrypted with their relevant user password as the key.  
__Type:__  _security_

## 10 Master Password Handling
10.1. When generating master passwords, the system shall use an OS based source of randomness suitable for cryptographic use.  
__Type:__  _security_

10.2. When generating master passwords, the system shall ensure they are at least 128 bytes long.  
__Type:__  _security_

10.3. When splitting a master password into intermediate passwords, the system shall use the Shamir's Secret Sharing Algorithm.  
__Type:__  _security_

10.3. When reconstructing a master password from intermediate passwords, the system shall use the Shamir's Secret Sharing Algorithm.  
__Type:__  _security_

10.5. The system shall never store master passwords in any format except its intermediate passwords.  
__Type:__  _security_

# 11 Miscellaneous Requirements
11.1. The system shall not use any non-standard python packages expect those on the following list:
 - pycryptodome
   - `pip install pycryptodome`
 - bcrypt 
   - `pip install bcrypt`
__Type:__ _portability_  
__Rationale:__ _This system will be deployed onto an air gapped network and these packages are already deployed on it, any others would have to be certified and then moved over_