# Sequence
sequenceDiagram
    participant Client
    participant Server
    participant Router
    participant CreateMasterPassword
    participant Crypt
    participant DB
    Client->>Server: password generation request
    activate Server
    Server->>Router: get_handler(path)
    activate Router
    Router-->>Server: CreateMasterPassword
    deactivate Router
    Server->>CreateMasterPassword: __call__(request)
    activate CreateMasterPassword
    CreateMasterPassword->>Crypt: split(threshold, user_passwords.length)
    activate Crypt
    Crypt-->>CreateMasterPassword: shares
    deactivate Crypt
    
    loop per share
         
         CreateMasterPassword->>Crypt: hash(used_password)
         activate Crypt
         Crypt-->>CreateMasterPassword: hashed_user_password
         deactivate Crypt
         CreateMasterPassword->>Crypt: encrypt(used_password, share)
         activate Crypt
         Crypt-->>CreateMasterPassword: encrypted_share
         deactivate Crypt
         CreateMasterPassword->>DB: store_share()
    end

    CreateMasterPassword-->>Server: master_password
    deactivate CreateMasterPassword
    Server-->>Client: master_password
    deactivate  Server

# Class Diagram
classDiagram
    class ServiceConnector {
        <<Interface>>
        +get_session_token(string account_id string password)
        +update_account_password(string account_id string old_password string new_password)
    }

    class _ExampleConnector {
        +get_session_token(string account_id string password)
        +update_account_password(string account_id string old_password string new_password)
    }
    ServiceConnector <|.. _ExampleConnector

    class Handler {
        <<Interface>>
        +__call__(Request req) Response
    }

    class Crypt {
        <<Helper>>
        +split(int threshold int share_count string secret) List~string~
        +combine(shares List~string~) string
        +encrypt(string password string data)
        +decrypt(string password string encrypted_data)
        +hash(string password)
        +check_hash(string pasword string hash)
    }

    class DBClient {
        <<Singleton>>
        +store_password(string service_name string account_id string user_id string hashed_password string encrypted_share)
        +get_password(string service_name string account_id string user_id) UserPassword
    }
    
    class CreateMasterPasswordHandler {
        +__call__(Request req) Response:
    }
    Handler <|.. CreateMasterPasswordHandler
    CreateMasterPasswordHandler ..> DBClient
    CreateMasterPasswordHandler ..> Crypt

    class LoginHandler {
        +__call__(Request req) Response:
    }
    Handler <|.. LoginHandler
    LoginHandler ..> DBClient
    LoginHandler ..> Crypt
    LoginHandler ..> ServiceConnector
   
    class RegenerateMasterPasswordHandler {
        +__call__(Request req) Response:
    }
    Handler <|.. RegenerateMasterPasswordHandler
    RegenerateMasterPasswordHandler ..> ServiceConnector
    RegenerateMasterPasswordHandler ..> Crypt
    
    class Route {
        +string path
        +List~str~ split_path
        +Map~int str~ params
        +Handler handler
        -list~Method~ __methods
        +methods() List~Method~
        +add_method(method Method...)
        +get_handler(List~string~ path)
    }
    Route "1" *-- "1" Handler

    class Router {
        +Map~Method List~Route~~ routes
        +add_route(Route route)
        +get_handler(Method method, List~string~ path)
    }
    Router "1" *-- "0..1" Route

    class Server {
        #Router _router
        +do_GET()
        +do_POST()
        +do_PUT()
        +do_DELETE()
        +pre_start()
        +handle_request()
        #_get_body()
        #_init_routes()
    }
    Server "1" *-- "1" Router

    