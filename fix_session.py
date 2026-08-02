print("=== FIX SESSION STARTED ===")

import os
import pyrogram

print("Pyrogram location:", pyrogram.__file__)

path = os.path.join(
    os.path.dirname(pyrogram.__file__),
    "session",
    "session.py"
)

print("Session path:", path)

with open(path, "r") as f:
    code = f.read()

target = """            elif isinstance(result, raw.types.BadMsgNotification):
                raise BadMsgNotification(result.error_code)"""

replacement = """            elif isinstance(result, raw.types.BadMsgNotification):
                if result.error_code in (16, 17):
                    from pyrogram.session.internals.msg_id import MsgId

                    MsgId.server_time += 25 if result.error_code == 16 else -25

                    print(f"[Auto-Fix] MTProto Error {result.error_code}")
                    print(f"[Auto-Fix] New server_time: {MsgId.server_time}")

                    return await self._send(data, wait_response, timeout)

                raise BadMsgNotification(result.error_code)"""

found = target in code

print("TARGET FOUND:", found)

if found:
    code = code.replace(target, replacement)

    with open(path, "w") as f:
        f.write(code)

    print("Patch applied successfully!")
else:
    print("Target code not found or already patched.")

idx = code.find("BadMsgNotification")
if idx != -1:
    print("\n===== CODE AROUND BadMsgNotification =====")
    print(code[max(0, idx - 200): idx + 500])
    print("==========================================")

print("=== PATCH FINISHED ===")
