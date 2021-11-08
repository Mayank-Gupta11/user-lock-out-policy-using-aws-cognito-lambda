# user-lock-out-policy-using-aws-cognito-lambda

In order to use above two lambda functions, just create two lambda functions in your aws lambda console with any name say (pre-auth and post-auth) and copy paste the entire code, once that is done
just edit the varibales <pool_id> in those lambda functions with your cognito user pool id which you can get by clicking on genral setting tab in cognito.

along with this, you will also have to create two custom attribute in cognito with name as #static_time_of_user
(for storing the user time for which he/she has been locked) and #count_limit_of_user (for storing current count of unsucessful login attempts)

now go to cognito dashboard under trigger section choose <pre-auth> lambda that you created above under pre authentication section and <post-auth> lambda that you created above under post authentication section.

# How it works
so now what will happen as user visits the login page, whether they enter correct credentials or wrong pre-auth lambda will be triggered and <count_limit_of_user> attirubute value will be incremented by 1 if they have entered correct credentials then they will be logged in sucessfully and post-auth lambda will be triggered that will make <count_limit_of_user> attribute value back to 0. but in case if they have entered wrong credentials then they will not be able to login and post-auth lambda will not trigger that is, user will again enter his/her credentials and now again if they enter wrong credentials say 4-5 times then <count_limit_of_user> attribute value will be incremented by 4-5 and as this limit increases user will be blocked for few mins. and those mins. for which user has been locked out will be stored in attribute <static_time_of_user>, so that if again user tries to login then he will face error as still these many seconds are remaining kindly wait for these many seconds before trying login again.
