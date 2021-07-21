
cd hapi-api/
# [# Remove a Specific Heroku Application]
heroku login
# [* Login to Heroku from script]
heroku apps:destroy --app lb-hapi-api --confirm lb-hapi-api --remote lb-hapi-api
# [* Destroy the app]
#git remote rm heroku
# [* Remove the Git heroku repo]
#git remote rm lb-hapi-api
# [* Remove the Git app repo]
#git remote rm lb-hapi-api-staging
# [* Remove the Git Staging repo]
heroku apps
# [* Echo the current list of apps]
git remote -v
# [* Echo the current list of heroku apps]
