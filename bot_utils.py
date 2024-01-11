import json

def get_message_template(template_name):
    with open("templates.json", "r", encoding="utf-8") as templates_file:
        templates = json.load(templates_file)
    return templates.get(template_name, "Default message template not found.")

def load_config():
    with open("config.json", "r", encoding='utf-8') as config_file:
        config = json.load(config_file)
        return config

def not_allowed(message):
    config = load_config()
    chat_id = message.chat.id
    command = message.text.split()[0]

    if chat_id not in config['masters'] and chat_id not in config['allowed_groups']:
        return True
    else:
        return False