# Passer - Backend
This repository contains backend server logic for application **Passer**. See [the main repository](https://github.com/petercurikjr/passer) (that contains Bachelor thesis dealing with given problem, website and iOS app). 

Each `@app.route` deals with either iOS app or Website interaction. They are described below.

### Interaction with the iOS app
When a user want to access his items on a foreign device without Passer, he uses the **Outsider** functionality. Outsider lets user choose, which items to send. Then, he chooses a one-time verification method that will be used to authenticate himself on the [website](https://passer.netlify.app).

After this process, data are sent to the server. Passer uses `HTTP POST` to send chosen items and verification method to server. This entry is deleted after 2 minutes.

### Interaction with the Website
Website sends entered verification to server and it responds with one of two states:
- `OK` status - Data of the user in `JSON` format are returned 
- `ERR` status - Entered verification method is not correct

The website (currently) offers two methods of one-time authentication:
- Six-digit code
        - User enteres the code generated in the iOS app. Website sends the code to the server to check. 
- QR code
        - User points his iOS device to website's QR code, which is uniquely generated each time. QR contains a `session-id` that is sent by the iOS Passer app (with the selected items to send) to the server after successful scan. 
        - In the meantime, website checks (in a loop) whether a given `session-id` wasn't already scanned by someone.

