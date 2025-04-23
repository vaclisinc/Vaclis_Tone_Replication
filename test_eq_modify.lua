local track = reaper.GetTrack(0, 0)
local fxidx = 0  -- 假設你的 ReaEQ 是 FX chain 的第一個
local bandtype = 1  -- 1 = loshelf
local bandidx = 0   -- 第一個 loshelf（通常就只有一條）

local paramtype = 1  -- 1=gain
local paramidx = nil -- paramidx 要這樣組：bandtype, bandidx, paramtype

function set_eq_band(track, fxidx, bandidx, freq, gain_db, q, bandtype)

    -- 開啟 band
    reaper.TrackFX_SetEQBandEnabled(track, fxidx, bandtype, bandidx, true)
    -- freq
    reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 0, freq, false)
    --local gain_norm = find_param_for_gain(gain_db)
    reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 1, gain_db, true)
    -- Q
    reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 2, q, false)
    
    --reaper.TrackFX_SetEQBandEnabled(track, fxidx, 2, bandidx, true)
  end

  local track = reaper.GetTrack(0, 0)
  local fxidx = reaper.TrackFX_GetEQ(track, false)
  set_eq_band(track, fxidx, bandidx, 100, 0.251, 3.0, 0)
  
根據 doc，paramidx 其實是組合的，但 REAPER 這裡直接給 function 3個 index
