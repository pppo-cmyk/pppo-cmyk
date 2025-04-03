
import language_tool_python

def get_suggestions(text):
    tool = language_tool_python.LanguageTool('pl')
    matches = tool.check(text)
    suggestions = []
    for match in matches:
        suggestions.append(f"{match.context} -> {match.message}")
    return suggestions if suggestions else ["Brak sugestii"]
