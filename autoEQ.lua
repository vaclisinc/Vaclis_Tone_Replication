-- === CONFIG ===
local input_dir = "/Users/vaclis./Documents/project/vtr/audio_samples/reaper/raw"
local output_dir = "/Users/vaclis./Documents/project/vtr/audio_samples/reaper/processed/"
local filename = "01.wav"

local gain_db_to_norm = {
  [-12]=0.126, [-11]=0.141, [-10]=0.158, [-9]=0.177, [-8]=0.199, [-7]=0.223,
  [-6]=0.251, [-5]=0.281, [-4]=0.315, [-3]=0.354, [-2]=0.397, [-1]=0.446,
  [0]=0.500, [1]=0.520, [2]=0.543, [3]=0.569, [4]=0.597, [5]=0.630,
  [6]=0.666, [7]=0.706, [8]=0.752, [9]=0.803, [10]=0.860, [11]=0.925, [12]=0.997
}

-- 頻率設計
local bands = {
  {freq = 80,    bandtype = 1, q = 1.0, name = "loshelf"},
  {freq = 240,   bandtype = 2, q = 1.0, name = "bell1"},
  {freq = 2500,  bandtype = 2, q = 1.0, name = "bell2"},
  {freq = 4000,  bandtype = 2, q = 1.0, name = "bell3"},
  {freq = 10000, bandtype = 4, q = 1.0, name = "hishelf"}
}

function set_eq_band(track, fxidx, bandidx, freq, gain_db, q, bandtype)
  reaper.TrackFX_SetEQBandEnabled(track, fxidx, bandtype, bandidx, true)
  reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 0, freq, false)
  reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 1, gain_db_to_norm[gain_db], true)
  reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 2, q, false)
end

for b = 1, #bands do
  for gain_db = -12, 12 do

    -- === 0. clean all (reset) ===
    for i = reaper.CountTracks(0) - 1, 0, -1 do
      local track = reaper.GetTrack(0, i)
      reaper.DeleteTrack(track)
    end

    -- === 1. import audio from dir ===
    local full_path = input_dir .. "/" .. filename
    reaper.InsertMedia(full_path, 0)
    local item = reaper.GetMediaItem(0, 0)
    if item then
      reaper.SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
    end

    -- === 2. adding audio fx effect ===
    local track = reaper.GetTrack(0, 0)
    local fxidx = reaper.TrackFX_GetEQ(track, true)

    -- Disable all bands first (clean slate)
    for j = 0, 1 do
      for i = 0, 7 do
        reaper.TrackFX_SetEQBandEnabled(track, fxidx, i, j, false)
      end
    end

    -- 只啟用五個 band，且全部設為 0dB
    for i = 1, #bands do
      local g = (i == b) and gain_db or 0
      set_eq_band(track, fxidx, i-1, bands[i].freq, g, bands[i].q, bands[i].bandtype)
    end

    -- === 3. setting output config (dir, filename, channels, range) ===
    local outname = filename:gsub("%.wav", "") .. "_eq_" .. bands[b].name .. "_" .. tostring(bands[b].freq) .. "_" .. (gain_db >= 0 and "+" or "") .. tostring(gain_db) .. ".wav"
    reaper.GetSetProjectInfo_String(0, "RENDER_FILE", output_dir, true)
    reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN", outname , true)   -- 指定檔名 ✅
    reaper.GetSetProjectInfo(0, "RENDER_RANGE", 1, true)       -- entire project
    reaper.GetSetProjectInfo(0, "RENDER_SRCL", 1, true)        -- master mix 
    reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 1, true)    -- mono

    -- === 4. export the processed audio file ===
    reaper.Main_OnCommand(42230, 0)
  end
end
