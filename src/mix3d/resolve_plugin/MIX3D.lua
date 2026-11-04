-- MIX3D: Workspace > Scripts > MIX3D in DaVinci Resolve (anche nella versione gratuita).
-- Legge le clip audio della timeline aperta, le passa a MIX3D e apre il pannello.
local r = resolve or Resolve()
local project = r and r:GetProjectManager():GetCurrentProject()
local tl = project and project:GetCurrentTimeline()
if not tl then print("MIX3D: apri un progetto con una timeline") return end

local function q(s) return '"' .. tostring(s or ""):gsub('[%c"\\]', function(c) return string.format("\\u%04x", c:byte()) end) .. '"' end
local clips = {}
-- tracce audio e anche video: l'audio di camera arriva anche se in timeline c'è solo la clip video
for _, kind in ipairs({"audio", "video"}) do
  for t = 1, tl:GetTrackCount(kind) do
    for _, it in pairs(tl:GetItemListInTrack(kind, t) or {}) do
      local mpi = it:GetMediaPoolItem()
      clips[#clips + 1] = string.format('{"kind":"%s","track":%d,"name":%s,"start_frame":%d,"end_frame":%d,"left_offset":%d,"file_path":%s}',
        kind, t, q(it:GetName()), it:GetStart(), it:GetEnd(), it:GetLeftOffset(), q(mpi and mpi:GetClipProperty("File Path")))
    end
  end
end
local json = string.format('{"project":%s,"timeline":%s,"fps":%s,"start_frame":%d,"clips":[%s]}',
  q(project:GetName()), q(tl:GetName()), q(tl:GetSetting("timelineFrameRate")), tl:GetStartFrame(), table.concat(clips, ","))

local dir = os.getenv("HOME") .. "/.mix3d/resolve"
os.execute('mkdir -p "' .. dir .. '"')
local f = assert(io.open(dir .. "/sessione.json", "w")); f:write(json); f:close()

-- MIX3D aperta: importa subito; chiusa: si avvia e importa la sessione appena scritta
local res = dir .. "/risposta.json"
os.remove(res)
os.execute('/usr/bin/curl -sf -m 120 -X POST http://127.0.0.1:8730/api/resolve/push -o "' .. res .. '"')
local h = io.open(res); local out = h and h:read("*a") or ""; if h then h:close() end
if out == "" then os.execute("open -a MIX3D")
elseif not out:find('"pannello": true', 1, true) then os.execute("open http://127.0.0.1:8730/") end
print("MIX3D: " .. #clips .. " clip inviate da " .. tl:GetName() .. " " .. out)
