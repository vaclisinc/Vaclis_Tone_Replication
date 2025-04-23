local track = reaper.GetTrack(0, 0)
local fxidx = 0  -- 假設你的 ReaEQ 是 FX chain 的第一個
local bandtype = 1  -- 1 = loshelf
local bandidx = 0   -- 第一個 loshelf（通常就只有一條）

local paramtype = 1  -- 1=gain
local paramidx = nil -- paramidx 要這樣組：bandtype, bandidx, paramtype

local retval, bandtype_out, bandidx_out, paramtype_out, normval = 
    reaper.TrackFX_GetEQParam(track, fxidx, bandtype, bandidx, paramtype)

reaper.ShowConsoleMsg(
        string.format("Bandtype:%d (should be 1=loshelf), Bandidx:%d, Paramtype:%d (should be 1=gain), Normval:%.3f\n", 
        bandtype_out, bandidx_out, paramtype_out, normval))


-- We get:
-- real dB  | norm val
-- -12			0.126
-- -11			0.141
-- -10			0.158
-- -9			0.177
-- -8			0.199
-- -7			0.223
-- -6			0.251
-- -5			0.281
-- -4			0.351
-- -3			0.354
-- -2			0.397
-- -1			0.446
-- 0			0.500
-- 1			0.520
-- 2			0.543
-- 3			0.569
-- 4			0.597
-- 5			0.630
-- 6			0.666
-- 7			0.706
-- 8			0.752
-- 9			0.803
-- 10			0.860
-- 11			0.925
-- 12			0.997



