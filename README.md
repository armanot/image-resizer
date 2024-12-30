imgur client_id: 1f6e4c5aa12a23f
imgur client_secret: 0a7111bd3a1bf4c183445706ae0509469e8c8361
access_token: 95979e5ca603a0e701ed51c5ceca039c9e3441b7
expires_in=315360000&token_type=bearer&refresh_token=0c795b1012b61b414627f20b4733036a34e74232&account_username=armanot&account_id=187634075



Manage Uploaded Images:

Use the deletehash to delete the image programmatically if needed:
bash
Copy code
curl -X DELETE https://api.imgur.com/3/image/nyMYABoVgQCY7Ie \
     -H "Authorization: Bearer 95979e5ca603a0e701ed51c5ceca039c9e3441b7"
Integrate with Your App:

Modify your backend to use the access token and automatically upload resized images to Imgur.
Handle Token Expiry:

Refresh the access token when it expires using the refresh token:
bash
Copy code
curl -X POST https://api.imgur.com/oauth2/token \
     -F "client_id=YOUR_CLIENT_ID" \
     -F "client_secret=YOUR_CLIENT_SECRET" \
     -F "grant_type=refresh_token" \
     -F "refresh_token=YOUR_REFRESH_TOKEN"