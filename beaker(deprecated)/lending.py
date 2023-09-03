from beaker import *
from pyteal import *

# States in contract 
class LendingState:
    amount_lend = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
    )
    lending_period = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
    )
    interest_rate = GlobalStateValue(
        stack_type=TealType.uint64,
        default=Int(0),
    )
    borrower_address = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes(""),
    )
    lender_address = GlobalStateValue(
        stack_type=TealType.bytes,
        default=Bytes(""),
    )

# Set global state to default value with apply method
app = Application("LendingContract", state=LendingState()).apply(
    unconditional_create_approval, initialize_global_state=True)

# For borrower to make request for the amount to borrow(take address,amount and asset)
@app.external(authorize=Authorize.only(Global.creator_address()))
def request_loan(amount: abi.Uint64) -> Expr:
    return Seq(
        app.state.borrower_address.set(Global.creator_address()),
        app.state.amount_lend.set(amount.get())
    )

@app.external(read_only=True)
def read_loan(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.amount_lend)

# @Subroutine(TealType.none)
# def pay(receiver: Expr, amount: Expr) -> Expr:
#     return InnerTxnBuilder.Execute(
#         {
#             TxnField.type_enum: TxnType.Payment,
#             TxnField.receiver: receiver,
#             TxnField.amount: amount,
#             TxnField.fee: Int(0),  # cover fee with outer txn
#         }
#     )

@app.external
def lend(pay: abi.PaymentTransaction) -> Expr:
    return Seq(
        # Assert(pay.get().amount() == app.state.amount_lend.get()),
        Assert(pay.get().receiver() == app.state.borrower_address.get()),
        app.state.lender_address.set(pay.get().sender()),
        Approve()
    )
