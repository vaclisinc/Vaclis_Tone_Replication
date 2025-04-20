-- === CONFIG ===
local input_dir = "/Users/vaclis./Documents/project/vtr/audio_samples/reaper/raw"
local output_dir = "/Users/vaclis./Documents/project/vtr/audio_samples/reaper/processed/"
local filename = "Elastic_Lead.wav"
local gain_db = 6
local freq = 300.0

-- === dir ===
local full_path = input_dir .. "/" .. filename
local outname = filename:gsub("%.wav", "") .. "_eq" .. tostring(freq) .. "_" .. (gain_db >= 0 and "+" or "") .. tostring(gain_db) .. ".wav"

-- === 0. clean all (reset) ===
for i = reaper.CountTracks(0) - 1, 0, -1 do
  local track = reaper.GetTrack(0, i)
  reaper.DeleteTrack(track)
end

-- === 1. import audio from dir ===
reaper.GetTrack(0, 0)
reaper.InsertMedia(full_path, 0)
local item = reaper.GetMediaItem(0, 0)
if item then
  reaper.SetMediaItemInfo_Value(item, "D_POSITION", 0.0)
end

-- === 2. adding audio fx effect, e.g. EQ, compressor, limiter, reverb, modulation...


-- === 3. setting output config (dir, filename, channels, range) ===
reaper.GetSetProjectInfo_String(0, "RENDER_FILE", output_dir, true)
reaper.GetSetProjectInfo_String(0, "RENDER_PATTERN",outname , true)   -- 指定檔名 ✅
reaper.GetSetProjectInfo(0, "RENDER_RANGE", 1, true)       -- entire project
reaper.GetSetProjectInfo(0, "RENDER_SRCL", 1, true)        -- master mix 
reaper.GetSetProjectInfo(0, "RENDER_CHANNELS", 1, true)    -- mono

-- === 4. export the processed audio file ===
reaper.Main_OnCommand(42230, 0)


