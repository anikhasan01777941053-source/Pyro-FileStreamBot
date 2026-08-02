path = '/usr/local/lib/python3.14/dist-packages/pyrogram/sync.py'
with open(path, 'r') as f:
    text = f.read()

# আগের ভাঙা কোড ক্লিয়ার করা
text = text.replace('try:\nmain_loop', 'main_loop')
text = text.replace('try:\n    main_loop', 'main_loop')

target = 'main_loop = asyncio.get_event_loop()'
replacement = '''try:
    main_loop = asyncio.get_event_loop()
except RuntimeError:
    main_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(main_loop)'''

text = text.replace(target, replacement)

with open(path, 'w') as f:
    f.write(text)

print("Pyrogram Sync Patched Successfully!")
