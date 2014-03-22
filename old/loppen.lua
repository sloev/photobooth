--[[
@title LOPPEN
--]]

local isrec,isvid=get_mode()
if not isrec then
    set_record(1)
	set_lcd_display(0)
end

local focused = false
local try = 1
while not focused and try <= 5 do
    print("Pre-focus attempt " .. try)
    press("shoot_half")
    sleep(1000)
    if get_prop(67) > 0 then
        focused = true
    end
    release("shoot_half")
    sleep(500)
    try = try + 1
end
set_aflock(1)


shoot()
shoot()
shoot()
shoot()

set_aflock(0)
