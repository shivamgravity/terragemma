"""
Audio Briefing & 'Pocket Phone' Voice Component
Renders an offline Web Speech API audio synthesiser so hikers can listen and pocket their screens.
"""

from typing import Optional


HTML_TEMPLATE = """
<div style="
    background: linear-gradient(135deg, #1b3815 0%, #2d5a27 100%);
    color: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 15px 0;
">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">🎧</span>
            <div>
                <h3 style="margin: 0; color: #a3e635; font-size: 18px; font-weight: 600;">__TITLE__</h3>
                <p style="margin: 2px 0 0 0; color: #d1fae5; font-size: 13px;">Screen-Free Mode • Listen & Pocket Your Device</p>
            </div>
        </div>
        __TURNAROUND_BADGE__
    </div>
    
    <div style="background: rgba(0, 0, 0, 0.2); border-left: 3px solid #a3e635; padding: 10px 14px; border-radius: 6px; font-size: 13px; color: #ecfdf5; line-height: 1.5; margin-bottom: 15px; font-style: italic;">
        "__TEXT_TO_SPEAK__"
    </div>

    <div style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
        <button id="playBtn" onclick="playBriefing()" style="
            background: #a3e635;
            color: #14532d;
            border: none;
            padding: 10px 18px;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: transform 0.1s ease, background 0.2s ease;
        ">
            <span id="btnIcon">▶️</span> <span id="btnText">Listen & Pocket Phone</span>
        </button>

        <button id="stopBtn" onclick="stopBriefing()" style="
            background: rgba(255, 255, 255, 0.15);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 10px 16px;
            border-radius: 8px;
            font-size: 13px;
            cursor: pointer;
        ">
            ⏹️ Silence
        </button>

        <div style="display: flex; align-items: center; gap: 6px; color: #d1fae5; font-size: 12px; margin-left: auto;">
            <label for="speedSelect">Voice Pace:</label>
            <select id="speedSelect" style="background: #14532d; color: #fff; border: 1px solid #a3e635; padding: 4px 8px; border-radius: 6px; font-size: 12px;">
                <option value="0.9">Calm (0.9x)</option>
                <option value="1.0" selected>Normal (1.0x)</option>
                <option value="1.15">Brisk (1.15x)</option>
            </select>
        </div>
    </div>

    <script>
        let synth = window.speechSynthesis;
        let currentUtterance = null;

        function playBriefing() {
            if (!synth) {
                alert("Speech synthesis is not supported in this browser.");
                return;
            }
            
            // If speaking, pause/resume
            if (synth.speaking && !synth.paused) {
                synth.pause();
                document.getElementById('btnText').innerText = "Resume Audio";
                document.getElementById('btnIcon').innerText = "▶️";
                return;
            } else if (synth.paused) {
                synth.resume();
                document.getElementById('btnText').innerText = "Pause";
                document.getElementById('btnIcon').innerText = "⏸️";
                return;
            }

            synth.cancel(); // clear queue
            const text = "__CLEAN_TEXT__";
            currentUtterance = new SpeechSynthesisUtterance(text);
            
            const speed = parseFloat(document.getElementById('speedSelect').value);
            currentUtterance.rate = speed;
            currentUtterance.pitch = 1.0;

            // Pick natural voice if available
            const voices = synth.getVoices();
            const englishVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha')));
            if (englishVoice) {
                currentUtterance.voice = englishVoice;
            }

            currentUtterance.onstart = function() {
                document.getElementById('btnText').innerText = "Playing... (Pocket Phone)";
                document.getElementById('btnIcon').innerText = "🔊";
            };

            currentUtterance.onend = function() {
                document.getElementById('btnText').innerText = "Replay Briefing";
                document.getElementById('btnIcon').innerText = "🔄";
            };

            currentUtterance.onerror = function() {
                document.getElementById('btnText').innerText = "Listen & Pocket Phone";
                document.getElementById('btnIcon').innerText = "▶️";
            };

            synth.speak(currentUtterance);
        }

        function stopBriefing() {
            if (synth) {
                synth.cancel();
                document.getElementById('btnText').innerText = "Listen & Pocket Phone";
                document.getElementById('btnIcon').innerText = "▶️";
            }
        }
    </script>
</div>
"""


def render_audio_briefing_html(
    text_to_speak: str,
    title: str = "Trailhead Audio Briefing",
    turnaround_time: str = ""
) -> str:
    """
    Returns an embedded HTML/JS snippet that plays offline speech synthesis
    directly through the user's browser audio output.
    """
    clean_text = text_to_speak.replace('"', '\\"').replace("\n", " ").replace("'", "\\'")
    
    if turnaround_time:
        turnaround_badge = (
            f'<div style="background: rgba(239, 68, 68, 0.25); border: 1px solid #ef4444; '
            f'color: #fca5a5; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold;">'
            f'Turnaround: {turnaround_time}</div>'
        )
    else:
        turnaround_badge = ""

    html = HTML_TEMPLATE.replace("__TITLE__", title)
    html = html.replace("__TURNAROUND_BADGE__", turnaround_badge)
    html = html.replace("__TEXT_TO_SPEAK__", text_to_speak)
    html = html.replace("__CLEAN_TEXT__", clean_text)
    
    return html
