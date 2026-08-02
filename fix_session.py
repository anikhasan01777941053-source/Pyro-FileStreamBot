import os
import pyrogram

path = os.path.join(
    os.path.dirname(pyrogram.__file__),
    "session",
    "session.py"
)
with open(path, 'r') as f:
    code = f.read()

target = '            if isinstance(result, raw.types.BadMsgNotification):\n                raise BadMsgNotification(result.error_code)'

replacement = '''            if isinstance(result, raw.types.BadMsgNotification):
                if result.error_code in (16, 17):
                    print(f"[Auto-Fix] MTProto Error {result.error_code} detected! Adjusting time offset...")
                    self.time_offset += 25 if result.error_code == 16 else -25
                    return await self._send(data, timeout)
                raise BadMsgNotification(result.error_code)'''

if target in code:
    code = code.replace(target, replacement)
    with open(path, 'w') as f:
        f.write(code)
    print("Patched session.py successfully!")
else:
    print("Target code updated or already patched.")
