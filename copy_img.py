import shutil

src = r"C:\Users\Manu\.gemini\antigravity-ide\brain\f24ec22c-a34f-456d-9ff7-d1ef6629d823\support_agent_popup_1783073975581.png"
dst = r"c:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\services_images\support_agent_popup.png"

shutil.copy2(src, dst)
print("Image copied successfully!")
