import requests
import time
import json

class SeedanceBytePlusNode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "endpoint_id": ("STRING", {"default": ""}),
                "prompt": ("STRING", {"multiline": True, "default": "A majestic dragon."}),
                "ratio": (["16:9", "9:16", "4:3", "3:4", "1:1"], {"default": "16:9"}),
                "duration": ("INT", {"default": 5, "min": 5, "max": 15, "step": 5}),
                "generate_audio": ("BOOLEAN", {"default": False}),
            }
        }

    # 出力を3つに増やしました
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("video_url", "task_id", "debug_msg")
    FUNCTION = "run_seedance"
    CATEGORY = "BytePlus/Seedance"

    def run_seedance(self, api_key, endpoint_id, prompt, ratio, duration, generate_audio):
        base_url = "https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": endpoint_id,
            "content": [{"type": "text", "text": prompt}],
            "ratio": ratio,
            "duration": duration,
            "generate_audio": generate_audio,
            "watermark": False
        }

        try:
            response = requests.post(base_url, headers=headers, json=payload)
            if response.status_code != 200:
                err_raw = response.text
                print(f"!!! Submit Error: {err_raw}")
                return ("", "NONE", f"SUBMIT_ERROR: {err_raw}")
            task_id = response.json().get("id")
        except Exception as e:
            return ("", "NONE", f"EXCEPTION: {str(e)}")

        status_url = f"{base_url}/{task_id}"
        
        for _ in range(150):
            try:
                res = requests.get(status_url, headers=headers)
                res_data = res.json()
                status = res_data.get("status")
                
                # コンソールへの進捗表示
                print(f"Polling Task {task_id}: {status}")

                if status == "succeeded":
                    # 解析した結果、URLは res_data["content"]["video_url"] にあることが判明
                    video_url = res_data.get("content", {}).get("video_url", "")
                    
                    # デバッグ用に全データを整形
                    debug_info = json.dumps(res_data, indent=2)
                    
                    # コンソールにも表示
                    print(f"✨ SUCCESS!\nURL: {video_url}\nRAW: {debug_info}")
                    
                    return (video_url, task_id, debug_info)

                elif status in ["failed", "cancelled"]:
                    err_detail = json.dumps(res_data, indent=2)
                    print(f"❌ FAILED:\n{err_detail}")
                    return ("", task_id, f"FAILED: {err_detail}")
                
                time.sleep(10)
            except Exception as e:
                print(f"Polling connection error: {e}")
                time.sleep(5)
                
        return ("", task_id, "TIMEOUT")

