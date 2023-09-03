### Commands
1. Store values
- export {NAME}={VALUE}
2. Start sandbox
    - ./sandbox up dev -v
    - ./sandbox up testnet -v
3. Enter container
    1. ./sandbox enter algod
    2. cd /data
4. Close and clean sandbox
    1. ./sandbox down
    2. ./sandbox clean
5. Show store value
    - echo ${NAME}
6. Deploy APP
    - goal app create --creator $ONE --approval-prog approval.teal --clear-prog clear.teal --global-ints 3 --global-byteslices 2  --local-ints 0 --local-byteslices 0
7. Read states
    - goal app read --global --guess-format --app-id $APP
8. Call functions
    - goal app call --app-id $APP -f $ONE --app-arg 'string:request_loan'