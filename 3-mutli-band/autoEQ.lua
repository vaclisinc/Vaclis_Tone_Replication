-- === CONFIG ===
local combos = dofile("/Users/vaclis./Documents/project/vtr/audio_samples/reaper/batch_14.lua")

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

local steps = {-12, -8, -4, 0, 4, 8, 12}

function set_eq_band(track, fxidx, bandidx, freq, gain_db, q, bandtype)
  reaper.TrackFX_SetEQBandEnabled(track, fxidx, bandtype, bandidx, true)
  reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 0, freq, false)
  reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 1, gain_db_to_norm[gain_db], true)
  reaper.TrackFX_SetEQParam(track, fxidx, bandtype, bandidx, 2, q, false)
end
for idx = 1, #combos do
  local vals = combos[idx]
      -- === 0. clean all (reset) ===
      for i = reaper.CountTracks(0) - 1, 0, -1 do
        local track = reaper.GetTrack(0, i)
        reaper.DeleteTrack(track)
      end
  
      -- === 1. import audio ===
      local full_path = input_dir .. "/" .. filename
      reaper.InsertMedia(full_path, 0)
      local item = reaper.GetMediaItem(0, 0)
      if item then
        reaper.SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
      end
  
      -- === 2. EQ 設定 ===
      local track = reaper.GetTrack(0, 0)
      local fxidx = reaper.TrackFX_GetEQ(track, true)
  
      -- Disable all bands first
      for j = 0, 1 do
        for i = 0, 7 do
          reaper.TrackFX_SetEQBandEnabled(track, fxidx, i, j, false)
        end
      end
  
      -- 設定所有 band
      for b = 1, 5 do
          set_eq_band(track, fxidx, b-1, bands[b].freq, vals[b], bands[b].q, bands[b].bandtype)
        end
      -- === 3. 設定檔名（標記所有 band dB） ===
      local outname = string.format("%s_eq_%s_%d_%s_%d_%s_%d_%s_%d_%s_%d.wav",
           filename:gsub("%.wav", ""),
           bands[1].name, vals[1],
           bands[2].name, vals[2],
           bands[3].name, vals[3],
           bands[4].name, vals[4],
           bands[5].name, vals[5]
       )
  
      reaper.GetSetProjectInfo_String(0, "RENDER_FILE", output_dir, true)
      reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN", outname, true)
      reaper.GetSetProjectInfo(0, "RENDER_RANGE", 1, true)
      reaper.GetSetProjectInfo(0, "RENDER_SRCL", 1, true)
      reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 1, true)
  
      -- === 4. Export ===
      reaper.Main_OnCommand(42230, 0)
  end
