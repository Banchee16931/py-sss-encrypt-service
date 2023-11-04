# py-sss-encrypt-service
A python library made for SSS Encryption on admin passwords as a service

Excellent overview of the project including  client, operational environment, and team. Excellent description of opportunity or challenges that gave rise to the project. Detailed description of the business process and reasons for choosing it for this assignment. Short and concise.   

## Overview of the project
The goal of this project is to create a microservice that takes in multiple admin passwords and if they are valid and there are enough of them to reach that specific password's threshold, it will return a single session token for whatever tool that password was for. It should have both an API as well as a website user interface.

### Client
DevOps team admins. This system is designed to cater towards the admins within the DevOps team and enable them to access admin account safely while forcing them to follow process guidelines.

### Operational Environment
The service will be deployed inside of a Kubernetes cluster ran across internal servers within the company. It will also be deployed on a air-gapped network and as a result reliance on non-standard packages should be kept to a minimum. An example of this is the choice to use a custom router solution rather than a non-standard python library like Flask.

### Team
This will be used within the DevOps team. I will be the sole contributor throughout the project but 

### Process Overview
The process that is being tackled by this project is how members of the DevOps team access admin accounts. This process is full of security flaws 

### Issues with current process that caused this project
The process for gaining admin permissions is quite a scary and decently unsecure process. It currently relies on a single shared set of passwords that are used for different admin accounts across the toolset. There are three main flaws with this process:
1. Having the passwords shared between each admin means that as more admins are added the passwords themselves are spread around and as a result the chance of them leaking increases.
2. Having each account secured by a singular password means that admins can individually access these accounts. Our currently process guidelines state that another admin must be present during this process but the system itself doesn't force this to take place.
3. Since the current process is one password per tool, admins are likely to forget it or have to write it down to make sure the remember.

## Proposed Solutions
### Have multiple admin accounts for each tool. One per admin
#### Pros
- Stops issue #3 as admins get to have there own password for their own admin account. This means they are less likely to write it down
#### Cons
- More accounts mean more things to keep secure and check for leaks. It also makes the password reset process more complex.

### SSS Encryption
#### Pros
- Stops issue #1 and #2. TODO

## Chosen solution
SSS Encryption with singular accounts, per tool, was chosen to lower management cost of multiple accounts.

### Improvements to the chosen option
#### Encrypt broken down SSS passwords with user defined passwords
This means that user's can define passwords that they will actually remember, reducing the likelihood they write it down anywhere.

#### Return session tokens to user rather than requiring a password per request
Using each tool's session token system, if applicable is a great choice as it means that admins will only have access for a set period of time. This means that after the two admins enter in there passwords, the observing admin can stay with that person throughout the token lifetime to ensure they don't do anything other than what is required. It also stops admins circumventing the system by just storing the master password and using it each time.