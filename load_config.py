import yaml

def load_config(yaml_path="config.yaml"):
    """Загружает настройки из YAML файла."""
    with open(yaml_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

config = load_config()
general = config["general"]
midjourney = config["midjourney"]

#general
MESSAGE_REPEAT_COUNT = general["MESSAGE_REPEAT_COUNT"]
HEADLESS_MODE = general["HEADLESS_MODE"]
WAITING_TIME = general["WAITING_TIME"]
TXT_PATH = general["TXT_PATH"]
DISCORD_SERVER_ID = general["DISCORD_SERVER_ID"]
DISCORD_CHANNEL_ID = general["DISCORD_CHANNEL_ID"]

TARGET_CHANNEL_URL = f"https://discord.com/channels/{DISCORD_SERVER_ID}/{DISCORD_CHANNEL_ID}"

#midjourney promt

ar_value = midjourney["ar_value"]
style_value = midjourney["style_value"]
c_value = midjourney["c_value"]
s_value = midjourney["s_value"]
v_value = midjourney["v_value"]
quality_value = midjourney["quality_value"]
weird_value = midjourney["weird_value"]
negative_value = midjourney["negative_value"]
add_value = midjourney["add_value"]



if __name__ == "__main__":
    print(TARGET_CHANNEL_URL,)