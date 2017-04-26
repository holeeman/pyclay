from simtalk_caller import *
if on_start:
    execute(default, on_start)
else:
    execute(default)

'''
if len(sys.argv) > 1:
    f = sys.argv[1].split("\\")
    f = f[len(f) - 1].replace(".py", "")
    m = __import__(f)
    try:
        attr_list = m.__all__
    except AttributeError:
        attr_list = dir(m)

    for attr in attr_list:
        globals()[attr] = getattr(m, attr)

    if len(sys.argv) > 2:
        execute(eval(sys.argv[2]))
    elif default:
        execute(default)
    else:
        print("No script to execute,s")

else:
    print "Please enter the script."
'''