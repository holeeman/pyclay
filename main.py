from classes import *

# sign up state
state_check_agree_page = State()
state_agreement = State()
state_check_sign_up_page = State()
state_enter_name = State()
state_check_name = State()
state_enter_others = State()
state_enter_captcha = State()

# tutorial state
state_check_tutorial = State()
state_click_tutorial = State()
state_check_req_call = State()
state_click_req_call = State()

state_goto_video = State()

# call state

# handler state
state_close_ad = State()
state_no_match = State()
state_move_to_dev_id = State()
state_check_dev_id = State()
state_enter_dev_id = State()

state_move = State()
state_detect = State()
state_enter = State()

state_test = State()
state_test2 = State()
state_call_click = State()
state_call_failed = State()
state_go_back_to_simtalk = State()
state_enter_back_to_simtalk = State()

# call end state
state_rate_check = State()
state_rate_click = State()
state_check_candy = State()
state_check_candy2 = State()
state_no_candy = State()

# reboot
state_quit = State()
state_reconfig = State()
state_reboot = State()

# command
state_check_agree_page.set([Wait(0.1), Match('agreement.png', Goto(state_agreement), Match('sign_up.png', Goto(state_enter_name), Goto(state_check_agree_page)))])
state_agreement.set([Click(79, 602), Click(288, 855), Goto(state_check_sign_up_page)])
state_check_sign_up_page.set([Wait(0.1), Match("sign_up.png", Goto(state_enter_name), Goto(state_check_sign_up_page))])
state_enter_name.set([Click(460, 319), KeyDown('backspace'), Wait(0.8), KeyUp('backspace'), Type(random_name(8)), Goto(state_check_name)])
state_check_name.set([Click(512, 328), Wait(1), Match("available.png", Goto(state_enter_others), Goto(state_enter_name))])
state_enter_others.set([Click(388, 466),  Wait(0.2), Click(388, 562), Wait(0.2), Click(388, 547), Wait(0.2), Click(388, 547), Wait(0.2), Click(388, 620), Wait(0.2), Click(388, 620), Goto(state_enter_captcha)])
state_enter_captcha.set([Wait(6), Captcha(), Wait(0.1), KeyDown('enter'), Drag(294, 806, 294, 520), Click(294, 1017) , Wait(3.5), Match('no_match.png', Goto(state_no_match), Goto(state_check_tutorial))])

state_check_tutorial.set([Wait(0.1), Match('tutorial.png', Goto(state_click_tutorial), Goto(state_check_tutorial))])
state_click_tutorial.set([Click(278, 733), Wait(1), Click(278,846), Wait(1), Click(278,846), Wait(1), Click(290, 617), Goto(state_check_req_call)])
state_check_req_call.set([Wait(0.1), Match('req_call.png', Goto(state_click_req_call), Match('video_call.png', Goto(state_test), Goto(state_check_req_call)))])
state_click_req_call.set([Click(408, 650), Goto(state_goto_video)])
state_goto_video.set([Wait(1.5), Click(191, 121), Match('video_call.png', Goto(state_test), Goto(state_check_req_call))])

state_no_match.set([Click(591, 892), Goto(state_move)])

state_move_to_dev_id.set([Drag(17, 580, 744, 562), Goto(state_check_dev_id)])
state_check_dev_id.set([Wait(0.2), Match('dev_id_icon.png', Goto(state_enter_dev_id), Goto(state_move_to_dev_id), 0.7)])
state_enter_dev_id.set([Click(64, 772), Wait(1), Click(484, 432), Wait(0.5), Click(199, 888), Wait(1), Click(590, 951), Goto(state_detect)])

state_move.set([Drag(17, 580, 744, 562), Goto(state_detect)])
state_detect.set([Log('test'), Wait(0.2), Match('simtalk_icon.png', Goto(state_enter), Goto(state_move), 0.7)])
state_enter.set([Log('click'), Click(175, 777), Goto(state_check_agree_page)])

state_test.set([Wait(1), Match('profile.png', Goto(state_call_click), Goto(state_test2))])
state_test2.set([Drag(248, 900, 248, 280, 0, 1), Goto(state_test)])
state_call_click.set([ClickPic('profile.png', (460, 0)), Wait(2), ClickPic('free.png'), Wait(10), Match("connecting.png", Goto(state_call_failed), Match("simtalk.png", Goto(state_call_failed), Goto(state_rate_check)))])
state_call_failed.set([Click(590, 947), Wait(0.5), Click(592, 1000), Drag(400, 968, 0, 968), Click(590, 947), Goto(state_go_back_to_simtalk)])
state_go_back_to_simtalk.set([Drag(17, 580, 744, 562), Wait(0.2), Match('simtalk_icon.png', Goto(state_enter_back_to_simtalk), Goto(state_go_back_to_simtalk))])
state_enter_back_to_simtalk.set([Click(170, 773), Goto(state_check_req_call)])

state_rate_check.set([Wait(0.2), Match('call_end.png', Goto(state_rate_click), Goto(state_rate_check))])
state_rate_click.set([Click(352, 524), Click(223, 707), Goto(state_check_candy)])
state_check_candy.set([Wait(1), Match('profile.png', Goto(state_check_candy2), Goto(state_check_candy))])
state_check_candy2.set([ClickPic('profile.png', (460, 0)), Wait(2), Match('no_candy_req.png', Goto(state_no_candy), ClickPic('free.png'))])
state_no_candy.set([Click(439, 744), Goto(state_quit)])

state_quit.set([Click(524, 126), Wait(1), Click(504, 389), Wait(0.2), Click(306, 583), Wait(2), Click(187, 693), Wait(2), Goto(state_reconfig)])
state_reconfig.set([Click(425, 24), Click(117, 175), Click(825, 426), Click(415, 927), Click(520, 587), Click(1023, 22), Goto(state_reboot)])
state_reboot.set([Click(592, 651), Click(209, 632), Wait(10), Goto(state_move_to_dev_id)])
#l = State()
#l.set([Wait(1), Goto(l)])
#setting(425, 24) feature(117,175) make(825, 426) save(415, 927) ok(520, 587) close(1023, 22)

#state_check_req_call.execute()
#state_goto_video.execute()
#state_agreement.execute()
#state_enter_name.execute()
#state_check_tutorial.execute()
#state_test.execute()
#state_rate_check.execute()
#state_t2.execute()
#state_move_to_dev_id.execute()
#state_reconfig.execute()
#close: Click(496 367)
#state_check_candy.execute()
#state_quit.execute()
#state_go_back_to_simtalk.execute()
#l.execute()
execute(state_quit)
