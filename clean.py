import json

with open('cases.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cleaned_cases = []
raw_cases = data.get('cases', data.get('cases ', []))

for case in raw_cases:
    clean_case = {}
    for k, v in case.items():
        clean_key = k.strip() # Bo'sh joylarni olib tashlash
        if isinstance(v, dict):
            clean_dict = {vk.strip(): (vv.strip() if isinstance(vv, str) else vv) for vk, vv in v.items()}
            clean_case[clean_key] = clean_dict
        elif isinstance(v, list):
            clean_case[clean_key] = [item.strip() if isinstance(item, str) else item for item in v]
        else:
            clean_case[clean_key] = v.strip() if isinstance(v, str) else v
    cleaned_cases.append(clean_case)

with open('cases.json', 'w', encoding='utf-8') as f:
    json.dump({"cases": cleaned_cases}, f, indent=2, ensure_ascii=False)

print("✅ cases.json muvaffaqiyatli tozalandi!")