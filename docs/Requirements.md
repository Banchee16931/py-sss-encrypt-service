# Definitions
| Word or Phrase           | Definition                                                                              |
| ------------------------ | --------------------------------------------------------------------------------------- |
| User Password            | The passwords that admin users enter into the system. |
| Master Password          | The per tool password that is actually sent to the tool for access. |
| Intermediate Password    | Passwords that is decrypted with the user password and through SSS encryption is assembled to create the master password for a tool |

# Document Layout
This document is has the following requirements structure: numbered headings are used to categorise requirements. Requirements are in the numbered in the format "X.Y." where "X" is the category (defined by the numbered heading) and "Y" is a number to distinctly identify that requirement within that category. 

Individual requirements are structured using the EARS convention ([info](https://alistairmavin.com/ears/#:~:text=The%20EARS%20ruleset%20states%20that,the%20clauses%20that%20are%20used.)).

Requirements are tagged to add extra information about them. The tags are as follows:
| Tag | Definition |
| --- | --- |
| Type | Defines a further breakdown of what a requirement is categorised as, such as security, usability, performance, maintainability, portability, reliability and availability |
| Completion | The specific test or part of the code that meets this requirement |
| Justification (optional) | Explaining why a requirement exists |

_Example:_
### Example Category
1.1. My system shall perform this action.


# Functional Requirements
## 1 Initial Password Generation
1.1. While a unique master password has not been generated for a given 

1.2. When 

## 5 Tool interaction
For this project tools will be swapped out for an interface that represents them (this is because all the tools are hosted on an air-gapped environment so for the sake of this assignment they have to be mocked.) As such the following requirements are meant to ensure that the mocked tool interfaces will perform the same actions as an actual interface would.

5.1. The tool interface shall allow passwords to be changed.  

5.2. The tool interface shall receive a username an password and respond if it matched with their stored counterparts.  

5.3. The tool interface shall store usernames as text.  

5.4. The tool interface shall store passwords as text.  
__Justification:__ _This is because it is a mock interface, further encryption isn't needed._

5.5. The tool interface shall store usernames and passwords persistently.  



# Non-Functional Requirements
## 50 User Password Handling

50.1. User passwords shall never be persistently stored in a non hashed state.  
__Type:__  _security_

50.2. User passwords shall be stored for verification using the bcrypt standard.  
__Type:__  _security_

## 51 Intermediate Password Handling
51.1. Intermediate passwords shall be encrypted using the AES standard.  
__Type:__  _security_

51.2. Intermediate passwords shall never be persistently stored in a non-encrypted state.  
__Type:__  _security_

## 52 Master Password Handling
52.1. Master passwords must be generated via a OS based source of randomness suitable for cryptographic use.  
__Type:__  _security_

# 60 Miscellaneous Requirements
60.1. No non-standard python packages shall be used expect those on the following list:
 - pycryptodome
   - `pip install pycryptodome`
 - bcrypt 
   - `pip install bcrypt`

__Type:__ _portability_  
__Justification:__ _This system will be deployed onto an air gapped network and these packages are already deployed on it_