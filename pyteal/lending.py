from pyteal import *
#time lib for python
"""LendingPlatform"""

def approval_program():
    handle_creation = Seq([
        App.globalPut(Bytes("amount"), Int(0)),
        App.globalPut(Bytes("period"), Int(0)),
        App.globalPut(Bytes("interest"), Int(0)),
        App.globalPut(Bytes("borrow_address"), Bytes("")),
        App.globalPut(Bytes("lend_address"), Bytes("")),
        Return(Int(1))
    ])
    handle_optin = Return(Int(1))
    handle_closeout = Return(Int(0))
    handle_updateapp = Return(Int(0))
    handle_deleteapp = Return(Int(0))


    request_loan = Seq([
        # Check if requester is the creator of contract
        Assert(Global.creator_address() == Txn.sender()),
        # Checking if contract is fresh?
        # Assert(App.globalGet(Bytes("amount")) == Int(0)),
        # Assuming Txn.application_args[1] can get input for amount
        # App.globalPut(Bytes("amount"), Txn.application_args[1]),
        App.globalPut(Bytes("borrow_address"), Txn.sender()),
        Return(Int(1))
    ])



    handle_noop = Seq(
        Assert(Global.group_size() == Int(1)), 
        Cond(
            [Txn.application_args[0] == Bytes("request_loan"), request_loan], 

        )
    )


    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return compileTeal(program, Mode.Application, version=5)


def clear_state_program():
    program = Return(Int(1))
    return compileTeal(program, Mode.Application, version=5)

# Write to file
appFile = open('approval.teal', 'w')
appFile.write(approval_program())
appFile.close()

clearFile = open('clear.teal', 'w')
clearFile.write(clear_state_program())
clearFile.close()