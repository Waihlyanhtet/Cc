#!/usr/bin/env python3
import sys
import io
import os

# Limit မှတ်တမ်းသိမ်းမည့် ဖိုင်အမည်
LOG_FILE = ".hits_limit.log"
LIMIT_COUNT = 30

def check_status():
    """ယခင်က Limit ပြည့်ထားခြင်း ရှိ၊ မရှိ စစ်ဆေးရန်"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            status = f.read().strip()
            if status == "REACHED":
                print("\n[!] Error: ဒီ ID အတွက် HITS 30 Limit ပြည့်သွားပါပြီ။")
                print("[!] နောက်တစ်ကြိမ် ထပ်မံ အသုံးပြု၍ မရတော့ပါ။\n")
                os._exit(0)

class HitWatcher(io.StringIO):
    def __init__(self):
        super().__init__()
        self.terminal = sys.__stdout__

    def write(self, s):
        self.terminal.write(s)
        
        # Screenshot_20260514-141713.png အရ "HITS: 30" ကို စစ်ဆေးခြင်း
        upper_s = s.upper()
        if f"HITS: {LIMIT_COUNT}" in upper_s or f"HITS:{LIMIT_COUNT}" in upper_s:
            self.terminal.write(f"\n\n[!] Target HITS ({LIMIT_COUNT}) ပြည့်သွားပါပြီ။")
            
            # Limit ပြည့်သွားကြောင်း ဖိုင်ထဲမှာ မှတ်တမ်းရေးမယ်
            with open(LOG_FILE, "w") as f:
                f.write("REACHED")
            
            self.terminal.write("[*] မှတ်တမ်းသိမ်းဆည်းပြီးပါပြီ။ Script ကို ရပ်လိုက်ပါပြီ။\n")
            os._exit(0)

# ၁။ အရင်ဆုံး status ကို စစ်မယ်
check_status()

# ၂။ Output ကို လမ်းကြောင်းလွှဲမယ်
sys.stdout = HitWatcher()

try:
    # ၃။ Starlink ကို Run မယ်
    import starlink
except KeyboardInterrupt:
    os._exit(0)
except Exception as e:
    # aiofiles error တက်ခဲ့လျှင် မြင်နိုင်ရန်
    print(f"Error: {e}")