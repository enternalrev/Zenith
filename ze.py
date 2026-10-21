"""
𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠 𝗥𝗔𝗜𝗗 𝗕𝗢𝗧 - 𝗣𝗥𝗢𝗙𝗘𝗦𝗦𝗜𝗢𝗡𝗔𝗟 𝗘𝗗𝗜𝗧𝗜𝗢𝗡
𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗯𝘆: 𝗥𝗘𝗩
v6.9 — REV is text-spam only (no rename) + /revs + /srbreak
"""

from instagrapi import Client
import time
import threading
import random
import os
import subprocess
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import requests
import base64
from io import BytesIO
import tempfile
import re
import urllib.parse

try:
    import yt_dlp
    YT_DLP_AVAILABLE = True
except ImportError:
    YT_DLP_AVAILABLE = False

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


class InstagramRaidBot:
    def __init__(self, username=None, password=None, owner_username=None, session_id=None,
                 is_child=False, parent=None):
        self.username = username
        self.password = password
        self.session_id = session_id
        self.owner_username = owner_username.lower() if owner_username else None
        self.client = Client()

        self.is_child = is_child
        self.parent = parent
        self.child_bots = []

        self.bot_delay = 0.001
        self.setup_bot()

        self.messages_sent = 0
        self.command_count = 0
        self.start_time = time.time()
        self.owner_id = None
        self.is_owner_verified = False
        self._last_owner_fetch = 0

        # Multi-GC instance state
        self.raid_instances = {}
        self.spm_instances = {}
        self.tspam_instances = {}
        self.spam_instances = {}
        self.nc_instances = {}
        self.nd_instances = {}
        self.ls_instances = {}
        self.replyraid_targets = {}
        self.sreply_instances = {}
        self.rev_instances = {}
        self.rev_delay = 0.01
        self.rev_break_secs = 2.0

        # TRALL — auto-reply to every message
        self.trall_active = False
        self.trall_text = None
        self.trall_count = 0
        self.trall_start = 0
        self._trall_seen = set()

        # Poll speed (can be changed via /faster and /normal)
        self.poll_interval = 0.1

        self.group_spam_active = False
        self.spm_waiting_for_speed = {}

        self.random_texts = [
"AGAR ME APKI माँ KO NAMAZ PADHTE WAQT CHODUN TO CYA VO SUNNAT HOGA?🤪",
"Teri mummy ko subah 5 baje uthake morning walk pe lejake break fast karake nahLake dholake lunch karake din me sulake raat me utha ke candle light date dinner krke phir Ghar pe lake dheere dheere pom pom krte krte chodunga 🤪🤏🏿 entry 🥵🥵🥵 Teri mummy ko subah 5 baje uthake morning walk pe lejake break fast karake nahLake dholake lunch karake din me sulake raat me utha ke candle light date dinner krke phir Ghar pe lake dheere dheere pom pom krte krte chodunga 🤪🤏🏿 entry 🥵🥵🥵",
"𝙏𝙚𝙧𝙞 𝙢𝙖 𝙠𝙞 𝙘𝙝𝙪𝙩 𝙆𝙖 𝙗𝙞𝙧𝙮𝙖𝙣𝙞 𝙥𝙠𝙖 𝙠𝙚 𝙠𝙝𝙖 𝙟𝙖𝙪𝙣𝙜𝙖😁",
"𝙏𝙐 𝙏𝙊𝙃 𝙈𝙀𝙍𝘼 𝙒𝙊𝙃𝙄 𝙏𝘼𝙏𝙏𝘼 𝙃𝘼𝙄 𝙉𝘼 ? 𝙅𝙄𝙎𝙈𝙀 𝙍𝙊𝙕 𝙆𝙃𝙐𝙅𝙇𝙄 𝙃𝙊𝙏𝙄🤣",
"𝙆𝙞𝙩𝙣𝙖 𝙘𝙝𝙪𝙙𝙚𝙜𝙖 𝘼𝙗 𝙩𝙚𝙧𝙞 𝙢𝙖 𝙠𝙤 𝙗𝙝𝙞 𝙢𝙤𝙠𝙖 𝙙𝙚 𝙘𝙝𝙪𝙙𝙣𝙚 𝙠𝙖🤗",
"Oye dost Teri randi maa ka 👙 aur 300 rupey reh gaye ake le ja Aur teri randi maa v yahi he Konsi maa Dharti maa Fatima Teri Ghar wali maa Ya teri dadi ki maa?",
"Ye dekh Tmkc me camel 🐪 ",
"Oho funny 🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣😂🤣 Ab trima chudegi😱",
"Baune trima cute RND he tri behen ko to slave banake rkha he mene itna attitude kese aara tujhme😂😂😂😂😂💔😂😂💔😂💔😂💔😂💔😂💔💔😂🥀🥀🥀",
"Apki mom itni RND kese he bina pese lie chud jaati😏🥀💔",
"Trima pe atomic bomb gir jae jo tre sarr pe pankha he na vo tut ke tre goto pe gire jo tre ghar pe cylinder he na tre ma jab uspe khana banari ho tb vi fatt jae jo tra nall he na vo leak hojae or tra ghar bhass jae mc",
"ＴＲＩＭＡ　ＣＨＵＤＧＹＩ　ＲＥ😜💜　        ほソがん       ˖ ᡣ𐭩 ⊹ ࣪  ౨ৎ˚₊",
"Beta lund chus bada ho pese duga 😏🥀",
"sun aukat anusar chud tu",
"chl mc apni mom ki kali chut ki mms send kr"
        ]

        # Music
        self.music_active = False
        self.music_queue = []
        self.current_song = None
        self.current_song_info = None
        self.music_volume = 70
        self.playlist = []
        self.repeat_mode = "none"
        self.music_thread = None
        self.audio_cache_dir = tempfile.mkdtemp()
        self.downloading = False
        self.current_audio_path = None
        self.music_status = "Stopped"
        self.current_position = 0
        self.song_duration = 0

        # Owners
        self.additional_owners = set()
        self.user_stats = {}

        self.emoji_list = ["🔥","⚡","💀","👑","🎯","💥","🚀","🎭","✨","🦾","❤️","💀","😈","👾","🤖","🎪","🌈","⚡","🔥","💫"]
        self.heart_emojis = ["❤️","🧡","💛","💚","💙","💜","🖤","🤍","🤎","💗","💓","💖","💕","💞","💘"]
        self.love_emojis = ["😋🩷","😋💕","😋❤️","😋💖","😋💗","😋💝","🩷","💕","❤️","💖","💗","💝"]

        # Executors — SHARED between parent and children
        if parent is not None:
            self.executor = parent.executor
            self.cmd_executor = parent.cmd_executor
            self.fetch_pool = parent.fetch_pool
            self.reply_executor = parent.reply_executor
            self._rename_executor = parent._rename_executor
        else:
            self.executor = ThreadPoolExecutor(max_workers=100)
            self.cmd_executor = ThreadPoolExecutor(max_workers=10)
            self.fetch_pool = ThreadPoolExecutor(max_workers=15)
            self.reply_executor = ThreadPoolExecutor(max_workers=20)
            self._rename_executor = ThreadPoolExecutor(max_workers=20)

        self.last_speed_check = time.time()
        self.messages_last_minute = 0

        self.active_processes = {}
        self.group_rename_delay = 0.1
        self.group_thread_ids = []

        self.processed_messages = set()
        self.thread_last_activity = {}
        self.song_cache = {}
        self._thread_fetch_cooldown = {}

        # Health check
        self.last_health_check = time.time()
        self.consecutive_health_failures = 0
        self._rate_limited_until = 0

        if YT_DLP_AVAILABLE:
            self.ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                'quiet': True, 'no_warnings': True, 'extract_flat': False,
                'outtmpl': os.path.join(self.audio_cache_dir, '%(title)s.%(ext)s'),
                'ignoreerrors': True, 'no_check_certificate': True,
            }

        self._start_cleanup_thread()

        if not is_child:
            print("""
╔══════════════════════════════════════════════════════╗
║           𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠 𝗥𝗔𝗜𝗗 𝗕𝗢𝗧 𝘃𝟲.𝟵             ║
║           𝗣𝗥𝗢𝗙𝗘𝗦𝗦𝗜𝗢𝗡𝗔𝗟 𝗘𝗗𝗜𝗧𝗜𝗢𝗡              ║
║                 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 𝗕𝗬: 𝗥𝗘𝗩                ║
╚══════════════════════════════════════════════════════╝
        """)

    def _start_cleanup_thread(self):
        def cleanup():
            while True:
                try:
                    now = time.time()
                    for tid in [t for t, (_, ts) in self.spm_waiting_for_speed.items() if now - ts > 60]:
                        del self.spm_waiting_for_speed[tid]
                    if len(self.processed_messages) > 5000:
                        self.processed_messages.clear()
                    if len(self.thread_last_activity) > 200:
                        items = sorted(self.thread_last_activity.items(), key=lambda x: str(x[1]))
                        self.thread_last_activity = dict(items[-100:])
                    if len(self._trall_seen) > 3000:
                        self._trall_seen.clear()
                    time.sleep(30)
                except:
                    time.sleep(30)
        threading.Thread(target=cleanup, daemon=True).start()

    def _format_number(self, value):
        if isinstance(value, int):
            return f"{value:,}"
        return str(value)

    def setup_bot(self):
        self.client.delay_range = [self.bot_delay, self.bot_delay + 0.0001]
        self.client.request_timeout = 3
        device_settings = {
            "app_version": "280.0.0.18.96", "android_version": 33,
            "manufacturer": "samsung", "device": "SM-G998B",
            "model": "SM-G998B", "version_code": "280.0.0.18.96"
        }
        settings = {
            "device_settings": device_settings,
            "user_agent": "Instagram 280.0.0.18.96 Android (33/13; 480dpi; 1080x2400; samsung; SM-G998B; y2s; exynos2100; en_US; 448127609)",
            "connection": "keep-alive", "max_retries": 2
        }
        try:
            self.client.set_settings(settings)
        except:
            self.client.set_device(device_settings)
            self.client.set_user_agent(settings.get("user_agent"))

    def login(self):
        try:
            print("⏳ 𝗘𝘀𝘁𝗮𝗯𝗹𝗶𝘀𝗵𝗶𝗻𝗴 𝘀𝗲𝗰𝘂𝗿𝗲 𝗰𝗼𝗻𝗻𝗲𝗰𝘁𝗶𝗼𝗻...")
            if self.session_id:
                print("🔑 𝗨𝘀𝗶𝗻𝗴 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗜𝗗 𝗟𝗼𝗴𝗶𝗻...")
                session_id = str(self.session_id).strip()
                if session_id.startswith('"') and session_id.endswith('"'):
                    session_id = session_id[1:-1]
                elif session_id.startswith("'") and session_id.endswith("'"):
                    session_id = session_id[1:-1]
                try:
                    session_data = json.loads(session_id)
                    if isinstance(session_data, dict):
                        if 'sessionid' in session_data:
                            session_id = session_data['sessionid']
                        elif 'cookies' in session_data and 'sessionid' in session_data['cookies']:
                            session_id = session_data['cookies']['sessionid']
                except:
                    pass
                try:
                    self.client.login_by_sessionid(session_id)
                    account_info = self.client.account_info()
                    self.username = account_info.username
                    print(f"✅ 𝗦𝗲𝘀𝘀𝗶𝗼𝗻 𝗟𝗼𝗴𝗶𝗻 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹!")
                    print(f"👤 𝗔𝗰𝗰𝗼𝘂𝗻𝘁: @{self.username}")
                except:
                    self.client = Client()
                    self.setup_bot()
                    self.client.set_settings({"cookies": {"sessionid": session_id}})
                    account_info = self.client.account_info()
                    self.username = account_info.username
                    print(f"✅ 𝗠𝗮𝗻𝘂𝗮𝗹 𝗖𝗼𝗼𝗸𝗶𝗲 𝗟𝗼𝗴𝗶𝗻 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹!")
                    print(f"👤 𝗔𝗰𝗰𝗼𝘂𝗻𝘁: @{self.username}")
            else:
                if not self.username or not self.password:
                    print("❌ 𝗖𝗿𝗲𝗱𝗲𝗻𝘁𝗶𝗮𝗹𝘀 𝗺𝗶𝘀𝘀𝗶𝗻𝗴!")
                    return False
                self.client.login(self.username, self.password)
                print("✅ 𝗡𝗼𝗿𝗺𝗮𝗹 𝗟𝗼𝗴𝗶𝗻 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹!")

            try:
                bot_info = self.client.account_info()
                print(f"""
📋 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗜𝗡𝗙𝗢
├── Username: @{bot_info.username}
├── Full Name: {bot_info.full_name}
├── Followers: {self._format_number(getattr(bot_info, 'follower_count', 'N/A'))}
└── Following: {self._format_number(getattr(bot_info, 'following_count', 'N/A'))}
""")
            except:
                pass

            if self.owner_username:
                for attempt in range(3):
                    try:
                        user_info = self.client.user_info_by_username(self.owner_username)
                        self.owner_id = user_info.pk
                        self.is_owner_verified = True
                        print(f"✅ Owner verified: @{self.owner_username} (ID: {self.owner_id})")
                        break
                    except Exception as e:
                        print(f"⚠️ Owner fetch attempt {attempt+1}/3 failed: {str(e)[:60]}")
                        time.sleep(1.5)
                else:
                    print(f"⚠️ Could not fetch owner_id at login — will retry at runtime")
                    self.is_owner_verified = False

            self._fetch_group_threads()
            return True
        except Exception as e:
            print(f"❌ 𝗟𝗼𝗴𝗶𝗻 𝗳𝗮𝗶𝗹𝗲𝗱: {str(e)[:100]}")
            return False

    def _fetch_group_threads(self):
        try:
            threads = self.client.direct_threads(amount=20)
            self.group_thread_ids = []
            for thread in threads:
                if hasattr(thread, 'users') and len(thread.users) > 2:
                    self.group_thread_ids.append(thread.id)
            print(f"✅ 𝗙𝗼𝘂𝗻𝗱 {len(self.group_thread_ids)} 𝗴𝗿𝗼𝘂𝗽 𝘁𝗵𝗿𝗲𝗮𝗱𝘀")
        except:
            self.group_thread_ids = []

    # ============ AUTH ============
    def is_owner(self, user_id):
        if self.parent is not None:
            return self.parent.is_owner(user_id)
        if not self.owner_id and self.owner_username:
            now = time.time()
            if now - self._last_owner_fetch > 30:
                self._last_owner_fetch = now
                try:
                    info = self.client.user_info_by_username(self.owner_username)
                    self.owner_id = info.pk
                    print(f"✅ Owner ID re-fetched: @{self.owner_username} -> {self.owner_id}")
                except Exception as e:
                    print(f"⚠️ Owner re-fetch failed: {str(e)[:60]}")
        if not self.owner_id:
            return False
        uid = str(user_id)
        if uid == str(self.owner_id):
            return True
        if uid in self.additional_owners:
            return True
        return False

    # ============ SEND HELPERS ============
    def send_text_nobreak(self, thread_id, text, retry_count=0):
        try:
            if retry_count > 3:
                print(f"❌ SEND FAIL [{str(thread_id)[:8]}] gave up after retries")
                return False
            self.client.direct_send(text, thread_ids=[thread_id])
            self.messages_sent += 1
            return True
        except Exception as e:
            err = str(e).lower()
            errname = type(e).__name__
            retry_keys = ['rate limit', '429', 'too many', 'timeout', 'temporarily',
                          'try again', 'wait', '500', '502', '503', '504', 'network']
            if any(k in err for k in retry_keys) and retry_count < 3:
                time.sleep(0.5 * (retry_count + 1))
                return self.send_text_nobreak(thread_id, text, retry_count + 1)
            print(f"❌ SEND FAIL [{str(thread_id)[:8]}] {errname}: {str(e)[:120]}")
            return False

    def send_text_async(self, thread_id, text):
        try:
            self.reply_executor.submit(self.send_text_nobreak, thread_id, text)
        except:
            try:
                self.executor.submit(self.send_text_nobreak, thread_id, text)
            except:
                pass

    def send_text_reply(self, thread_id, msg_obj, text):
        try:
            if msg_obj is None:
                return self.send_text_nobreak(thread_id, text)
            try:
                self.client.direct_send(text, thread_ids=[thread_id], reply_to_message=msg_obj)
                self.messages_sent += 1
                return True
            except Exception as e:
                print(f"⚠️ reply_to_message failed ({type(e).__name__}), fallback to plain send")
                return self.send_text_nobreak(thread_id, text)
        except Exception as e:
            print(f"❌ reply send failed: {str(e)[:80]}")
            return False

    def send_voice_note(self, thread_id, audio_path, retry_count=0):
        try:
            if retry_count > 2:
                return False
            if not os.path.exists(audio_path):
                return False
            with open(audio_path, 'rb') as f:
                audio_data = f.read()
            self.client.direct_send_voice(audio_data, thread_ids=[thread_id])
            self.messages_sent += 1
            return True
        except Exception as e:
            if "rate limit" in str(e).lower():
                time.sleep(0.5)
                return self.send_voice_note(thread_id, audio_path, retry_count + 1)
            return False

    def send_voice_async(self, thread_id, audio_path):
        self.executor.submit(self.send_voice_note, thread_id, audio_path)

    # ============ BROADCAST ============
    def _broadcast(self, method_name, *args, **kwargs):
        for child in self.child_bots:
            try:
                getattr(child, method_name)(*args, **kwargs)
            except Exception as e:
                print(f"Broadcast {method_name} to @{child.username} failed: {e}")

    def _broadcast_to_children(self, method_name, *args, **kwargs):
        for child in self.child_bots:
            try:
                getattr(child, method_name)(*args, **kwargs)
            except Exception as e:
                print(f"Broadcast {method_name} failed: {str(e)[:50]}")

    # ============ TRALL ============
    def handle_trall(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /trall <text>")
            return
        self.trall_active = True
        self.trall_text = args
        self.trall_count = 0
        self.trall_start = time.time()
        self._trall_seen = set()
        self.send_text_async(thread_id, f"""🔥 𝗧𝗥𝗔𝗟𝗟 𝗔𝗖𝗧𝗜𝗩𝗘
├── Text: "{args[:40]}"
├── Mode: Auto-reply to EVERY message
├── Speed: MAX (0.05s poll = 20x/sec)
├── Only MAIN bot replies
├── Skips: bot msgs + owner + sons
└── Stop: /stroall or /ruk""")

    def handle_stroall(self, thread_id, user_id):
        if not self.trall_active:
            self.send_text_async(thread_id, "ℹ️ 𝗡𝗢 𝗧𝗥𝗔𝗟𝗟 𝗔𝗖𝗧𝗜𝗩𝗘")
            return
        self.trall_active = False
        self.trall_text = None
        self.send_text_async(thread_id, f"🛑 𝗧𝗥𝗔𝗟𝗟 𝗦𝗧𝗢𝗣𝗣𝗘𝗗\n└── Total replies: {self.trall_count}")

    def handle_faster(self, thread_id, user_id):
        old = self.poll_interval
        self.poll_interval = 0.05
        self.send_text_async(thread_id, f"⚡ 𝗙𝗔𝗦𝗧𝗘𝗥 𝗠𝗢𝗗𝗘\n├── Old poll: {old:.3f}s\n├── New poll: 0.05s (20x/sec)\n└── Use /normal to revert")

    def handle_normal(self, thread_id, user_id):
        old = self.poll_interval
        self.poll_interval = 0.1
        self.send_text_async(thread_id, f"⚙️ 𝗡𝗢𝗥𝗠𝗔𝗟 𝗠𝗢𝗗𝗘\n├── Old poll: {old:.3f}s\n├── New poll: 0.1s (10x/sec)")

    # ============ TSPAM ============
    def handle_tspam(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /tspam <name>")
            return
        if thread_id in self.tspam_instances:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️  𝗧𝗦𝗣𝗔𝗠 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /ruk to stop all.")
            return
        self.tspam_instances[thread_id] = {
            'name': args, 'count': 0, 'start': time.time(), 'active': True
        }
        t = threading.Thread(target=self._run_tspam, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'tspam_{thread_id}'] = t
        if not self.is_child:
            self.send_text_async(thread_id, f"🔥 𝗧𝗦𝗣𝗔𝗠 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗\n├── Name: {args}\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚")

    def _run_tspam(self, thread_id):
        inst = self.tspam_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.tspam_instances.get(thread_id) is inst:
            try:
                msg = f"{inst['name']} {random.choice(self.random_texts)}"
                self.executor.submit(self.send_text_nobreak, thread_id, msg)
                inst['count'] += 1
                if inst['count'] % 50 == 0:
                    elapsed = time.time() - inst['start']
                    print(f"🔥 TSpam [{str(thread_id)[:8]}]: {inst['count']} | {inst['count']/max(elapsed,0.1):.1f}/sec")
                time.sleep(0.05)
            except Exception as e:
                print(f"TSPAM error: {e}")
                time.sleep(0.5)
        print(f"✅ TSPAM STOPPED [{str(thread_id)[:8]}]: {inst['count']}")
        if self.tspam_instances.get(thread_id) is inst:
            del self.tspam_instances[thread_id]
        self.active_processes.pop(f'tspam_{thread_id}', None)

    def stop_tspam(self):
        if not self.tspam_instances:
            return "ℹ️  𝗡𝗢 𝗧𝗦𝗣𝗔𝗠\n└── None active."
        total, dur, cnt = 0, 0, 0
        for tid in list(self.tspam_instances.keys()):
            inst = self.tspam_instances.get(tid)
            if not inst:
                continue
            el = time.time() - inst['start']
            total += inst['count']; dur = max(dur, el); cnt += 1
            inst['active'] = False
            del self.tspam_instances[tid]
            self.active_processes.pop(f'tspam_{tid}', None)
        return f"🛑 𝗧𝗦𝗣𝗔𝗠 𝗧𝗘𝗥𝗠𝗜𝗡𝗔𝗧𝗘𝗗\n├── Instances: {cnt}\n├── Total: {total}\n└── Speed: {total/max(dur,0.1):.1f}/sec"

    # ============ NC ============
    def handle_group_rename(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /nc <text>")
            return
        if thread_id in self.nc_instances:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️  𝗡𝗖 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /ruk to stop all.")
            return
        self.nc_instances[thread_id] = {
            'text': args, 'heart_index': 0, 'active': True
        }
        t = threading.Thread(target=self._run_group_rename, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'nc_{thread_id}'] = t
        if not self.is_child:
            self.send_text_async(thread_id, f"🔄 𝗡𝗖 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗\n├── Text: \"{args[:30]}...\"\n├── Speed: {int(1/self.group_rename_delay)}/sec\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚")

    def _do_rename(self, thread_id, new_name):
        try:
            self.client.private_request(
                f"direct_v2/threads/{thread_id}/update_title/",
                {"title": new_name[:50]}
            )
        except:
            pass

    def _run_group_rename(self, thread_id):
        inst = self.nc_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.nc_instances.get(thread_id) is inst:
            try:
                heart = self.heart_emojis[inst['heart_index'] % len(self.heart_emojis)]
                new_name = f"{inst['text']} {heart}"
                self._rename_executor.submit(self._do_rename, thread_id, new_name)
                inst['heart_index'] += 1
                time.sleep(self.group_rename_delay)
            except Exception as e:
                print(f"NC error: {e}")
                time.sleep(self.group_rename_delay)
        if self.nc_instances.get(thread_id) is inst:
            del self.nc_instances[thread_id]
        self.active_processes.pop(f'nc_{thread_id}', None)

    def handle_ncdelay(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, f"⚙️ 𝗡𝗖 𝗗𝗘𝗟𝗔𝗬: {self.group_rename_delay:.3f}s ({int(1/self.group_rename_delay)}/sec)")
            return
        try:
            d = max(0.01, min(2.0, float(args)))
            self.group_rename_delay = d
            if self.parent:
                self.parent.group_rename_delay = d
            if not self.is_child:
                self.send_text_async(thread_id, f"⚙️ 𝗡𝗖 𝗗𝗘𝗟𝗔𝗬: {d:.3f}s ({int(1/d)}/sec)")
        except:
            if not self.is_child:
                self.send_text_async(thread_id, "❌ /ncdelay 0.1")

    # ============ ND ============
    def handle_nd(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /nd <text>")
            return
        if thread_id in self.nd_instances:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️  𝗡𝗗 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /ruk to stop all.")
            return
        self.nd_instances[thread_id] = {
            'text': args, 'count': 0, 'heart_index': 0,
            'start': time.time(), 'active': True
        }
        t = threading.Thread(target=self._run_nd, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'nd_{thread_id}'] = t
        if not self.is_child:
            self.send_text_async(thread_id, f"🔥 𝗡𝗗 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗\n├── Text: {args}\n├── Mode: Rename + Spam\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚")

    def _run_nd(self, thread_id):
        inst = self.nd_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.nd_instances.get(thread_id) is inst:
            try:
                if not self.is_child:
                    heart = self.heart_emojis[inst['heart_index'] % len(self.heart_emojis)]
                    new_name = f"{inst['text']} {heart}"
                    self._rename_executor.submit(self._do_rename, thread_id, new_name)
                inst['heart_index'] += 1
                self.executor.submit(self.send_text_nobreak, thread_id, inst['text'])
                inst['count'] += 1
                if inst['count'] % 50 == 0:
                    el = time.time() - inst['start']
                    print(f"🔥 ND [{str(thread_id)[:8]}]: {inst['count']} | {inst['count']/max(el,0.1):.1f}/sec")
                time.sleep(0.05)
            except Exception as e:
                print(f"ND error: {e}")
                time.sleep(0.2)
        if self.nd_instances.get(thread_id) is inst:
            del self.nd_instances[thread_id]
        self.active_processes.pop(f'nd_{thread_id}', None)

    # ============ LS ============
    def _build_ls_message(self, name):
        love_emoji = random.choice(self.love_emojis)
        hearts = "♥" * 20
        blocks = []
        for i in range(15):
            if i % 2 == 0:
                blocks.append(f"{name} Ｉ ＬＯＶＥ ＹＯＵ ＳＭ{love_emoji}\n{hearts}\n{'／' * 30}")
            else:
                blocks.append(f"{name} ꪶꪮꪜꫀ ꪗꪮꪊ ᦓꪑ{love_emoji}\n{hearts}\n{'/' * 30}")
        return "\n".join(blocks)[:950]

    def handle_ls(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /ls <name>")
            return
        if thread_id in self.ls_instances:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️  𝗟𝗦 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /stoplas or /ruk")
            return
        self.ls_instances[thread_id] = {
            'name': args, 'count': 0, 'start': time.time(),
            'active': True, 'emoji_index': 0,
        }
        t = threading.Thread(target=self._run_ls, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'ls_{thread_id}'] = t
        if not self.is_child:
            self.send_text_async(thread_id, f"💖 𝗟𝗦 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗\n├── Name: {args}\n├── Mode: Rename + Love Spam\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚")

    def _run_ls(self, thread_id):
        inst = self.ls_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.ls_instances.get(thread_id) is inst:
            try:
                if not self.is_child:
                    emoji = self.love_emojis[inst['emoji_index'] % len(self.love_emojis)]
                    new_name = f"{inst['name']} I LOVE YOU SM {emoji}"
                    self._rename_executor.submit(self._do_rename, thread_id, new_name)
                inst['emoji_index'] += 1
                love_msg = self._build_ls_message(inst['name'])
                self.executor.submit(self.send_text_nobreak, thread_id, love_msg)
                inst['count'] += 1
                if inst['count'] % 20 == 0:
                    el = time.time() - inst['start']
                    print(f"💖 LS [{str(thread_id)[:8]}]: {inst['count']} | {inst['count']/max(el,0.1):.1f}/sec")
                time.sleep(0.05)
            except Exception as e:
                print(f"LS error: {e}")
                time.sleep(0.3)
        if self.ls_instances.get(thread_id) is inst:
            del self.ls_instances[thread_id]
        self.active_processes.pop(f'ls_{thread_id}', None)

    def stop_ls(self):
        if not self.ls_instances:
            return "ℹ️  𝗡𝗢 𝗟𝗦 𝗔𝗖𝗧𝗜𝗩𝗘"
        total = sum(i['count'] for i in self.ls_instances.values())
        for tid in list(self.ls_instances.keys()):
            self.ls_instances[tid]['active'] = False
            del self.ls_instances[tid]
            self.active_processes.pop(f'ls_{tid}', None)
        return f"🛑 𝗟𝗦 𝗧𝗘𝗥𝗠𝗜𝗡𝗔𝗧𝗘𝗗\n└── Total: {total}"

    # ============ REPLYRAID ============
    def handle_replyraid(self, thread_id, user_id, args, msg_obj):
        if not args:
            self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── Reply to someone with /replyraid <name>")
            return
        if msg_obj is None:
            self.send_text_async(thread_id, "❌ Use /replyraid AS A REPLY to a message")
            return
        target_user_id = None
        target_username = None
        try:
            replied = getattr(msg_obj, 'replied_to_message', None)
            if replied:
                if isinstance(replied, dict):
                    target_user_id = replied.get('user_id') or replied.get('sender_id')
                    target_username = replied.get('username')
                else:
                    target_user_id = getattr(replied, 'user_id', None)
                    target_username = getattr(replied, 'username', None)
        except Exception:
            pass
        if target_user_id is None:
            try:
                replied = getattr(msg_obj, 'reply', None)
                if replied:
                    target_user_id = getattr(replied, 'user_id', None)
                    target_username = getattr(replied, 'username', None)
            except Exception:
                pass
        if target_user_id is None:
            self.send_text_async(thread_id, "❌ Couldn't detect replied user. Reply to a message properly.")
            return
        target_user_id = str(target_user_id)
        if target_user_id in self.replyraid_targets:
            self.replyraid_targets[target_user_id]['name'] = args
            self.replyraid_targets[target_user_id]['active'] = True
            self.send_text_async(thread_id, f"🎯 𝗥𝗘𝗣𝗟𝗬𝗥𝗔𝗜𝗗 𝗨𝗣𝗗𝗔𝗧𝗘𝗗\n├── Target: {target_username or target_user_id}\n└── Name: {args}")
            return
        self.replyraid_targets[target_user_id] = {
            'name': args, 'count': 0, 'active': True,
            'thread_id': thread_id, 'username': target_username,
        }
        self.send_text_async(thread_id, f"🎯 𝗥𝗘𝗣𝗟𝗬𝗥𝗔𝗜𝗗 𝗔𝗖𝗧𝗜𝗩𝗘\n├── Target: {target_username or target_user_id}\n├── Name: {args}\n└── Bot replies to every message from target")

    def stop_replyraid(self):
        if not self.replyraid_targets:
            return "ℹ️  𝗡𝗢 𝗥𝗘𝗣𝗟𝗬𝗥𝗔𝗜𝗗 𝗔𝗖𝗧𝗜𝗩𝗘"
        total = sum(t['count'] for t in self.replyraid_targets.values())
        count = len(self.replyraid_targets)
        self.replyraid_targets.clear()
        return f"🛑 𝗥𝗘𝗣𝗟𝗬𝗥𝗔𝗜𝗗 𝗦𝗧𝗢𝗣𝗣𝗘𝗗\n├── Targets: {count}\n└── Replies: {total}"

    # ============ SREPLY ============
    def handle_sreply(self, thread_id, user_id, args, msg_obj):
        if not args:
            self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── Reply to someone with /sreply <name>")
            return
        if msg_obj is None:
            self.send_text_async(thread_id, "❌ Use /sreply AS A REPLY to a message")
            return
        target_user_id = None
        target_username = None
        try:
            replied = getattr(msg_obj, 'replied_to_message', None)
            if replied:
                if isinstance(replied, dict):
                    target_user_id = replied.get('user_id') or replied.get('sender_id')
                    target_username = replied.get('username')
                else:
                    target_user_id = getattr(replied, 'user_id', None)
                    target_username = getattr(replied, 'username', None)
        except Exception:
            pass
        if target_user_id is None:
            try:
                replied = getattr(msg_obj, 'reply', None)
                if replied:
                    target_user_id = getattr(replied, 'user_id', None)
                    target_username = getattr(replied, 'username', None)
            except Exception:
                pass
        if target_user_id is None:
            self.send_text_async(thread_id, "❌ Couldn't detect replied user. Reply to a message properly.")
            return
        target_user_id = str(target_user_id)
        reply_target = msg_obj
        try:
            replied_obj = getattr(msg_obj, 'replied_to_message', None)
            if replied_obj is not None and not isinstance(replied_obj, dict):
                reply_target = replied_obj
        except Exception:
            pass
        self.start_sreply_direct(thread_id, args, target_user_id, target_username, reply_target)
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.start_sreply_direct(thread_id, args, target_user_id, target_username, reply_target)
                except Exception as e:
                    print(f"Child sreply broadcast failed: {str(e)[:50]}")
        self.send_text_async(thread_id, f"🔥 𝗦𝗥𝗘𝗣𝗟𝗬 𝗔𝗖𝗧𝗜𝗩𝗘\n├── Target: {target_username or target_user_id}\n├── Name: {args}\n├── Speed: 10 msg/sec × {len(self.child_bots)+1} bots\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚")

    def start_sreply_direct(self, thread_id, name, target_user_id, target_username=None, msg_obj=None):
        if thread_id in self.sreply_instances:
            inst = self.sreply_instances[thread_id]
            inst['name'] = name
            inst['target'] = target_user_id
            inst['target_username'] = target_username
            if msg_obj is not None:
                inst['last_msg_obj'] = msg_obj
            inst['active'] = True
            return
        self.sreply_instances[thread_id] = {
            'name': name,
            'target': target_user_id,
            'target_username': target_username,
            'last_msg_obj': msg_obj,
            'count': 0,
            'start': time.time(),
            'active': True,
        }
        t = threading.Thread(target=self._run_sreply, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'sreply_{thread_id}'] = t

    def _run_sreply(self, thread_id):
        inst = self.sreply_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.sreply_instances.get(thread_id) is inst:
            try:
                msg = f"{inst['name']} {random.choice(self.random_texts)}"
                reply_target = inst.get('last_msg_obj')
                if reply_target is not None:
                    self.executor.submit(self.send_text_reply, thread_id, reply_target, msg)
                else:
                    self.executor.submit(self.send_text_nobreak, thread_id, msg)
                inst['count'] += 1
                if inst['count'] % 50 == 0:
                    el = time.time() - inst['start']
                    print(f"🔥 SReply [{str(thread_id)[:8]}]: {inst['count']} | {inst['count']/max(el,0.1):.1f}/sec")
                time.sleep(0.1)
            except Exception as e:
                print(f"SREPLY error: {e}")
                time.sleep(0.2)
        print(f"✅ SREPLY STOPPED [{str(thread_id)[:8]}]: {inst['count']}")
        if self.sreply_instances.get(thread_id) is inst:
            del self.sreply_instances[thread_id]
        self.active_processes.pop(f'sreply_{thread_id}', None)

    def stop_sreply(self):
        if not self.sreply_instances:
            return "ℹ️  𝗡𝗢 𝗦𝗥𝗘𝗣𝗟𝗬"
        total, dur, cnt = 0, 0, 0
        for tid in list(self.sreply_instances.keys()):
            inst = self.sreply_instances.get(tid)
            if not inst:
                continue
            el = time.time() - inst['start']
            total += inst['count']; dur = max(dur, el); cnt += 1
            inst['active'] = False
            del self.sreply_instances[tid]
            self.active_processes.pop(f'sreply_{tid}', None)
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.stop_sreply()
                except:
                    pass
        return f"🛑 𝗦𝗥𝗘𝗣𝗟𝗬 𝗦𝗧𝗢𝗣𝗣𝗘𝗗\n├── Instances: {cnt}\n├── Total: {total}\n└── Avg: {total/max(dur,0.1):.1f}/sec"

    # ============ REV (TEXT-ONLY, no rename) ============
    def _build_rev_chunks(self, name):
        P1 = "ᴛᴇʀɪ ᴍᴀ ᴋᴏ ᴄʜᴀɴᴅɴɪ ʀᴀᴀᴛ ᴍᴇ ᴄʜᴏᴅᴋᴀʀ ᴅᴀꜰꜰᴀɴ ᴋʀᴜɢᴀ ᴘɪʟʟᴇ😜🩷✓<<<<<<<<<<<<<<<<<<<<<<<"
        P2 = "𝙏𝙀𝙍𝙄 𝙈𝘼 𝙆𝙊 𝘾𝙃𝘼𝙉𝘿𝙉𝙄 𝙍𝘼𝘼𝙏 𝙈𝙀 𝘾𝙃𝙊𝘿𝙆𝘼𝙍 𝘿𝘼𝙁𝙁𝘼𝙉 𝙆𝙍𝙐𝙂𝘼 𝙋𝙄𝙇𝙇𝙀😜🩷✓<<<<<<<<<<<<<<<<<<<<<<<"
        P3 = "𝘛𝘌𝘙𝘐 𝘔𝘈 𝘒𝘖 𝘊𝘏𝘈𝘕𝘋𝘕𝘐 𝘙𝘈𝘈𝘛 𝘔𝘌 𝘊𝘏𝘖𝘋𝘒𝘈𝘙 𝘋𝘈𝘍𝘍𝘈𝘕 𝘒𝘙𝘜𝘎𝘈 𝘗𝘐𝘓𝘓𝘌😜🩷✓<<<<<<<<<<<<<<<<<<<<<<<"
        P4 = "𝙏𝙧𝙞 𝙖𝙪𝙠𝙖𝙩 𝙝𝙖𝙧𝙧 𝙟𝙖𝙜𝙖𝙝 𝙘𝙝𝙪𝙙𝙣𝙚 𝙠𝙞 𝙝𝙞 𝙝𝙚 𝙢𝙘 𝙠𝙚 𝙡𝙖𝙙𝙠𝙚😜"

        sections = [
            "<❤️>  🎀  🍉 ⋆ 🍒\n\n" + "\n\n".join([P1] * 14),
            "<❤️>\n\n𝗣𝗜𝗟𝗟𝗘😜🩷✓<<<<<<<<<<<<<<<<<<<<<<<\n\n" + "\n\n".join([P2] * 10),
            "<💗>\n\n" + "\n\n".join([P3] * 14),
            "<🩵>\n\n" + "\n\n".join([P2] * 14),
            "<💔>\n\n" + P4,
        ]

        MAX_CHUNK = 700
        chunks = []
        for section in sections:
            lines = section.split("\n")
            current = ""
            for line in lines:
                candidate = current + ("\n" if current else "") + line
                if len(candidate) > MAX_CHUNK and current:
                    chunks.append(current)
                    current = line
                else:
                    current = candidate
            if current:
                chunks.append(current)

        final = [f"{name}\n{c}" for c in chunks]
        return final

    def handle_rev(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /rev <name>")
            return
        if thread_id in self.rev_instances:
            self.send_text_async(thread_id, "⚠️  𝗥𝗘𝗩 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /stoprev or /ruk")
            return

        self.start_rev_direct(thread_id, args)

        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.start_rev_direct(thread_id, args)
                except Exception as e:
                    print(f"Child rev broadcast failed: {str(e)[:50]}")

        speed = int(1 / max(self.rev_delay, 0.001))
        self.send_text_async(thread_id, f"🔥 𝗥𝗘𝗩 𝗔𝗖𝗧𝗜𝗩𝗘\n├── Name: {args}\n├── Mode: TEXT spam only (NO rename)\n├── Break: every {self.rev_break_secs:.1f}s\n├── Speed: {speed}/sec\n├── Bots: {len(self.child_bots)+1}\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚")

    def start_rev_direct(self, thread_id, name):
        if thread_id in self.rev_instances:
            inst = self.rev_instances[thread_id]
            inst['name'] = name
            inst['chunks'] = self._build_rev_chunks(name)
            inst['active'] = True
            return

        self.rev_instances[thread_id] = {
            'name': name,
            'chunks': self._build_rev_chunks(name),
            'chunk_index': 0,
            'last_break': time.time(),
            'count': 0,
            'break_count': 0,
            'start': time.time(),
            'active': True,
            'delay': self.rev_delay,
            'break_secs': self.rev_break_secs,
        }
        t = threading.Thread(target=self._run_rev, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'rev_{thread_id}'] = t

    def _run_rev(self, thread_id):
        """TEXT spam only — NO RENAME anywhere in this loop."""
        inst = self.rev_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.rev_instances.get(thread_id) is inst:
            try:
                now = time.time()
                break_secs = inst.get('break_secs', self.rev_break_secs)

                # Break interval: send ONE break message
                if now - inst['last_break'] >= break_secs:
                    inst['last_break'] = now
                    break_text = f"{inst['name']} 𝙏𝙧𝙞 𝙖𝙪𝙠𝙖𝙩 𝙝𝙖𝙧𝙧 𝙟𝙖𝙜𝙖𝙝 𝙘𝙝𝙪𝙙𝙣𝙚 𝙠𝙞 𝙝𝙞 𝙝𝙚 𝙢𝙘 𝙠𝙚 𝙡𝙖𝙙𝙠𝙚😜"
                    self.executor.submit(self.send_text_nobreak, thread_id, break_text)
                    inst['count'] += 1
                    inst['break_count'] += 1
                    time.sleep(inst.get('delay', self.rev_delay))
                    continue

                # PRIMARY: send next TEXT chunk
                chunk = inst['chunks'][inst['chunk_index'] % len(inst['chunks'])]
                inst['chunk_index'] += 1
                self.executor.submit(self.send_text_nobreak, thread_id, chunk)
                inst['count'] += 1

                if inst['count'] % 20 == 0:
                    el = time.time() - inst['start']
                    print(f"🔥 REV [{str(thread_id)[:8]}]: {inst['count']} text sent | "
                          f"{inst['count']/max(el, 0.1):.1f}/sec | breaks={inst['break_count']}")

                time.sleep(inst.get('delay', self.rev_delay))
            except Exception as e:
                print(f"REV error: {e}")
                time.sleep(0.1)

        print(f"✅ REV STOPPED [{str(thread_id)[:8]}]: {inst['count']} total, {inst['break_count']} breaks")
        if self.rev_instances.get(thread_id) is inst:
            del self.rev_instances[thread_id]
        self.active_processes.pop(f'rev_{thread_id}', None)

    def stop_rev(self):
        if not self.rev_instances:
            return "ℹ️  𝗡𝗢 𝗥𝗘𝗩"
        total, breaks, dur, cnt = 0, 0, 0, 0
        for tid in list(self.rev_instances.keys()):
            inst = self.rev_instances.get(tid)
            if not inst:
                continue
            el = time.time() - inst['start']
            total += inst['count']
            breaks += inst.get('break_count', 0)
            dur = max(dur, el)
            cnt += 1
            inst['active'] = False
            del self.rev_instances[tid]
            self.active_processes.pop(f'rev_{tid}', None)
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.stop_rev()
                except Exception:
                    pass
        return f"🛑 𝗥𝗘𝗩 𝗦𝗧𝗢𝗣𝗣𝗘𝗗\n├── Instances: {cnt}\n├── Total: {total}\n├── Breaks: {breaks}\n└── Avg: {total/max(dur,0.1):.1f}/sec"

    def handle_setdelay(self, thread_id, user_id, args):
        if not args:
            cur = int(1 / max(self.rev_delay, 0.001))
            self.send_text_async(thread_id, f"⚙️ 𝗥𝗘𝗩 𝗗𝗘𝗟𝗔𝗬: {self.rev_delay:.4f}s (~{cur}/sec)\n└── Use: /setdelay 0.01 or /revs 0.01")
            return
        try:
            d = max(0.001, min(2.0, float(args)))
            self.rev_delay = d
            if self.parent:
                self.parent.rev_delay = d
            for inst in self.rev_instances.values():
                inst['delay'] = d
            self.send_text_async(thread_id, f"⚙️ 𝗥𝗘𝗩 𝗗𝗘𝗟𝗔𝗬 𝗦𝗘𝗧: {d:.4f}s (~{int(1/d)}/sec)")
        except Exception:
            self.send_text_async(thread_id, "❌ /setdelay 0.001 to 2.0")

    # ============ /revs — set rev speed ============
    def handle_revs(self, thread_id, user_id, args):
        if not args:
            cur = int(1 / max(self.rev_delay, 0.001))
            self.send_text_async(thread_id, f"""⚡ 𝗥𝗘𝗩𝗦 - REV SPEED
├── Current: {self.rev_delay:.4f}s (~{cur}/sec)
└── Use: /revs <seconds>
    ├── /revs 0.001 = ~1000/sec (max theoretical)
    ├── /revs 0.01  = ~100/sec (default)
    ├── /revs 0.05  = ~20/sec
    └── /revs 0.1   = ~10/sec""")
            return
        try:
            d = max(0.001, min(2.0, float(args)))
            self.rev_delay = d
            if self.parent:
                self.parent.rev_delay = d
            for inst in self.rev_instances.values():
                inst['delay'] = d
            self.send_text_async(thread_id, f"⚡ 𝗥𝗘𝗩𝗦 𝗦𝗘𝗧: {d:.4f}s (~{int(1/d)}/sec)")
        except Exception:
            self.send_text_async(thread_id, "❌ /revs 0.001 to 2.0")

    # ============ /srbreak — set rev break seconds (break only, no rename) ============
    def handle_srbreak(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, f"""⏸️ 𝗦𝗥𝗕𝗥𝗘𝗔𝗞 - REV BREAK SECONDS
├── Current: {self.rev_break_secs:.1f}s (break line every N sec)
└── Use: /srbreak <seconds>
    ├── /srbreak 1.0 = break every 1s
    ├── /srbreak 2.0 = break every 2s (default)
    ├── /srbreak 5.0 = break every 5s
    └── /srbreak 10.0 = break every 10s""")
            return
        try:
            s = max(0.5, min(60.0, float(args)))
            self.rev_break_secs = s
            if self.parent:
                self.parent.rev_break_secs = s
            for inst in self.rev_instances.values():
                inst['break_secs'] = s
            self.send_text_async(thread_id, f"⏸️ 𝗦𝗥𝗕𝗥𝗘𝗔𝗞 𝗦𝗘𝗧: {s:.1f}s\n└── Break every {s:.1f}s")
        except Exception:
            self.send_text_async(thread_id, "❌ /srbreak 0.5 to 60.0")

    # ============ GROUPS ============
    def handle_group_list(self, thread_id, user_id):
        if not self.group_thread_ids:
            if not self.is_child:
                self.send_text_async(thread_id, "📋 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽 𝘁𝗵𝗿𝗲𝗮𝗱𝘀 𝗳𝗼𝘂𝗻𝗱")
            return
        text = f"📋 𝗚𝗥𝗢𝗨𝗣𝗦 ({len(self.group_thread_ids)})\n"
        for i, gid in enumerate(self.group_thread_ids[:10]):
            text += f"├── {i+1}. {str(gid)[:12]}...\n"
        if len(self.group_thread_ids) > 10:
            text += f"└── ... and {len(self.group_thread_ids)-10} more"
        if not self.is_child:
            self.send_text_async(thread_id, text)

    def handle_group_raid(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /groupraid <text>")
            return
        if not self.group_thread_ids:
            if not self.is_child:
                self.send_text_async(thread_id, "❌ 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽 𝘁𝗵𝗿𝗲𝗮𝗱𝘀")
            return
        def run():
            sent = 0
            for gid in self.group_thread_ids:
                try:
                    for _ in range(5):
                        self.send_text_nobreak(gid, f"{random.choice(self.emoji_list)} {args}")
                        sent += 1
                    time.sleep(0.1)
                except:
                    continue
            if not self.is_child:
                self.send_text_async(thread_id, f"✅ 𝗚𝗿𝗼𝘂𝗽 𝗥𝗮𝗶𝗱 𝗗𝗼𝗻𝗲\n├── Sent: {sent}\n└── Groups: {len(self.group_thread_ids)}")
        threading.Thread(target=run, daemon=True).start()
        if not self.is_child:
            self.send_text_async(thread_id, f"🚀 𝗚𝗿𝗼𝘂𝗽 𝗥𝗮𝗶𝗱 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")

    def handle_group_spam(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /groupspam <text>")
            return
        if not self.group_thread_ids:
            if not self.is_child:
                self.send_text_async(thread_id, "❌ 𝗡𝗼 𝗴𝗿𝗼𝘂𝗽𝘀")
            return
        self.group_spam_active = True
        def run():
            count = 0
            while self.group_spam_active:
                try:
                    for gid in self.group_thread_ids:
                        if not self.group_spam_active:
                            break
                        self.send_text_nobreak(gid, args)
                        count += 1
                        time.sleep(0.01)
                except:
                    time.sleep(0.1)
        threading.Thread(target=run, daemon=True).start()
        if not self.is_child:
            self.send_text_async(thread_id, f"♾️ 𝗚𝗿𝗼𝘂𝗽 𝗦𝗽𝗮𝗺 𝗦𝘁𝗮𝗿𝘁𝗲𝗱")    # ============ MUSIC ============
    def search_youtube(self, query):
        if not YT_DLP_AVAILABLE:
            return []
        try:
            opts = {'quiet': True, 'no_warnings': True, 'extract_flat': True, 'ignoreerrors': True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(f"ytsearch5:{query}", download=False)
                results = []
                if info and 'entries' in info:
                    for entry in info['entries']:
                        if entry:
                            dur = entry.get('duration', 0)
                            dur_str = f"{dur//60}:{dur%60:02d}" if dur else "N/A"
                            results.append({
                                'title': entry.get('title', 'Unknown'),
                                'url': f"https://youtube.com/watch?v={entry.get('id', '')}",
                                'duration': dur_str,
                                'uploader': entry.get('uploader', 'Unknown'),
                            })
                return results
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def download_song(self, url, thread_id=None):
        if not YT_DLP_AVAILABLE:
            return None
        try:
            self.downloading = True
            if thread_id and not self.is_child:
                self.send_text_async(thread_id, "⏳ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴...")
            with yt_dlp.YoutubeDL(self.ydl_opts.copy()) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    self.downloading = False
                    return None
                base = ydl.prepare_filename(info)
                mp3 = base.replace('.webm', '.mp3').replace('.m4a', '.mp3').replace('.mkv', '.mp3')
                if not os.path.exists(mp3):
                    for f in os.listdir(self.audio_cache_dir):
                        if f.endswith('.mp3') and (info['title'] in f or f.startswith(info.get('id', ''))):
                            mp3 = os.path.join(self.audio_cache_dir, f)
                            break
                if os.path.exists(mp3):
                    self.downloading = False
                    return {'path': mp3, 'title': info.get('title', 'Unknown'),
                            'duration': info.get('duration', 0), 'uploader': info.get('uploader', 'Unknown')}
                self.downloading = False
                return None
        except Exception as e:
            print(f"Download error: {e}")
            self.downloading = False
            return None

    def handle_song(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /song <name>")
            return
        if not YT_DLP_AVAILABLE:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️ yt-dlp not installed")
            return
        if not self.is_child:
            self.send_text_async(thread_id, f"🔍 𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴: {args}")
        def run():
            results = self.search_youtube(args)
            if not results:
                if not self.is_child:
                    self.send_text_async(thread_id, "❌ No results")
                return
            song = results[0]
            if not self.is_child:
                self.send_text_async(thread_id, f"🎵 𝗙𝗼𝘂𝗻𝗱: {song['title']}\n⏳ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴...")
            dl = self.download_song(song['url'], thread_id)
            if dl and os.path.exists(dl['path']):
                self.send_voice_note(thread_id, dl['path'])
                if not self.is_child:
                    self.send_text_async(thread_id, f"✅ {dl['title']}")
            else:
                if not self.is_child:
                    self.send_text_async(thread_id, "❌ Download failed")
        threading.Thread(target=run, daemon=True).start()

    def handle_play(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /play <name>")
            return
        if not YT_DLP_AVAILABLE:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️ yt-dlp not installed")
            return
        self.music_status = "Loading"
        if not self.is_child:
            self.send_text_async(thread_id, f"🔍 𝗦𝗲𝗮𝗿𝗰𝗵𝗶𝗻𝗴: {args}")
        def run():
            results = self.search_youtube(args)
            if not results:
                if not self.is_child:
                    self.send_text_async(thread_id, "❌ No results")
                return
            song = results[0]
            self.current_song = song['title']
            self.current_song_info = song
            self.music_status = "Downloading"
            if not self.is_child:
                self.send_text_async(thread_id, f"🎵 𝗣𝗹𝗮𝘆𝗶𝗻𝗴: {song['title']}")
            dl = self.download_song(song['url'], thread_id)
            if dl and os.path.exists(dl['path']):
                self.current_audio_path = dl['path']
                self.song_duration = dl.get('duration', 0)
                self.music_active = True
                self.music_status = "Playing"
                self.send_voice_note(thread_id, dl['path'])
                if not self.is_child:
                    self.send_text_async(thread_id, f"▶️ 𝗡𝗼𝘄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴: {dl['title']}")
            else:
                self.music_status = "Stopped"
                if not self.is_child:
                    self.send_text_async(thread_id, "❌ Download failed")
        threading.Thread(target=run, daemon=True).start()

    def handle_pause(self, thread_id, user_id):
        if not self.music_active:
            if not self.is_child:
                self.send_text_async(thread_id, "⏸️ 𝗡𝗼 𝗺𝘂𝘀𝗶𝗰 𝗽𝗹𝗮𝘆𝗶𝗻𝗴")
            return
        self.music_active = False
        self.music_status = "Paused"
        if not self.is_child:
            self.send_text_async(thread_id, "⏸️ 𝗣𝗮𝘂𝘀𝗲𝗱")

    def handle_resume(self, thread_id, user_id):
        if not self.current_audio_path:
            if not self.is_child:
                self.send_text_async(thread_id, "▶️ 𝗡𝗼 𝘀𝗼𝗻𝗴")
            return
        self.music_active = True
        self.music_status = "Playing"
        if not self.is_child:
            self.send_text_async(thread_id, f"▶️ 𝗥𝗲𝘀𝘂𝗺𝗲𝗱: {self.current_song}")

    def handle_stop_music(self, thread_id, user_id):
        self.music_active = False
        self.music_status = "Stopped"
        self.current_song = None
        self.current_audio_path = None
        if not self.is_child:
            self.send_text_async(thread_id, "⏹️ 𝗠𝘂𝘀𝗶𝗰 𝗦𝘁𝗼𝗽𝗽𝗲𝗱")

    def handle_volume(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, f"🔊 𝗩𝗼𝗹𝘂𝗺𝗲: {self.music_volume}%")
            return
        try:
            self.music_volume = max(0, min(100, int(args)))
            if not self.is_child:
                self.send_text_async(thread_id, f"🔊 𝗩𝗼𝗹𝘂𝗺𝗲: {self.music_volume}%")
        except:
            if not self.is_child:
                self.send_text_async(thread_id, "❌ /volume 0-100")

    def handle_playlist(self, thread_id, user_id, args):
        if not args:
            if not self.playlist:
                if not self.is_child:
                    self.send_text_async(thread_id, "📋 𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗲𝗺𝗽𝘁𝘆")
                return
            text = f"📋 𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 ({len(self.playlist)}):\n"
            for i, s in enumerate(self.playlist[:10], 1):
                text += f"├── {i}. {s}\n"
            if not self.is_child:
                self.send_text_async(thread_id, text)
            return
        a = args.lower()
        if a.startswith("add "):
            s = args[4:].strip()
            if s:
                self.playlist.append(s)
                if not self.is_child:
                    self.send_text_async(thread_id, f"✅ Added: {s}")
        elif a.startswith("remove "):
            try:
                i = int(args.split(" ")[1]) - 1
                if 0 <= i < len(self.playlist):
                    r = self.playlist.pop(i)
                    if not self.is_child:
                        self.send_text_async(thread_id, f"🗑️ Removed: {r}")
            except:
                pass
        elif a == "clear":
            self.playlist = []
            if not self.is_child:
                self.send_text_async(thread_id, "🗑️ Cleared")
        elif a == "shuffle":
            random.shuffle(self.playlist)
            if not self.is_child:
                self.send_text_async(thread_id, "🔀 Shuffled")
        elif a == "play":
            if self.playlist:
                self.handle_play(thread_id, user_id, self.playlist.pop(0))
        else:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /playlist [add/remove/clear/shuffle/play]")

    def handle_repeat(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, f"🔁 𝗥𝗲𝗽𝗲𝗮𝘁: {self.repeat_mode}")
            return
        if args.lower() in ["none", "one", "all"]:
            self.repeat_mode = args.lower()
            if not self.is_child:
                self.send_text_async(thread_id, f"🔁 𝗥𝗲𝗽𝗲𝗮𝘁: {self.repeat_mode}")
        else:
            if not self.is_child:
                self.send_text_async(thread_id, "❌ /repeat [none/one/all]")

    def handle_lyrics(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /lyrics <song>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, f"📝 𝗟𝘆𝗿𝗶𝗰𝘀: {args}\n[Simulated]")

    def handle_music(self, thread_id, user_id, args):
        if not self.is_child:
            self.send_text_async(thread_id, f"""
🎵 𝗠𝘂𝘀𝗶𝗰 𝗦𝘁𝗮𝘁𝘂𝘀
├── Status: {self.music_status}
├── Current: {self.current_song or 'None'}
├── Volume: {self.music_volume}%
├── Playlist: {len(self.playlist)}
└── Repeat: {self.repeat_mode}
""")

    def handle_music_search(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /musicsearch <query>")
            return
        if not YT_DLP_AVAILABLE:
            if not self.is_child:
                self.send_text_async(thread_id, "⚠️ yt-dlp missing")
            return
        def run():
            results = self.search_youtube(args)
            if not results:
                if not self.is_child:
                    self.send_text_async(thread_id, "❌ No results")
                return
            text = f"🔍 {args}\n\n"
            for i, s in enumerate(results[:5], 1):
                text += f"{i}. {s['title']}\n   ⏱️ {s['duration']}\n"
            if not self.is_child:
                self.send_text_async(thread_id, text[:2000])
        threading.Thread(target=run, daemon=True).start()

    def handle_queue(self, thread_id, user_id):
        if not self.is_child:
            if not self.music_queue:
                self.send_text_async(thread_id, "📋 Queue empty")
                return
            text = f"📋 Queue ({len(self.music_queue)}):\n"
            for i, s in enumerate(self.music_queue[:5], 1):
                text += f"{i}. {s}\n"
            self.send_text_async(thread_id, text)

    def handle_skip(self, thread_id, user_id):
        if not self.music_queue:
            if not self.is_child:
                self.send_text_async(thread_id, "⏭️ Queue empty")
            return
        self.handle_play(thread_id, user_id, self.music_queue.pop(0))

    def handle_loop(self, thread_id, user_id):
        self.repeat_mode = "one" if self.repeat_mode == "none" else "none"
        if not self.is_child:
            self.send_text_async(thread_id, f"🔁 Loop: {self.repeat_mode}")

    def handle_genre(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /genre <genre>")
            return
        genres = {
            "pop": "🎵 Pop - Catchy, mainstream",
            "rock": "🎸 Rock - Guitar-driven",
            "hip-hop": "🎤 Hip-Hop - Rhythmic, urban",
            "jazz": "🎷 Jazz - Smooth, soulful",
            "classical": "🎼 Classical - Orchestral",
            "electronic": "🎹 Electronic - Synthesized",
            "rb": "🎵 R&B - Soulful, emotional",
            "country": "🪕 Country - Storytelling",
        }
        g = args.lower()
        if not self.is_child:
            self.send_text_async(thread_id, genres.get(g, f"❌ '{g}' not in: {', '.join(genres.keys())}"))

    def handle_cover(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /cover <song>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, f"🖼️ Cover: {args}\n└── 🎵 Enjoy!")

    # ============ SPM ============
    def handle_spm_command(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 𝗨𝗦𝗔𝗚𝗘\n└── /spm <text>")
            return
        self.spm_waiting_for_speed[thread_id] = (args, time.time())
        if not self.is_child:
            self.send_text_async(thread_id, f"""
⚡ 𝗦𝗣𝗠 𝗦𝗣𝗘𝗘𝗗 𝗦𝗘𝗟𝗘𝗖𝗧𝗜𝗢𝗡
├── Text: "{args[:30]}..."
├── Reply with "fast" or "slow"
└── Timeout: 60s
""")

    def handle_speed_selection(self, thread_id, user_id, choice):
        if thread_id not in self.spm_waiting_for_speed:
            return
        text, _ = self.spm_waiting_for_speed[thread_id]
        del self.spm_waiting_for_speed[thread_id]
        choice = choice.lower()
        if choice not in ["fast", "slow"]:
            self.send_text_async(thread_id, "❌ Invalid speed")
            return
        result = self.start_spm(thread_id, text, choice)
        self.send_text_async(thread_id, result)

    def start_spm(self, thread_id, text, mode="fast"):
        if thread_id in self.spm_instances:
            return "⚠️  𝗦𝗣𝗠 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /ruk to stop all."
        self.spm_instances[thread_id] = {
            'message': text, 'count': 0, 'start': time.time(),
            'mode': mode, 'active': True
        }
        t = threading.Thread(target=self._run_spm, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'spm_{thread_id}'] = t
        return f"🚀 𝗦𝗣𝗠 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗\n├── Mode: {mode.upper()}\n├── Speed: {'35' if mode=='fast' else '20'}/sec\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚"

    def _run_spm(self, thread_id):
        inst = self.spm_instances.get(thread_id)
        if not inst:
            return
        bs, delay = (7, 0.028) if inst['mode'] == "fast" else (4, 0.05)
        while inst.get('active') and self.spm_instances.get(thread_id) is inst:
            try:
                for _ in range(bs):
                    if not inst.get('active'):
                        break
                    self.executor.submit(self.send_text_nobreak, thread_id, inst['message'])
                    inst['count'] += 1
                    if inst['count'] % 100 == 0:
                        el = time.time() - inst['start']
                        print(f"🚀 SPM [{str(thread_id)[:8]}]: {inst['count']} | {inst['count']/max(el,0.1):.1f}/sec")
                if not inst.get('active'):
                    break
                time.sleep(delay)
            except Exception as e:
                print(f"SPM error: {e}")
                time.sleep(0.5)
        if self.spm_instances.get(thread_id) is inst:
            del self.spm_instances[thread_id]
        self.active_processes.pop(f'spm_{thread_id}', None)

    def stop_spm(self):
        if not self.spm_instances:
            return "ℹ️  𝗡𝗢 𝗦𝗣𝗠"
        total, dur, cnt = 0, 0, 0
        for tid in list(self.spm_instances.keys()):
            inst = self.spm_instances.get(tid)
            if not inst:
                continue
            el = time.time() - inst['start']
            total += inst['count']; dur = max(dur, el); cnt += 1
            inst['active'] = False
            del self.spm_instances[tid]
            self.active_processes.pop(f'spm_{tid}', None)
        return f"🛑 𝗦𝗣𝗠 𝗧𝗘𝗥𝗠𝗜𝗡𝗔𝗧𝗘𝗗\n├── Instances: {cnt}\n├── Total: {total}\n└── Avg: {total/max(dur,0.1):.1f}/sec"

    # ============ RUK ============
    def ruk_all(self):
        stopped, total = [], 0
        for name, coll in [
            ("RAID", self.raid_instances), ("SPM", self.spm_instances),
            ("TSPAM", self.tspam_instances), ("SPAM", self.spam_instances),
        ]:
            if coll:
                for tid, inst in list(coll.items()):
                    inst['active'] = False
                    total += inst.get('count', 0)
                coll.clear()
                stopped.append(name)
        if self.nc_instances:
            for inst in list(self.nc_instances.values()):
                inst['active'] = False
            self.nc_instances.clear()
            stopped.append("NC")
        if self.nd_instances:
            for inst in list(self.nd_instances.values()):
                inst['active'] = False
                total += inst.get('count', 0)
            self.nd_instances.clear()
            stopped.append("ND")
        if self.ls_instances:
            for inst in list(self.ls_instances.values()):
                inst['active'] = False
                total += inst.get('count', 0)
            self.ls_instances.clear()
            stopped.append("LS")
        if self.replyraid_targets:
            for inst in list(self.replyraid_targets.values()):
                total += inst.get('count', 0)
            self.replyraid_targets.clear()
            stopped.append("REPLYRAID")
        if self.sreply_instances:
            for inst in list(self.sreply_instances.values()):
                inst['active'] = False
                total += inst.get('count', 0)
            self.sreply_instances.clear()
            stopped.append("SREPLY")
        if self.rev_instances:
            for inst in list(self.rev_instances.values()):
                inst['active'] = False
                total += inst.get('count', 0)
            self.rev_instances.clear()
            stopped.append("REV")
        if self.trall_active:
            self.trall_active = False
            self.trall_text = None
            total += self.trall_count
            stopped.append("TRALL")
        if self.group_spam_active:
            self.group_spam_active = False
            stopped.append("GROUP SPAM")
        if self.music_active:
            self.music_active = False
            self.music_status = "Stopped"
            stopped.append("MUSIC")
        self.spm_waiting_for_speed.clear()
        self.active_processes.clear()
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.ruk_all()
                except:
                    pass
        if not stopped:
            return "ℹ️  𝗡𝗢 𝗔𝗖𝗧𝗜𝗩𝗘 𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗘𝗦"
        return f"🛑 𝗥𝗨𝗞 - 𝗔𝗟𝗟 𝗞𝗜𝗟𝗟𝗘𝗗\n├── Stopped: {', '.join(stopped)}\n├── Instances: {len(stopped)}\n└── Msgs: {total}"

    def stop_all(self):
        return self.ruk_all()

    # ============ RAID ============
    def start_counted_raid(self, thread_id, count, text):
        if thread_id in self.raid_instances:
            return "⚠️  𝗥𝗔𝗜𝗗 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /ruk to stop all."
        try:
            count = int(count)
            if count <= 0:
                return "❌ Count must be > 0"
            if count > 5000:
                return "⚠️ Max 5000"
        except:
            return "❌ /raid <count> <text>"
        self.raid_instances[thread_id] = {
            'message': text, 'count': 0, 'max': count,
            'start': time.time(), 'active': True
        }
        t = threading.Thread(target=self._run_ultrafast_raid, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'raid_{thread_id}'] = t
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.start_counted_raid(thread_id, count, text)
                except:
                    pass
        return f"🚀 𝗥𝗔𝗜𝗗 𝗦𝗧𝗔𝗥𝗧𝗘𝗗\n├── Target: {count} × {len(self.child_bots)+1} bot(s)\n├── Text: \"{text[:30]}...\"\n└── Status: 𝗔𝗖𝗧𝗜𝗩𝗘"

    def _run_ultrafast_raid(self, thread_id):
        inst = self.raid_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.raid_instances.get(thread_id) is inst and inst['count'] < inst['max']:
            try:
                n = min(5, inst['max'] - inst['count'])
                for _ in range(n):
                    if not inst.get('active'):
                        break
                    self.executor.submit(self.send_text_nobreak, thread_id, inst['message'])
                    inst['count'] += 1
                if inst['count'] % 50 == 0:
                    el = time.time() - inst['start']
                    print(f"⚡ Raid [{str(thread_id)[:8]}]: {inst['count']}/{inst['max']} | {inst['count']/max(el,0.1):.1f}/sec")
                time.sleep(0.01)
            except:
                time.sleep(0.1)
        if self.raid_instances.get(thread_id) is inst:
            del self.raid_instances[thread_id]
        self.active_processes.pop(f'raid_{thread_id}', None)

    def stop_raid(self):
        if not self.raid_instances:
            return "ℹ️  𝗡𝗢 𝗥𝗔𝗜𝗗"
        total, dur, cnt = 0, 0, 0
        for tid in list(self.raid_instances.keys()):
            inst = self.raid_instances.get(tid)
            if not inst:
                continue
            el = time.time() - inst['start']
            total += inst['count']; dur = max(dur, el); cnt += 1
            inst['active'] = False
            del self.raid_instances[tid]
            self.active_processes.pop(f'raid_{tid}', None)
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.stop_raid()
                except:
                    pass
        return f"🛑 𝗥𝗔𝗜𝗗 𝗦𝗧𝗢𝗣𝗣𝗘𝗗\n├── Instances: {cnt}\n├── Sent: {total}\n└── Avg: {total/max(dur,0.1):.1f}/sec"

    # ============ SPAM ============
    def start_spam_loop(self, thread_id, text):
        if not text:
            return "📝 /spam <text>"
        if thread_id in self.spam_instances:
            return "⚠️  𝗦𝗣𝗔𝗠 𝗔𝗖𝗧𝗜𝗩𝗘 𝗜𝗡 𝗧𝗛𝗜𝗦 𝗖𝗛𝗔𝗧\n└── /ruk to stop all."
        self.spam_instances[thread_id] = {
            'message': text, 'count': 0, 'start': time.time(), 'active': True
        }
        t = threading.Thread(target=self._run_spam_loop, args=(thread_id,), daemon=True)
        t.start()
        self.active_processes[f'spam_{thread_id}'] = t
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.start_spam_loop(thread_id, text)
                except:
                    pass
        return f"♾️  𝗦𝗣𝗔𝗠 𝗔𝗖𝗧𝗜𝗩𝗔𝗧𝗘𝗗\n├── Text: \"{text[:30]}...\"\n├── Bots: {len(self.child_bots)+1}\n└── Status: 𝗥𝗨𝗡𝗡𝗜𝗡𝗚"

    def _run_spam_loop(self, thread_id):
        inst = self.spam_instances.get(thread_id)
        if not inst:
            return
        while inst.get('active') and self.spam_instances.get(thread_id) is inst:
            try:
                for _ in range(3):
                    if not inst.get('active'):
                        break
                    self.executor.submit(self.send_text_nobreak, thread_id, inst['message'])
                    inst['count'] += 1
                    if inst['count'] % 100 == 0:
                        el = time.time() - inst['start']
                        print(f"♾️  Spam [{str(thread_id)[:8]}]: {inst['count']} | {inst['count']/max(el,0.1):.1f}/sec")
                time.sleep(0.005)
            except:
                time.sleep(0.5)
        if self.spam_instances.get(thread_id) is inst:
            del self.spam_instances[thread_id]
        self.active_processes.pop(f'spam_{thread_id}', None)

    def stop_spam_loop(self):
        if not self.spam_instances:
            return "ℹ️  𝗡𝗢 𝗦𝗣𝗔𝗠"
        total, dur, cnt = 0, 0, 0
        for tid in list(self.spam_instances.keys()):
            inst = self.spam_instances.get(tid)
            if not inst:
                continue
            el = time.time() - inst['start']
            total += inst['count']; dur = max(dur, el); cnt += 1
            inst['active'] = False
            del self.spam_instances[tid]
            self.active_processes.pop(f'spam_{tid}', None)
        if not self.is_child:
            for child in self.child_bots:
                try:
                    child.stop_spam_loop()
                except:
                    pass
        return f"🛑 𝗦𝗣𝗔𝗠 𝗧𝗘𝗥𝗠𝗜𝗡𝗔𝗧𝗘𝗗\n├── Instances: {cnt}\n├── Total: {total}\n└── Avg: {total/max(dur,0.1):.1f}/sec"

    # ============ EFFECT COMMANDS ============
    def handle_swipe(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /swipe <text>")
            return
        def run():
            for i in range(5):
                self.send_text_nobreak(thread_id, "░"*i + " " + args + " " + "░"*(4-i))
                time.sleep(0.15)
        threading.Thread(target=run, daemon=True).start()

    def handle_autospam(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /autospam <text>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, self.start_spam_loop(thread_id, args))
        else:
            self.start_spam_loop(thread_id, args)

    def handle_hybrid(self, thread_id, user_id, args):
        if not args or '|' not in args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /hybrid t1|t2|t3")
            return
        texts = [t.strip() for t in args.split('|') if t.strip()]
        def run():
            for _ in range(50):
                self.send_text_nobreak(thread_id, random.choice(texts))
                time.sleep(0.05)
        threading.Thread(target=run, daemon=True).start()
        if not self.is_child:
            self.send_text_async(thread_id, f"🎭 𝗛𝗬𝗕𝗥𝗜𝗗 𝗦𝗧𝗔𝗥𝗧𝗘𝗗 ({len(texts)} variants × 50)")

    def handle_massdm(self, thread_id, user_id, args):
        if not args or ' ' not in args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /massdm @u1,@u2 message")
            return
        users_part, msg = args.split(' ', 1)
        users = [u.strip().replace('@','') for u in users_part.split(',') if u.strip()]
        def run():
            sent = 0
            for u in users:
                try:
                    info = self.client.user_info_by_username(u)
                    t = self.client.direct_thread(info.pk)
                    self.client.direct_send(msg, thread_ids=[t.id])
                    sent += 1
                    time.sleep(0.3)
                except:
                    continue
            if not self.is_child:
                self.send_text_async(thread_id, f"✅ MassDM: {sent}/{len(users)}")
        threading.Thread(target=run, daemon=True).start()
        if not self.is_child:
            self.send_text_async(thread_id, f"📨 MassDM to {len(users)} users")

    def handle_ghost(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /ghost <text>")
            return
        def run():
            for _ in range(5):
                self.send_text_nobreak(thread_id, f"👻 {args}")
                time.sleep(0.05)
                self.send_text_nobreak(thread_id, "👻")
                time.sleep(0.05)
        threading.Thread(target=run, daemon=True).start()

    def handle_matrix(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /matrix <text>")
            return
        def run():
            for _ in range(5):
                self.send_text_nobreak(thread_id, "01"*5 + " " + args + " " + "10"*5)
                time.sleep(0.1)
        threading.Thread(target=run, daemon=True).start()

    def handle_glitch(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /glitch <text>")
            return
        g = "".join(random.choice([c, "▓", "▒", "░", c.upper()]) for c in args)
        if not self.is_child:
            self.send_text_async(thread_id, f"⚡ {g} ⚡")

    def handle_echo(self, thread_id, user_id, args):
        if not args or ' ' not in args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /echo <n> <text>")
            return
        try:
            n, txt = args.split(' ', 1)
            n = min(int(n), 20)
            def run():
                for i in range(n):
                    self.send_text_nobreak(thread_id, f"[{i+1}/{n}] {txt}")
                    time.sleep(0.05)
            threading.Thread(target=run, daemon=True).start()
        except:
            if not self.is_child:
                self.send_text_async(thread_id, "❌ /echo 5 hello")

    def handle_rotate(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /rotate <text>")
            return
        def run():
            for _ in range(3):
                for i in range(len(args)):
                    self.send_text_nobreak(thread_id, args[i:] + args[:i])
                    time.sleep(0.05)
        threading.Thread(target=run, daemon=True).start()

    def handle_rainbow(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /rainbow <text>")
            return
        rainbow = "".join(f"🔴{c}" if i%6==0 else f"🟠{c}" if i%6==1 else f"🟡{c}" if i%6==2 else f"🟢{c}" if i%6==3 else f"🔵{c}" if i%6==4 else f"🟣{c}" for i,c in enumerate(args))
        if not self.is_child:
            self.send_text_async(thread_id, rainbow)

    def handle_bounce(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /bounce <text>")
            return
        def run():
            for pad in [0,2,4,2,0]:
                self.send_text_nobreak(thread_id, " "*pad + args)
                time.sleep(0.1)
        threading.Thread(target=run, daemon=True).start()

    def handle_morse(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /morse <text>")
            return
        morse = {
            'a':'.-','b':'-...','c':'-.-.','d':'-..','e':'.','f':'..-.','g':'--.',
            'h':'....','i':'..','j':'.---','k':'-.-','l':'.-..','m':'--','n':'-.',
            'o':'---','p':'.--.','q':'--.-','r':'.-.','s':'...','t':'-','u':'..-',
            'v':'...-','w':'.--','x':'-..-','y':'-.--','z':'--..'
        }
        if not self.is_child:
            self.send_text_async(thread_id, "📡 " + ' '.join(morse.get(c.lower(), '') for c in args))

    def handle_leet(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /leet <text>")
            return
        trans = str.maketrans('aAeEiIoOsStT', '443311005577')
        if not self.is_child:
            self.send_text_async(thread_id, args.translate(trans))

    def handle_spongebob(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /spongebob <text>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, "".join(c.upper() if i%2==0 else c.lower() for i,c in enumerate(args)))

    def handle_zalgo(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /zalgo <text>")
            return
        marks = ["\u0301","\u0302","\u0303","\u0304","\u0305","\u0306","\u0307","\u0308"]
        if not self.is_child:
            self.send_text_async(thread_id, "".join(c + "".join(random.choice(marks) for _ in range(2)) for c in args))

    def handle_vibe(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /vibe <text>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, f"{random.choice(self.emoji_list)} {args.upper()} {random.choice(self.emoji_list)}")

    def handle_capslock(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /capslock <text>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, "".join(c.upper() if random.random()>0.5 else c.lower() for c in args))

    def handle_mock(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /mock <text>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, "".join(c.upper() if i%2==0 else c.lower() for i,c in enumerate(args)))

    def handle_say(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /say <text>")
            return
        if not self.is_child:
            self.send_text_async(thread_id, args)

    def handle_delete(self, thread_id, user_id, args):
        if not self.is_child:
            self.send_text_async(thread_id, "🗑️ (Simulated)")

    def handle_seen(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /seen @user")
            return
        if not self.is_child:
            self.send_text_async(thread_id, f"👁️ {args} - Last seen: Just now (simulated)")

    def handle_hack(self, thread_id, user_id, args):
        if not args:
            if not self.is_child:
                self.send_text_async(thread_id, "📝 /hack @user")
            return
        def run():
            for s in ["Initializing...","Bypassing firewall...","Decrypting...","Accessing DB...","Complete!"]:
                self.send_text_nobreak(thread_id, f"💻 {s}")
                time.sleep(0.3)
            self.send_text_nobreak(thread_id, f"✅ {args} hacked (simulation)")
        threading.Thread(target=run, daemon=True).start()    # ============ BOT MANAGEMENT (main owner only) ============
    def handle_addbot(self, thread_id, user_id, args):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬")
            return
        if not args:
            self.send_text_async(thread_id, """📝 𝗨𝗦𝗔𝗚𝗘
├── /addbot <sessionid>
├── /addbot <username>:<password>
└── /botlist - Show all bots""")
            return
        self.send_text_async(thread_id, "⏳ 𝗟𝗼𝗴𝗴𝗶𝗻𝗴 𝗶𝗻 𝗻𝗲𝘄 𝗯𝗼𝘁...")
        def do_add():
            try:
                if ':' in args and not (args.startswith('"') or args.startswith("'")):
                    user, pwd = args.split(':', 1)
                    child = InstagramRaidBot(
                        username=user.strip(),
                        password=pwd.strip(),
                        owner_username=self.owner_username,
                        is_child=True,
                        parent=self
                    )
                else:
                    child = InstagramRaidBot(
                        owner_username=self.owner_username,
                        session_id=args.strip(),
                        is_child=True,
                        parent=self
                    )
                if not child.login():
                    self.send_text_async(thread_id, "❌ 𝗟𝗼𝗴𝗶𝗻 𝗳𝗮𝗶𝗹𝗲𝗱")
                    return
                if not hasattr(self, '_processed_lock'):
                    self._processed_lock = threading.Lock()
                child.processed_messages = self.processed_messages
                child.thread_last_activity = self.thread_last_activity
                child._thread_fetch_cooldown = self._thread_fetch_cooldown
                child._processed_lock = self._processed_lock
                child.additional_owners = self.additional_owners
                child.replyraid_targets = self.replyraid_targets
                child.sreply_instances = self.sreply_instances
                child.rev_instances = self.rev_instances
                child.spm_waiting_for_speed = self.spm_waiting_for_speed
                child.owner_id = self.owner_id
                child.poll_interval = self.poll_interval
                child.rev_delay = self.rev_delay
                child.rev_break_secs = self.rev_break_secs
                self.child_bots.append(child)
                t = threading.Thread(target=child.run, daemon=True)
                t.start()
                self.send_text_async(thread_id, f"""✅ 𝗕𝗢𝗧 𝗔𝗗𝗗𝗘𝗗
├── Username: @{child.username}
├── Total Bots: {len(self.child_bots)+1}
└── Status: 𝗢𝗡𝗟𝗜𝗡𝗘""")
            except Exception as e:
                self.send_text_async(thread_id, f"❌ Error: {str(e)[:80]}")
        threading.Thread(target=do_add, daemon=True).start()

    def handle_removebot(self, thread_id, user_id, args):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬")
            return
        if not args:
            self.send_text_async(thread_id, "📝 /removebot @username")
            return
        target = args.replace('@','').strip().lower()
        for child in list(self.child_bots):
            if child.username and child.username.lower() == target:
                try:
                    child.ruk_all()
                except:
                    pass
                self.child_bots.remove(child)
                self.send_text_async(thread_id, f"✅ 𝗥𝗘𝗠𝗢𝗩𝗘𝗗: @{child.username}\n└── Remaining: {len(self.child_bots)+1}")
                return
        self.send_text_async(thread_id, f"❌ Bot not found: @{target}")

    def handle_botlist(self, thread_id, user_id):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬")
            return
        text = f"🤖 𝗕𝗢𝗧 𝗟𝗜𝗦𝗧 ({len(self.child_bots)+1} total)\n"
        text += f"├── 🥇 @{self.username} (MAIN)\n"
        for i, child in enumerate(self.child_bots, 1):
            text += f"├── {i}. @{child.username}\n"
        text += f"└── /addbot to add more"
        self.send_text_async(thread_id, text)

    # ============ SON MANAGEMENT (main owner only) ============
    def add_additional_owner(self, thread_id, user_id, target_username):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗡𝗟𝗬 𝗠𝗔𝗜𝗡 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗔𝗗𝗗 𝗦𝗢𝗡𝗦")
            return
        if not target_username or not target_username.strip():
            self.send_text_async(thread_id, "📝 /addson @username")
            return
        target = target_username.replace('@', '').strip().lower()
        try:
            info = self.client.user_info_by_username(target)
            tid = str(info.pk)
            if tid in self.additional_owners:
                self.send_text_async(thread_id, f"ℹ️  @{target} is already a son")
                return
            self.additional_owners.add(tid)
            self.send_text_async(thread_id, f"✅ 𝗔𝗗𝗗𝗘𝗗 𝗦𝗢𝗡\n└── @{target} (ID: {tid})")
        except:
            self.send_text_async(thread_id, f"❌ User not found: @{target}")

    def remove_additional_owner(self, thread_id, user_id, target_username):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗡𝗟𝗬 𝗠𝗔𝗜𝗡 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗥𝗘𝗠𝗢𝗩𝗘 𝗦𝗢𝗡𝗦")
            return
        if not target_username or not target_username.strip():
            self.send_text_async(thread_id, "📝 /removeson @username")
            return
        target = target_username.replace('@', '').strip().lower()
        try:
            info = self.client.user_info_by_username(target)
            tid = str(info.pk)
            if tid in self.additional_owners:
                self.additional_owners.discard(tid)
                self.send_text_async(thread_id, f"✅ 𝗥𝗘𝗠𝗢𝗩𝗘𝗗 𝗦𝗢𝗡\n└── @{target}")
            else:
                self.send_text_async(thread_id, f"ℹ️  @{target} is not a son")
        except:
            self.send_text_async(thread_id, f"❌ User not found: @{target}")

    def handle_son_list(self, thread_id, user_id):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗡𝗟𝗬 𝗠𝗔𝗜𝗡 𝗢𝗪𝗡𝗘𝗥 𝗖𝗔𝗡 𝗩𝗜𝗘𝗪 𝗦𝗢𝗡 𝗟𝗜𝗦𝗧")
            return
        if not self.additional_owners:
            self.send_text_async(thread_id, "📋 𝗡𝗢 𝗦𝗢𝗡𝗦 𝗬𝗘𝗧\n└── /addson @user")
            return
        text = f"👥 𝗦𝗢𝗡𝗦 ({len(self.additional_owners)})\n"
        for i, sid in enumerate(list(self.additional_owners), 1):
            text += f"├── {i}. {sid}\n"
        text += "└── /removeson @user to remove"
        self.send_text_async(thread_id, text[:2000])

    def set_delay(self, delay_seconds):
        try:
            d = max(0.001, min(2.0, float(delay_seconds)))
            self.bot_delay = d
            self.client.delay_range = [d, d + 0.0001]
            return f"⚙️ 𝗗𝗘𝗟𝗔𝗬: {d:.3f}s (~{int(1/d)}/sec)"
        except:
            return "❌ /delay 0.001 to 2.0"

    # ============ INFO / FUN COMMANDS ============
    def handle_ping(self, thread_id, user_id):
        self.command_count += 1
        trall_status = "ON" if self.trall_active else "OFF"
        self.send_text_async(thread_id, f"🏓 𝗣𝗢𝗡𝗚!\n├── Uptime: {time.time()-self.start_time:.1f}s\n├── Commands: {self.command_count}\n├── Messages: {self.messages_sent}\n├── Poll: {self.poll_interval:.3f}s\n├── TRALL: {trall_status}\n├── REV Delay: {self.rev_delay:.4f}s\n├── REV Break: {self.rev_break_secs:.1f}s\n└── Bots: {len(self.child_bots)+1}")

    def handle_status(self, thread_id, user_id):
        self.command_count += 1
        uptime = time.time() - self.start_time
        speed = self.messages_sent / uptime if uptime > 0 else 0
        bot_names = f"@{self.username}"
        for c in self.child_bots:
            bot_names += f", @{c.username}"
        trall_status = "🟢 ON" if self.trall_active else "⚫ OFF"
        trall_text_short = (self.trall_text or '')[:30]
        self.send_text_async(thread_id, f"""
╔═══════════════════════════════════════╗
║        𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗨𝗦 𝗥𝗘𝗣𝗢𝗥𝗧            ║
╠═══════════════════════════════════════╣
║ 🤖 Bots ({len(self.child_bots)+1}): {bot_names[:40]}
║ 👑 Owner: @{self.owner_username or 'N/A'}
║ 👥 Sons: {len(self.additional_owners)}
╠═══════════════════════════════════════╣
║ ⚡ Speed: {speed:.1f}/sec
║ 📨 Messages: {self.messages_sent}
║ ⏱️  Uptime: {uptime:.0f}s
║ 📊 Commands: {self.command_count}
║ 🔄 Poll: {self.poll_interval:.3f}s
╠═══════════════════════════════════════╣
║ 🔥 Raid: {len(self.raid_instances)}
║ ♾️  Spam: {len(self.spam_instances)}
║ 🚀 SPM: {len(self.spm_instances)}
║ 🔥 TSpam: {len(self.tspam_instances)}
║ 🔄 NC: {len(self.nc_instances)}
║ 🔥 ND: {len(self.nd_instances)}
║ 💖 LS: {len(self.ls_instances)}
║ 🎯 ReplyRaid: {len(self.replyraid_targets)}
║ 🔥 SReply: {len(self.sreply_instances)}
║ 💥 REV: {len(self.rev_instances)} ({self.rev_delay:.3f}s/msg)
╠═══════════════════════════════════════╣
║ 📢 TRALL: {trall_status} ({self.trall_count} sent)
║    Text: "{trall_text_short}"
╠═══════════════════════════════════════╣
║ 🎵 Music: {'ON' if self.music_active else 'OFF'}
║ ⚙️  NC Delay: {self.group_rename_delay:.3f}s
║ ⏸️  REV Break: {self.rev_break_secs:.1f}s
╚═══════════════════════════════════════╝
""")

    def handle_help(self, thread_id, user_id):
        self.command_count += 1
        help_text = """
╔═══════════════════════════════════════╗
║        𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦 𝗠𝗘𝗡𝗨                ║
╠═══════════════════════════════════════╣
║ 🛑 𝗠𝗔𝗦𝗧𝗘𝗥 𝗦𝗧𝗢𝗣                     ║
║ /ruk  /stop  /stopall  /kill          ║
╠═══════════════════════════════════════╣
║ 📢 𝗧𝗥𝗔𝗟𝗟 (auto-reply ALL)            ║
║ ├── /trall <text>  - Reply EVERY msg  ║
║ ├── /stroall       - Stop trall       ║
║ ├── /faster        - Max poll speed   ║
║ └── /normal        - Normal poll      ║
╠═══════════════════════════════════════╣
║ 🤖 𝗕𝗢𝗧 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧 (owner)          ║
║ ├── /addbot <session|user:pass>       ║
║ ├── /removebot @user                  ║
║ └── /botlist                          ║
╠═══════════════════════════════════════╣
║ 💖 𝗟𝗢𝗩𝗘 𝗦𝗣𝗔𝗠 / 𝗥𝗘𝗣𝗟𝗬𝗥𝗔𝗜𝗗          ║
║ ├── /ls <name>                        ║
║ ├── /stoplas                          ║
║ ├── /replyraid <name> (reply)         ║
║ └── /stopreplyraid                    ║
╠═══════════════════════════════════════╣
║ 🔥 𝗦𝗥𝗘𝗣𝗟𝗬                          ║
║ ├── /sreply <name> (reply) 10/sec     ║
║ └── /stopsreply                       ║
╠═══════════════════════════════════════╣
║ 💥 𝗥𝗘𝗩 (TEXT SPAM ONLY, NO RENAME) ║
║ ├── /rev <name>                       ║
║ ├── /stoprev                          ║
║ ├── /revs <sec>      - Speed          ║
║ ├── /setdelay <sec>  - Speed (alias)  ║
║ └── /srbreak <sec>   - Break interval ║
╠═══════════════════════════════════════╣
║ 🔄 𝗥𝗘𝗡𝗔𝗠𝗘 + 𝗦𝗣𝗔𝗠                  ║
║ ├── /nc <text>                        ║
║ ├── /ncdelay <sec>                    ║
║ └── /nd <text>                        ║
╠═══════════════════════════════════════╣
║ ⚡ 𝗣𝗘𝗥𝗙𝗢𝗥𝗠𝗔𝗡𝗖𝗘                    ║
║ ├── /raid <n> <text>                  ║
║ ├── /spam <text>                      ║
║ ├── /spm <text>                       ║
║ ├── /tspam <name>                     ║
║ ├── /autospam /hybrid /massdm         ║
║ ├── /stopraid /stopspam /stopspm      ║
║ ├── /stoptspam                        ║
║ └── /delay <sec>                      ║
╠═══════════════════════════════════════╣
║ 🎵 𝗠𝗨𝗦𝗜𝗖                             ║
║ /song /play /pause /resume            ║
║ /stopmusic /volume /playlist          ║
║ /repeat /lyrics /music                ║
║ /musicsearch /queue /skip /loop       ║
║ /genre /cover                         ║
╠═══════════════════════════════════════╣
║ 📋 𝗚𝗥𝗢𝗨𝗣𝗦                            ║
║ /grouplist /groupraid /groupspam      ║
╠═══════════════════════════════════════╣
║ 🎮 𝗘𝗙𝗙𝗘𝗖𝗧𝗦 & 𝗙𝗨𝗡                  ║
║ /swipe /ghost /matrix /glitch         ║
║ /echo /rotate /rainbow /bounce        ║
║ /morse /leet /spongebob /zalgo        ║
║ /vibe /capslock /mock /say /hack      ║
║ /ping /status /info /uptime /stats    ║
║ /emoji /meme /joke /flood /quote      ║
║ /dice /coin /calc /roll /rps /8ball   ║
║ /fact /trivia /weather /love          ║
║ /ascii /binary /reverse /upper        ║
║ /lower /len /replace /count           ║
║ /shuffle /palindrome /vowels          ║
║ /anagram /prime /fibonacci            ║
║ /clear /typing /secret                ║
╠═══════════════════════════════════════╣
║ 👑 𝗢𝗪𝗡𝗘𝗥 (main only)                 ║
║ /addson /removeson /sonlist           ║
║ /owner /ownerstatus /broadcast        ║
╚═══════════════════════════════════════╝
"""
        self.send_text_async(thread_id, help_text)

    def handle_owner_status(self, thread_id, user_id):
        uptime = time.time() - self.start_time
        speed = self.messages_sent / uptime if uptime > 0 else 0
        self.send_text_async(thread_id, f"""
👑 𝗢𝗪𝗡𝗘𝗥 𝗦𝗧𝗔𝗧𝗨𝗦
├── Main: @{self.owner_username or 'N/A'}
├── Sons: {len(self.additional_owners)}
├── Bots: {len(self.child_bots)+1}
├── Speed: {speed:.1f}/sec
├── Messages: {self.messages_sent}
├── Poll: {self.poll_interval:.3f}s
├── TRALL: {'ON' if self.trall_active else 'OFF'}
├── REV Delay: {self.rev_delay:.4f}s
├── REV Break: {self.rev_break_secs:.1f}s
├── Active procs: {len(self.active_processes)}
└── Music: {'ON' if self.music_active else 'OFF'}
""")

    def handle_owner_check(self, thread_id, user_id):
        if self.is_owner(user_id):
            level = 'MAIN' if str(user_id) == str(self.owner_id) else 'SON'
            self.send_text_async(thread_id, f"✅ 𝗢𝗪𝗡𝗘𝗥 𝗩𝗘𝗥𝗜𝗙𝗜𝗘𝗗\n├── Level: {level}\n└── Access: FULL")
        else:
            self.send_text_async(thread_id, "⛔ 𝗔𝗖𝗖𝗘𝗦𝗦 𝗗𝗘𝗡𝗜𝗘𝗗")

    def handle_info(self, thread_id, user_id):
        self.send_text_async(thread_id, f"""
🤖 𝗕𝗢𝗧 𝗜𝗡𝗙𝗢
├── Main: @{self.username}
├── Bots: {len(self.child_bots)+1}
├── Owner: @{self.owner_username or 'N/A'}
├── Sons: {len(self.additional_owners)}
├── Messages: {self.messages_sent}
├── Commands: {self.command_count}
├── Groups: {len(self.group_thread_ids)}
├── Delay: {self.bot_delay:.3f}s
├── NC Delay: {self.group_rename_delay:.3f}s
├── REV Delay: {self.rev_delay:.4f}s
├── REV Break: {self.rev_break_secs:.1f}s
├── Poll: {self.poll_interval:.3f}s
└── Version: 6.9
""")

    def handle_emoji(self, thread_id, args, user_id):
        if not args:
            self.send_text_async(thread_id, "📝 /emoji <text>")
            return
        e = random.choice(self.emoji_list)
        self.send_text_async(thread_id, f"{e} {args.upper()} {e}")

    def handle_meme(self, thread_id, user_id):
        self.send_text_async(thread_id, f"🎭 {random.choice(['Bot too OP!','On fire 🔥','RIP servers','Bot king 👑','Lightning fast ⚡'])}")

    def handle_joke(self, thread_id, user_id):
        self.send_text_async(thread_id, f"😂 {random.choice(['Bot needed space!','Always online!','Never gonna give you up!'])}")

    def handle_flood(self, thread_id, args, user_id):
        if not args:
            self.send_text_async(thread_id, "📝 /flood <text>")
            return
        def run():
            for i in range(5):
                self.send_text_nobreak(thread_id, f"{i+1}. {args}")
                time.sleep(0.05)
        threading.Thread(target=run, daemon=True).start()

    def handle_time(self, thread_id, user_id):
        self.send_text_async(thread_id, f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")

    def handle_uptime(self, thread_id, user_id):
        u = int(time.time() - self.start_time)
        self.send_text_async(thread_id, f"⏳ Uptime: {u//3600}h {(u%3600)//60}m {u%60}s")

    def handle_stats(self, thread_id, user_id):
        uid = str(user_id)
        self.user_stats[uid] = self.user_stats.get(uid, 0) + 1
        rank = 'REGULAR' if self.user_stats[uid] < 10 else 'ACTIVE' if self.user_stats[uid] < 50 else 'POWER USER'
        self.send_text_async(thread_id, f"📊 Commands: {self.user_stats[uid]}\nRank: {rank}")

    def handle_dice(self, thread_id, user_id):
        self.send_text_async(thread_id, f"🎲 Rolled: {random.randint(1,6)}")

    def handle_coin(self, thread_id, user_id):
        self.send_text_async(thread_id, f"🪙 {random.choice(['HEADS','TAILS'])}")

    def handle_calc(self, thread_id, args, user_id):
        if not args:
            self.send_text_async(thread_id, "📝 /calc <expr>")
            return
        try:
            if not all(c in "0123456789+-*/.() " for c in args):
                raise ValueError()
            self.send_text_async(thread_id, f"🧮 {args} = {eval(args)}")
        except:
            self.send_text_async(thread_id, "❌ Invalid expression")

    def handle_about(self, thread_id, user_id):
        self.send_text_async(thread_id, "🤖 Instagram Raid Bot v6.9\nDev: 𝗥𝗘𝗩\nREV is TEXT SPAM ONLY (no rename) | /revs + /srbreak | Multi-Bot | TRALL | Fast Poll | Auth Gate")

    def handle_cmds(self, thread_id, user_id):
        self.send_text_async(thread_id, "📋 Use /help for full list")

    def handle_speed(self, thread_id, user_id):
        u = time.time() - self.start_time
        s = self.messages_sent / u if u > 0 else 0
        self.send_text_async(thread_id, f"⚡ Speed: {s:.1f}/sec\nTotal: {self.messages_sent}\nDelay: {self.bot_delay:.3f}s\nPoll: {self.poll_interval:.3f}s\nREV Delay: {self.rev_delay:.4f}s\nREV Break: {self.rev_break_secs:.1f}s")

    def handle_chatid(self, thread_id, user_id):
        self.send_text_async(thread_id, f"💬 {thread_id}")

    def handle_userid(self, thread_id, user_id):
        self.send_text_async(thread_id, f"👤 {user_id}")

    def handle_myinfo(self, thread_id, user_id):
        try:
            info = self.client.user_info(user_id)
            self.send_text_async(thread_id, f"👤 @{info.username}\n{info.full_name}\nID: {info.pk}")
        except:
            self.send_text_async(thread_id, "❌ Couldn't fetch")

    def handle_profile(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /profile @user")
            return
        try:
            uname = args.replace('@','').strip()
            info = self.client.user_info_by_username(uname)
            self.send_text_async(thread_id, f"📊 @{info.username}\nFollowers: {self._format_number(getattr(info,'follower_count',0))}\nPrivate: {'Yes' if info.is_private else 'No'}")
        except:
            self.send_text_async(thread_id, f"❌ @{args} not found")

    def handle_sendmsg(self, thread_id, user_id, args):
        if not args or ' ' not in args:
            self.send_text_async(thread_id, "📝 /sendmsg @user message")
            return
        target, msg = args.split(' ', 1)
        try:
            info = self.client.user_info_by_username(target.replace('@','').strip())
            t = self.client.direct_thread(info.pk)
            self.client.direct_send(msg, thread_ids=[t.id])
            self.send_text_async(thread_id, f"✅ Sent to @{target}")
        except:
            self.send_text_async(thread_id, "❌ Failed")

    def handle_broadcast(self, thread_id, user_id, args):
        if str(user_id) != str(self.owner_id):
            self.send_text_async(thread_id, "⛔ 𝗢𝗪𝗡𝗘𝗥 𝗢𝗡𝗟𝗬")
            return
        if not args:
            self.send_text_async(thread_id, "📝 /broadcast <text>")
            return
        self.send_text_async(thread_id, "⚠️ Broadcast starting...")

    def handle_followers(self, thread_id, user_id, args):
        uname = args.replace('@','').strip() if args else self.username
        try:
            info = self.client.user_info_by_username(uname)
            self.send_text_async(thread_id, f"📈 @{info.username}\nFollowers: {self._format_number(getattr(info,'follower_count',0))}")
        except:
            self.send_text_async(thread_id, f"❌ @{uname}")

    def handle_posts(self, thread_id, user_id, args):
        uname = args.replace('@','').strip() if args else self.username
        try:
            info = self.client.user_info_by_username(uname)
            self.send_text_async(thread_id, f"📸 @{info.username}\nPosts: {self._format_number(getattr(info,'media_count',0))}")
        except:
            self.send_text_async(thread_id, f"❌ @{uname}")

    def handle_quote(self, thread_id, user_id):
        self.send_text_async(thread_id, f"💭 {random.choice(['Do great work. - Jobs','Innovation distinguishes. - Jobs','Strive to be of value. - Einstein'])}")

    def handle_weather(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /weather city")
            return
        self.send_text_async(thread_id, f"🌤️ {args.title()}: {random.choice(['Sunny','Cloudy','Rainy'])} {random.randint(10,35)}°C")

    def handle_trivia(self, thread_id, user_id):
        q = random.choice([{"q":"Capital of France?","a":"Paris"},{"q":"Largest ocean?","a":"Pacific"},{"q":"Symbol for gold?","a":"Au"}])
        self.send_text_async(thread_id, f"❓ {q['q']}\nAnswer: {q['a']}")

    def handle_fact(self, thread_id, user_id):
        self.send_text_async(thread_id, f"📚 {random.choice(['Honey never spoils.','Octopuses have 3 hearts.','A day on Venus > a year.'])}")

    def handle_8ball(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /8ball question")
            return
        self.send_text_async(thread_id, f"🎱 {random.choice(['Yes','No','Maybe','Definitely','Uncertain','Ask later'])}")

    def handle_roll(self, thread_id, user_id, args):
        try:
            sides = max(2, min(100, int(args) if args else 6))
        except:
            sides = 6
        self.send_text_async(thread_id, f"🎲 {random.randint(1,sides)} (1-{sides})")

    def handle_rps(self, thread_id, user_id, args):
        if not args or args.lower() not in ['rock','paper','scissors']:
            self.send_text_async(thread_id, "📝 /rps rock|paper|scissors")
            return
        bc = random.choice(['rock','paper','scissors'])
        uc = args.lower()
        result = "TIE" if uc==bc else ("WIN" if (uc=='rock' and bc=='scissors') or (uc=='paper' and bc=='rock') or (uc=='scissors' and bc=='paper') else "LOSE")
        self.send_text_async(thread_id, f"✊ You: {uc} | Bot: {bc} | {result}")

    def handle_love(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /love name1 name2")
            return
        self.send_text_async(thread_id, f"💖 {args}: {random.randint(1,100)}%")

    def handle_ascii(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /ascii text")
            return
        t = args.upper()
        self.send_text_async(thread_id, f"╔{'═'*(len(t)+2)}╗\n║ {t} ║\n╚{'═'*(len(t)+2)}╝")

    def handle_binary(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /binary text")
            return
        self.send_text_async(thread_id, ' '.join(format(ord(c),'08b') for c in args[:20]))

    def handle_reverse(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /reverse text")
            return
        self.send_text_async(thread_id, args[::-1])

    def handle_upper(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /upper text")
            return
        self.send_text_async(thread_id, args.upper())

    def handle_lower(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /lower text")
            return
        self.send_text_async(thread_id, args.lower())

    def handle_len(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /len text")
            return
        self.send_text_async(thread_id, f"Length: {len(args)}")

    def handle_replace(self, thread_id, user_id, args):
        if not args or args.count(' ') < 2:
            self.send_text_async(thread_id, "📝 /replace old new text")
            return
        p = args.split(' ', 2)
        self.send_text_async(thread_id, p[2].replace(p[0], p[1]))

    def handle_count(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /count text")
            return
        self.send_text_async(thread_id, f"Words: {len(args.split())}\nChars: {len(args)}")

    def handle_shuffle(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /shuffle text")
            return
        w = args.split()
        random.shuffle(w)
        self.send_text_async(thread_id, ' '.join(w))

    def handle_palindrome(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /palindrome text")
            return
        t = args.lower().replace(' ','')
        self.send_text_async(thread_id, f"{'✅' if t==t[::-1] else '❌'} {args}")

    def handle_vowels(self, thread_id, user_id, args):
        if not args:
            self.send_text_async(thread_id, "📝 /vowels text")
            return
        v = sum(1 for c in args.lower() if c in 'aeiou')
        self.send_text_async(thread_id, f"Vowels: {v}\nConsonants: {len(args)-v}")

    def handle_anagram(self, thread_id, user_id, args):
        if not args or ' ' not in args:
            self.send_text_async(thread_id, "📝 /anagram word1 word2")
            return
        w1, w2 = args.split(' ', 1)
        self.send_text_async(thread_id, f"{'✅' if sorted(w1.lower())==sorted(w2.lower()) else '❌'} Anagram")

    def handle_prime(self, thread_id, user_id, args):
        try:
            n = int(args)
            p = n > 1 and all(n%i != 0 for i in range(2, int(n**0.5)+1))
            self.send_text_async(thread_id, f"{n}: {'✅ Prime' if p else '❌ Not prime'}")
        except:
            self.send_text_async(thread_id, "❌ /prime number")

    def handle_fibonacci(self, thread_id, user_id, args):
        try:
            n = max(1, min(20, int(args) if args else 10))
        except:
            n = 10
        fib = [0,1]
        for i in range(2,n):
            fib.append(fib[-1]+fib[-2])
        self.send_text_async(thread_id, ', '.join(map(str, fib[:n])))

    def handle_clear(self, thread_id, user_id):
        self.send_text_async(thread_id, "🧹 Clearing...")

    def handle_typing(self, thread_id, user_id):
        self.send_text_async(thread_id, "✍️ Typing...")
        time.sleep(1)
        self.send_text_async(thread_id, "✅ Done")

    def handle_secret(self, thread_id, user_id):
        self.send_text_async(thread_id, f"🔒 {random.choice(['Bot watching 👀','Owner loves pizza 🍕','Shhh 🤫'])}")

    # ============ MESSAGE PROCESSING ============
    def _try_mark_processed(self, key):
        if not hasattr(self, '_processed_lock'):
            self._processed_lock = threading.Lock()
        with self._processed_lock:
            if key in self.processed_messages:
                return False
            self.processed_messages.add(key)
            if len(self.processed_messages) > 5000:
                self.processed_messages.clear()
            return True

    def _fetch_and_process(self, thread_id):
        try:
            messages = self.client.direct_messages(thread_id, amount=30, use_cache=False)
        except TypeError:
            try:
                messages = self.client.direct_messages(thread_id, amount=30)
            except Exception:
                return
        except Exception:
            try:
                messages = self.client.direct_messages(thread_id, amount=30)
            except Exception:
                return

        if not messages:
            return

        try:
            messages = list(reversed(messages))
        except Exception:
            pass

        my_id_str = str(getattr(self.client, 'user_id', '') or '')

        for msg in messages:
            msg_id = getattr(msg, 'id', None)
            if msg_id is None:
                continue
            key = (thread_id, msg_id)
            if not self._try_mark_processed(key):
                continue
            if my_id_str and str(msg.user_id) == my_id_str:
                continue

            uid = str(msg.user_id)

            if self.trall_active and self.trall_text and not self.is_child:
                if not self.is_owner(uid):
                    self.executor.submit(self.send_text_reply, thread_id, msg, self.trall_text)
                    self.trall_count += 1

            if uid in self.replyraid_targets:
                target = self.replyraid_targets[uid]
                if target.get('active'):
                    text = f"{target['name']} {random.choice(self.random_texts)}"
                    self.send_text_reply(thread_id, msg, text)
                    target['count'] += 1

            if thread_id in self.sreply_instances:
                sinst = self.sreply_instances[thread_id]
                if str(sinst.get('target')) == uid:
                    sinst['last_msg_obj'] = msg

            if hasattr(msg, 'text') and msg.text:
                try:
                    self.process_command(thread_id, msg.text, msg.user_id, msg)
                except Exception as e:
                    print(f"process_command error: {str(e)[:60]}")

    def check_messages(self):
        now = time.time()
        if now < self._rate_limited_until:
            return
        try:
            threads = self.client.direct_threads(amount=20, use_cache=False)
        except TypeError:
            try:
                threads = self.client.direct_threads(amount=20)
            except Exception as e:
                err = str(e).lower()
                if 'rate' in err or '429' in err or 'too many' in err or 'wait' in err:
                    self._rate_limited_until = now + 60
                    print(f"⚠️ Rate limited @{self.username}, backoff 60s")
                return
        except Exception as e:
            err = str(e).lower()
            if 'rate' in err or '429' in err or 'too many' in err or 'wait' in err:
                self._rate_limited_until = now + 60
                print(f"⚠️ Rate limited @{self.username}, backoff 60s")
            return

        if not threads:
            return

        if not hasattr(self, '_logged_first_fetch'):
            self._logged_first_fetch = True
            print(f"👂 @{self.username} now listening to {len(threads)} threads")

        fetch_cooldown = 0.3 if self.trall_active else 2.0

        for thread in threads:
            try:
                tid = thread.id
                has_new_activity = False
                la = getattr(thread, 'last_activity_at', None)
                if la is not None:
                    try:
                        ts = la.timestamp() if hasattr(la, 'timestamp') else float(la)
                    except Exception:
                        ts = 0
                    prev = self.thread_last_activity.get(tid, 0)
                    if ts > prev:
                        has_new_activity = True
                        self.thread_last_activity[tid] = ts

                cooldown_ok = (now - self._thread_fetch_cooldown.get(tid, 0)) >= fetch_cooldown

                if has_new_activity or cooldown_ok:
                    self._thread_fetch_cooldown[tid] = now
                    self.fetch_pool.submit(self._fetch_and_process, tid)
            except Exception:
                continue

    def _health_check(self):
        now = time.time()
        if now - self.last_health_check < 60:
            return
        self.last_health_check = now
        try:
            self.client.account_info()
            self.consecutive_health_failures = 0
        except:
            self.consecutive_health_failures += 1
            if self.consecutive_health_failures >= 3:
                print(f"🔄 Re-login @{self.username}...")
                try:
                    self.client = Client()
                    self.setup_bot()
                    if self.session_id:
                        self.client.login_by_sessionid(self.session_id)
                    elif self.username and self.password:
                        self.client.login(self.username, self.password)
                    else:
                        raise Exception("No creds")
                    self.consecutive_health_failures = 0
                    print(f"✅ @{self.username} re-logged in")
                except Exception as e:
                    print(f"❌ @{self.username} re-login failed: {str(e)[:50]}")

    # ============ DISPATCH ============
    def process_command(self, thread_id, message, user_id, msg_obj=None):
        if not message:
            return False
        is_command = message.strip().startswith('/')
        is_speed_response = (thread_id in self.spm_waiting_for_speed and not is_command)
        if not is_command and not is_speed_response:
            return False

        if not self.is_owner(user_id):
            self.send_text_reply(thread_id, msg_obj, "chal tmkc 👎🏿")
            return False

        if is_speed_response:
            choice = message.strip().lower()
            if choice in ["fast", "slow"]:
                self.handle_speed_selection(thread_id, user_id, choice)
            else:
                self.spm_waiting_for_speed.pop(thread_id, None)
                self.send_text_async(thread_id, "❌ Invalid. Type 'fast' or 'slow'")
            return True

        parts = message.strip().split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        self.cmd_executor.submit(self._execute_command, thread_id, command, args, user_id, msg_obj)
        return True

    def _execute_command(self, thread_id, command, args, user_id, msg_obj=None):
        if self.is_child:
            return self.parent._execute_command(thread_id, command, args, user_id, msg_obj)
        print(f"⚡ [{self.username}] CMD: {command} args={args[:30]!r} from={user_id}")
        try:
            # ===== STOP ALL =====
            if command in ['/ruk', '/stop', '/stopall', '/kill']:
                self.send_text_async(thread_id, self.ruk_all())
            # ===== TRALL =====
            elif command == '/trall':
                self.handle_trall(thread_id, user_id, args)
            elif command == '/stroall':
                self.handle_stroall(thread_id, user_id)
            elif command == '/faster':
                self.handle_faster(thread_id, user_id)
            elif command == '/normal':
                self.handle_normal(thread_id, user_id)
            # ===== BOT MGMT =====
            elif command == '/addbot': self.handle_addbot(thread_id, user_id, args)
            elif command == '/removebot': self.handle_removebot(thread_id, user_id, args)
            elif command == '/botlist': self.handle_botlist(thread_id, user_id)
            # ===== LS =====
            elif command == '/ls':
                self.handle_ls(thread_id, user_id, args)
                self._broadcast_to_children('handle_ls', thread_id, user_id, args)
            elif command == '/stoplas':
                result = self.stop_ls()
                self._broadcast_to_children('stop_ls')
                self.send_text_async(thread_id, result)
            # ===== REPLYRAID =====
            elif command == '/replyraid':
                self.handle_replyraid(thread_id, user_id, args, msg_obj)
            elif command == '/stopreplyraid':
                self.send_text_async(thread_id, self.stop_replyraid())
            # ===== SREPLY =====
            elif command == '/sreply':
                self.handle_sreply(thread_id, user_id, args, msg_obj)
            elif command == '/stopsreply':
                self.send_text_async(thread_id, self.stop_sreply())
            # ===== REV =====
            elif command == '/rev':
                self.handle_rev(thread_id, user_id, args)
            elif command == '/stoprev':
                self.send_text_async(thread_id, self.stop_rev())
            elif command == '/revs':
                self.handle_revs(thread_id, user_id, args)
            elif command == '/setdelay':
                self.handle_setdelay(thread_id, user_id, args)
            elif command == '/srbreak':
                self.handle_srbreak(thread_id, user_id, args)
            # ===== ND =====
            elif command == '/nd':
                self.handle_nd(thread_id, user_id, args)
                self._broadcast_to_children('handle_nd', thread_id, user_id, args)
            # ===== NC =====
            elif command == '/nc': self.handle_group_rename(thread_id, user_id, args)
            elif command == '/ncdelay': self.handle_ncdelay(thread_id, user_id, args)
            # ===== TSPAM =====
            elif command == '/tspam':
                self.handle_tspam(thread_id, user_id, args)
                self._broadcast_to_children('handle_tspam', thread_id, user_id, args)
            elif command == '/stoptspam':
                result = self.stop_tspam()
                self._broadcast_to_children('stop_tspam')
                self.send_text_async(thread_id, result)
            # ===== MUSIC =====
            elif command == '/song': self.handle_song(thread_id, user_id, args)
            elif command == '/play': self.handle_play(thread_id, user_id, args)
            elif command == '/pause': self.handle_pause(thread_id, user_id)
            elif command == '/resume': self.handle_resume(thread_id, user_id)
            elif command == '/stopmusic': self.handle_stop_music(thread_id, user_id)
            elif command == '/volume': self.handle_volume(thread_id, user_id, args)
            elif command == '/playlist': self.handle_playlist(thread_id, user_id, args)
            elif command == '/repeat': self.handle_repeat(thread_id, user_id, args)
            elif command == '/lyrics': self.handle_lyrics(thread_id, user_id, args)
            elif command == '/music': self.handle_music(thread_id, user_id, args)
            elif command == '/musicsearch': self.handle_music_search(thread_id, user_id, args)
            elif command == '/queue': self.handle_queue(thread_id, user_id)
            elif command == '/skip': self.handle_skip(thread_id, user_id)
            elif command == '/loop': self.handle_loop(thread_id, user_id)
            elif command == '/genre': self.handle_genre(thread_id, user_id, args)
            elif command == '/cover': self.handle_cover(thread_id, user_id, args)
            # ===== GROUPS =====
            elif command == '/grouplist': self.handle_group_list(thread_id, user_id)
            elif command == '/groupraid': self.handle_group_raid(thread_id, user_id, args)
            elif command == '/groupspam': self.handle_group_spam(thread_id, user_id, args)
            # ===== EFFECTS =====
            elif command == '/swipe': self.handle_swipe(thread_id, user_id, args)
            elif command == '/autospam': self.handle_autospam(thread_id, user_id, args)
            elif command == '/hybrid': self.handle_hybrid(thread_id, user_id, args)
            elif command == '/massdm': self.handle_massdm(thread_id, user_id, args)
            elif command == '/ghost': self.handle_ghost(thread_id, user_id, args)
            elif command == '/matrix': self.handle_matrix(thread_id, user_id, args)
            elif command == '/glitch': self.handle_glitch(thread_id, user_id, args)
            elif command == '/echo': self.handle_echo(thread_id, user_id, args)
            elif command == '/rotate': self.handle_rotate(thread_id, user_id, args)
            elif command == '/rainbow': self.handle_rainbow(thread_id, user_id, args)
            elif command == '/bounce': self.handle_bounce(thread_id, user_id, args)
            elif command == '/morse': self.handle_morse(thread_id, user_id, args)
            elif command == '/leet': self.handle_leet(thread_id, user_id, args)
            elif command == '/spongebob': self.handle_spongebob(thread_id, user_id, args)
            elif command == '/zalgo': self.handle_zalgo(thread_id, user_id, args)
            elif command == '/vibe': self.handle_vibe(thread_id, user_id, args)
            elif command == '/capslock': self.handle_capslock(thread_id, user_id, args)
            elif command == '/mock': self.handle_mock(thread_id, user_id, args)
            elif command == '/say': self.handle_say(thread_id, user_id, args)
            elif command == '/delete': self.handle_delete(thread_id, user_id, args)
            elif command == '/seen': self.handle_seen(thread_id, user_id, args)
            elif command == '/hack': self.handle_hack(thread_id, user_id, args)
            # ===== SON MGMT =====
            elif command == '/addson': self.add_additional_owner(thread_id, user_id, args)
            elif command == '/removeson': self.remove_additional_owner(thread_id, user_id, args)
            elif command == '/sonlist': self.handle_son_list(thread_id, user_id)
            # ===== CORE =====
            elif command == '/ping': self.handle_ping(thread_id, user_id)
            elif command == '/status': self.handle_status(thread_id, user_id)
            elif command == '/help': self.handle_help(thread_id, user_id)
            elif command == '/ownerstatus': self.handle_owner_status(thread_id, user_id)
            elif command == '/owner': self.handle_owner_check(thread_id, user_id)
            elif command == '/raid':
                p = args.split(' ', 1) if args else ["", ""]
                c = p[0] if p else ""
                t = p[1] if len(p) > 1 else ""
                self.send_text_async(thread_id, self.start_counted_raid(thread_id, c, t))
            elif command == '/stopraid':
                self.send_text_async(thread_id, self.stop_raid())
            elif command == '/spam':
                self.send_text_async(thread_id, self.start_spam_loop(thread_id, args))
            elif command == '/stopspam':
                self.send_text_async(thread_id, self.stop_spam_loop())
            elif command == '/delay':
                self.send_text_async(thread_id, self.set_delay(args))
            elif command == '/spm':
                self.handle_spm_command(thread_id, user_id, args)
            elif command == '/stopspm':
                result = self.stop_spm()
                self._broadcast_to_children('stop_spm')
                self.send_text_async(thread_id, result)
            elif command == '/info': self.handle_info(thread_id, user_id)
            elif command == '/emoji': self.handle_emoji(thread_id, args, user_id)
            elif command == '/meme': self.handle_meme(thread_id, user_id)
            elif command == '/joke': self.handle_joke(thread_id, user_id)
            elif command == '/flood': self.handle_flood(thread_id, args, user_id)
            elif command == '/time': self.handle_time(thread_id, user_id)
            elif command == '/uptime': self.handle_uptime(thread_id, user_id)
            elif command == '/stats': self.handle_stats(thread_id, user_id)
            elif command == '/dice': self.handle_dice(thread_id, user_id)
            elif command == '/coin': self.handle_coin(thread_id, user_id)
            elif command == '/calc': self.handle_calc(thread_id, args, user_id)
            elif command == '/about': self.handle_about(thread_id, user_id)
            elif command == '/cmds': self.handle_cmds(thread_id, user_id)
            elif command == '/speed': self.handle_speed(thread_id, user_id)
            elif command == '/chatid': self.handle_chatid(thread_id, user_id)
            elif command == '/userid': self.handle_userid(thread_id, user_id)
            elif command == '/myinfo': self.handle_myinfo(thread_id, user_id)
            elif command == '/profile': self.handle_profile(thread_id, user_id, args)
            elif command == '/sendmsg': self.handle_sendmsg(thread_id, user_id, args)
            elif command == '/broadcast': self.handle_broadcast(thread_id, user_id, args)
            elif command == '/followers': self.handle_followers(thread_id, user_id, args)
            elif command == '/posts': self.handle_posts(thread_id, user_id, args)
            elif command == '/quote': self.handle_quote(thread_id, user_id)
            elif command == '/weather': self.handle_weather(thread_id, user_id, args)
            elif command == '/trivia': self.handle_trivia(thread_id, user_id)
            elif command == '/fact': self.handle_fact(thread_id, user_id)
            elif command == '/8ball': self.handle_8ball(thread_id, user_id, args)
            elif command == '/roll': self.handle_roll(thread_id, user_id, args)
            elif command == '/rps': self.handle_rps(thread_id, user_id, args)
            elif command == '/love': self.handle_love(thread_id, user_id, args)
            elif command == '/ascii': self.handle_ascii(thread_id, user_id, args)
            elif command == '/binary': self.handle_binary(thread_id, user_id, args)
            elif command == '/reverse': self.handle_reverse(thread_id, user_id, args)
            elif command == '/upper': self.handle_upper(thread_id, user_id, args)
            elif command == '/lower': self.handle_lower(thread_id, user_id, args)
            elif command == '/len': self.handle_len(thread_id, user_id, args)
            elif command == '/replace': self.handle_replace(thread_id, user_id, args)
            elif command == '/count': self.handle_count(thread_id, user_id, args)
            elif command == '/shuffle': self.handle_shuffle(thread_id, user_id, args)
            elif command == '/palindrome': self.handle_palindrome(thread_id, user_id, args)
            elif command == '/vowels': self.handle_vowels(thread_id, user_id, args)
            elif command == '/anagram': self.handle_anagram(thread_id, user_id, args)
            elif command == '/prime': self.handle_prime(thread_id, user_id, args)
            elif command == '/fibonacci': self.handle_fibonacci(thread_id, user_id, args)
            elif command == '/clear': self.handle_clear(thread_id, user_id)
            elif command == '/typing': self.handle_typing(thread_id, user_id)
            elif command == '/secret': self.handle_secret(thread_id, user_id)
            else:
                self.send_text_async(thread_id, "❌ Unknown command. Use /help")
        except Exception as e:
            import traceback
            print(f"❌ Command error for {command}: {e}")
            traceback.print_exc()
            try:
                self.send_text_nobreak(thread_id, f"⚠️ Error: {str(e)[:80]}")
            except:
                pass

    # ============ MAIN LOOP ============
    def run(self):
        if not self.is_child:
            print("""
╔══════════════════════════════════════════════════════╗
║               𝗕𝗢𝗧 𝗦𝗬𝗦𝗧𝗘𝗠 𝗔𝗖𝗧𝗜𝗩𝗘                 ║
╠══════════════════════════════════════════════════════╣
║  Status: 𝗢𝗣𝗘𝗥𝗔𝗧𝗜𝗢𝗡𝗔𝗟                            ║
║  Mode: 𝗧𝗥𝗔𝗟𝗟 + 𝗥𝗘𝗩 (text-only) + 𝗠𝗨𝗟𝗧𝗜-𝗕𝗢𝗧   ║
╚══════════════════════════════════════════════════════╝
            """)
            print(f"🤖 Main Bot: @{self.username}")
            print(f"👑 Owner: @{self.owner_username}")
            print(f"📋 Groups: {len(self.group_thread_ids)}")
            print(f"🔒 Auth: Only owner + sons can use commands")
            print(f"⚡ Poll interval: {self.poll_interval:.3f}s")
            print(f"💥 REV delay: {self.rev_delay:.4f}s | Break: {self.rev_break_secs:.1f}s")
            print(f"🔄 Fast polling enabled...\n")

        error_count = 0
        last_status = time.time()
        cycle = 0

        while True:
            try:
                self.check_messages()
                cycle += 1
                if cycle % 200 == 0:
                    self._health_check()
                if not self.is_child and time.time() - last_status >= 30:
                    last_status = time.time()
                    uptime = time.time() - self.start_time
                    speed = self.messages_sent / uptime if uptime > 0 else 0
                    trall = "ON" if self.trall_active else "OFF"
                    rev = len(self.rev_instances)
                    print(f"📊 {self.messages_sent} msgs | {speed:.1f}/sec | {self.command_count} cmds | {len(self.active_processes)} procs | {len(self.child_bots)+1} bots | TRALL:{trall} | REV:{rev}")
                error_count = 0
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                print(f"\n🛑 @{self.username} stopped")
                self.executor.shutdown(wait=False)
                break
            except Exception as e:
                error_count += 1
                print(f"⚠️ Loop error @{self.username} ({error_count}): {str(e)[:50]}")
                if error_count > 10:
                    print(f"⚠️ Too many errors, sleeping 30s")
                    time.sleep(30)
                    error_count = 0
                else:
                    time.sleep(1)


def start_bot():
    print("""
╔══════════════════════════════════════════════════════╗
║      𝗜𝗡𝗦𝗧𝗔𝗚𝗥𝗔𝗠 𝗥𝗔𝗜𝗗 𝗕𝗢𝗧 - 𝗣𝗥𝗢 𝗘𝗗𝗜𝗧𝗜𝗢𝗡       ║
║                 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 𝗕𝗬: 𝗥𝗘𝗩                ║
║                     𝗩𝗘𝗥𝗦𝗜𝗢𝗡 𝟲.𝟵                 ║
╚══════════════════════════════════════════════════════╝
    """)

    print("🔐 𝗟𝗢𝗚𝗜𝗡 𝗠𝗘𝗧𝗛𝗢𝗗")
    print("1️⃣  Normal Login")
    print("2️⃣  Session ID Login")
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("➤ Select (1/2): ").strip()

    username = password = ""
    session_id = None
    if choice == "2":
        print("\n🔑 Paste session ID:")
        session_id = input("➤ Session ID: ").strip()
        if not session_id:
            print("❌ Required!")
            return
    else:
        username = input("➤ Bot username: ").strip()
        password = input("➤ Bot password: ").strip()

    owner = input("➤ Your username (owner): ").strip()

    if (choice == "1" and (not username or not password)) or (choice == "2" and not session_id):
        print("❌ Credentials required!")
        return

    bot = InstagramRaidBot(
        username if choice == "1" else None,
        password if choice == "1" else None,
        owner,
        session_id if choice == "2" else None
    )

    if bot.login():
        print("\n" + "═" * 55)
        print("✅ 𝗦𝗬𝗦𝗧𝗘𝗠 𝗥𝗘𝗔𝗗𝗬")
        print("═" * 55)
        print(f"""
📋 𝗠𝗔𝗜𝗡 𝗕𝗢𝗧
├── Username: @{bot.username}
├── Owner: @{owner} (ID: {bot.owner_id or 'NOT FETCHED'})
├── Groups: {len(bot.group_thread_ids)}
├── Mode: TRALL + REV (text-only) + Multi-Bot
└── Version: 6.9

🤖 𝗔𝗖𝗧𝗜𝗩𝗘 𝗕𝗢𝗧𝗦
└── 🥇 @{bot.username} (MAIN)

➕ 𝗧𝗢 𝗔𝗗𝗗 𝗠𝗢𝗥𝗘 𝗕𝗢𝗧𝗦
├── /addbot <sessionid>
└── /addbot <username>:<password>

💥 𝗥𝗘𝗩 (TEXT SPAM ONLY, NO RENAME)
├── /rev <name>        - Text spam + break every 2s
├── /stoprev           - Stop rev
├── /revs <sec>        - Set rev speed (default 0.01)
├── /setdelay <sec>    - Set rev speed (alias)
└── /srbreak <sec>     - Set break interval (default 2.0)

📢 𝗧𝗥𝗔𝗟𝗟
├── /trall <text>      - Auto-reply to EVERY msg
├── /stroall           - Stop trall
├── /faster            - Max poll (0.05s)
└── /normal            - Normal poll (0.1s)

⭐ 𝗖𝗢𝗥𝗘 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦
├── /ls <name>         - Love spam + rename
├── /stoplas           - Stop LS
├── /replyraid <name>  - Reply raid (use as reply)
├── /stopreplyraid     - Stop replyraid
├── /sreply <name>     - 10/sec targeted spam (reply)
├── /stopsreply        - Stop sreply
├── /nc <text>         - Rename only
├── /ncdelay <sec>     - Set NC speed
├── /nd <text>         - Rename + spam
├── /tspam <name>      - Random texts
├── /raid <n> <text>   - Counted raid
├── /spam <text>       - Infinite spam
├── /spm <text>        - SPM (fast/slow)
├── /groupraid         - Raid all GCs
├── /groupspam         - Spam all GCs
├── /ruk  /stop  /kill - KILL ALL
├── /stopmusic         - Music only stop
├── /addbot /botlist /removebot - Bot mgmt
├── /addson /removeson /sonlist - Son mgmt
└── /help              - Full command list
        """)
        if bot.owner_id is None:
            print("⚠️  WARNING: owner_id not fetched at login — will retry at runtime (30s cooldown)")
        print("🚀 Starting bot engine...")
        bot.run()
    else:
        print("\n❌ 𝗟𝗢𝗚𝗜𝗡 𝗙𝗔𝗜𝗟𝗘𝗗")


if __name__ == "__main__":
    start_bot()