#!/bin/bash

API_URL="http://localhost:5002/phrases"
INPUT_FILE="phrases.json"
OFFSET="${1:-0}"
LIMIT="${2:-9999}"
shift 2 # Shift past offset and limit
LEVEL_FILTERS=("$@") # Remaining args are levels, if any

# Ensure jq is available
if ! command -v jq &> /dev/null; then
  echo "❌ 'jq' is not installed. Please install it to use this script."
  exit 1
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "❌ Input file '$INPUT_FILE' not found."
  exit 1
fi

# Build jq filter string for level filtering
jq_filter='.'
if [[ ${#LEVEL_FILTERS[@]} -gt 0 ]]; then
  jq_levels=$(printf '"%s",' "${LEVEL_FILTERS[@]}")
  jq_levels="[${jq_levels%,}]"
  jq_filter+=" | map(select(.level as \$lvl | \$lvl | IN(${jq_levels}[])))"
fi

# Run jq with slicing for offset and limit
jq -c "$jq_filter | .[$OFFSET:$((OFFSET + LIMIT))]" "$INPUT_FILE" | jq -c '.[]' | while read -r item; do
  level=$(echo "$item" | jq -r '.level')
  text=$(echo "$item" | jq -r '.phrase')
  translation=$(echo "$item" | jq -r '.translation')
  categories=$(echo "$item" | jq -c '.category')

  json=$(jq -n \
    --arg level "$level" \
    --arg text "$text" \
    --arg translation "$translation" \
    --argjson category "$categories" \
    '{level: $level, text: $text, translation: $translation, category: $category}')

  echo "📤 Posting [$level]: $text"
  curl -s -X POST -H "Content-type: application/json" -d "$json" "$API_URL"
  echo # newline
done

