[slack.open-austin.org](http://slack.open-austin.org) is a Slackin server. It allows people to self-invite themselves to the Open Austin slack (slack.open-austin.org)

@larcher and @luqmaan set slackin up as part of https://github.com/open-austin/project-ideas/issues/19.

The Slackin server is deployed to the Open Austin Heroku account.

To update Slackin:

- set your computer up to use heroku with the open austin credentials 
- `git clone https://git.heroku.com/openaustin-slackin.git`
- `git remote add rauchg git@github.com:rauchg/slackin.git`
- `git merge rauchg/master -X theirs`
- verify that things still work
  - `npm install`
  - `SLACK_API_TOKEN=... SLACK_SUBDOMAIN=open-austin npm start`
  - navigate to localhost:3000
- `git push origin master`

