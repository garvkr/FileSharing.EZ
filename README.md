This project implements a secure file-sharing system with two user roles: *Ops User* and *Client User*.

## *Features*
1.⁠ ⁠Ops User Actions:
   - Login
   - Upload files (only ⁠ .pptx ⁠, ⁠ .docx ⁠, ⁠ .xlsx ⁠ formats)

2.⁠ ⁠*Client User Actions*:
   - Sign up (receives an encrypted verification URL)
   - Email verification
   - Login
   - List all uploaded files
   - Download files (receives a secure, encrypted download URL)

3.⁠ ⁠*Security*:
   - Passwords are securely hashed.
   - File downloads are managed via encrypted URLs, valid only for client users.

## API Endpoints

### Auth
•⁠  ⁠*POST /signup*  
  Registers a new client user and returns a verification URL.

•⁠  ⁠*GET /email-verify*  
  Verifies the user email using the provided token.

•⁠  ⁠*POST /login*  
  Logs in a user with email and password.

### File Management
•⁠  ⁠*POST /upload*  
  Allows Ops users to upload files (restricted to ⁠ .pptx ⁠, ⁠ .docx ⁠, ⁠ .xlsx ⁠).

•⁠  ⁠*GET /files*  
  Lists all uploaded files (for client users).

•⁠  ⁠*POST /download*  
  Returns an encrypted download URL for a specific file (for client users).

•⁠  ⁠*GET /download-file*  
  Downloads a file using the encrypted URL.
