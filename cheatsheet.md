# Cheatsheet

## Commands
### Store values
    - export {NAME}={VALUE}
### Start sandbox
    - ./sandbox up dev -v
    - ./sandbox up testnet -v
### Enter container
    1. ./sandbox enter algod
    2. cd /data
### Close and clean sandbox
    1. ./sandbox down
    2. ./sandbox clean
### Show store value
    - echo ${NAME}
### Deploy APP
    - goal app create --creator $ONE --approval-prog approval.teal --clear-prog clear.teal --global-ints 3 --global-byteslices 2  --local-ints 0 --local-byteslices 0
### Read states
    - goal app read --global --guess-format --app-id $APP
### Call functions
    - goal app call --app-id $APP -f $ONE --app-arg 'string:request_loan'