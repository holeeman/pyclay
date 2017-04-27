from classes import *
state_call_wait = State()
state_call = State()
state_accept_call = State()
state_check_end = State()
state_rate = State()
state_end = State([Log("program ended.")])

state_call_wait.set([Wait(1), Match('notification.png', Goto(state_end), Comment("not found")), Match('call_accept.png', Goto(state_accept_call), Match('menu_bar.png', Goto(state_call_wait), Log('ad displayed'))), Goto(state_call_wait)])
state_accept_call.set([ClickPic('call_accept.png'), Wait(5), Goto(state_check_end)])
state_check_end.set([Wait(1), Match('call_end.png', Goto(state_rate), Match('call_accept.png', Goto(state_accept_call), Goto(state_check_end)))])
state_rate.set([Match('rate_star.png', ClickPic('rate_star.png', (-40, 40)), Goto(state_call_wait), t=3), Match('rate_confirm.png', ClickPic('rate_confirm.png'), Goto(state_call_wait), t=3), Match('rated.png', Goto(state_call_wait), Goto(state_rate)), Goto(state_call_wait)])
default = state_rate
