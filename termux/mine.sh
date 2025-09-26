#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
# UzvarUA NPC Generator v1.0 🍵
# Створює функцію, manifest.json і npc_dialogue.json для NPC з дзвоном і tellraw

command -v python >/dev/null 2>&1 || {
  echo "❌ Python не знайдено. Встанови його через: pkg install python"
  exit 1
}

# === CONFIG ===
PACK_NAME="UzvarUA_NPC_Pack"
UUID1=$(python -c "import uuid; print(uuid.uuid4())")
UUID2=$(python -c "import uuid; print(uuid.uuid4())")
FUNC_NAME="gong_react"
SOUND_ID="custom.gong"
TEXT="§d☕ UzvarUA: Ти пробудив силу дзвону!"

# Функція
pack_uzvar(){
  robby="pack_icon.png"
  echo "👽 Не забудьте добавити $robby"
}

[[ -z "$UUID1" || -z "$UUID2" ]] && {
  echo "❌ Не вдалося згенерувати UUID"
  exit 1
}

# === FILE TREE ===
mkdir -p "$PACK_NAME/functions"
mkdir -p "$PACK_NAME/sounds/custom"
mkdir -p "$PACK_NAME/texts"

# === FUNCTION FILE ===
cat > "$PACK_NAME/functions/$FUNC_NAME.mcfunction" <<EOF
playsound $SOUND_ID @initiator
tellraw @initiator {"rawtext":[{"text":"$TEXT"}]}
EOF

# === MANIFEST FILE ===
cat > "$PACK_NAME/manifest.json" <<EOF
{
  "format_version": 2,
  "header": {
    "name": "$PACK_NAME",
    "description": "NPC reacts with sound and branded message",
    "uuid": "$UUID1",
    "version": [1, 0, 0]
  },
  "modules": [
    {
      "type": "data",
      "uuid": "$UUID2",
      "version": [1, 0, 0]
    }
  ]
}
EOF

# === NPC DIALOGUE FILE ===
cat > "$PACK_NAME/npc_dialogue.json" <<EOF
{
  "npc_dialogue": {
    "on_open": {
      "commands": [
        "function $FUNC_NAME"
      ]
    }
  }
}
EOF

# === DONE ===
echo -e "\n✅ UzvarUA NPC Pack створено!"
echo "📁 $PACK_NAME готовий до копіювання в /games/com.mojang/behavior_packs/"
echo "🔔 Не забудь додати gong.ogg у sounds/custom/"
pack_uzvar
