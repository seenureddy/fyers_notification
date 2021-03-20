#Fyers Backend Challenge

Create an application in Python which mimics an email client.

##Tasks
  - User must be able to send email with to,cc,bcc, subject and body
  - There must be a capability to send mass emails by uploading a csv file with email ids which contains to, from, cc, bcc, subject and body.
  - At the end of the day(say 9PM) the admin should receive an email with basic analytics like the number of emails sent. You can add a cron script which calls a python function as part of the submission which does this
## Setup:
- Emails must be sent via a smtp server you can use gmail, zoho etc to configure the email client.
- All your app logs must be streamed to ELK stack, You can use the free version from elastic to implement the feature.   

## Instructions:    
- You can use any python framework to complete this.
- API endpoints and setup instructions must be clearly documented in a readme file along with a requirement.txt file for setup.
- Code must be pushed to github.
- In the submission email the link to the repo must be mentioned along with screenshots of working api on postman and logs on elk web UI   

##Bonus points: 
Host the application on AppEngine/Heroku/AWS.   

The Final evaluation will be on these criteria
   1. Ingenuity of the approach
   2. Accuracy/relevance of the solution
   3. Time taken to submit the solution
   4. Code quality and documentation