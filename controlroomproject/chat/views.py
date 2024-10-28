from django.shortcuts import render
import ollama

# Chat type configurations
CHAT_CONFIGS = {
    "general": {
        "title": "General Assistant",
        "system_prompt": "You are a helpful assistant that can discuss any topic.",
    },
    "financial": {
        "title": "Financial Advisor",
        "system_prompt": "You are a financial advisor. Provide advice about personal finance, investments, and money management.",
    },
    "fitness": {
        "title": "Fitness Trainer",
        "system_prompt": "You are a personal fitness trainer. Provide advice about exercise, workout plans, and healthy lifestyle.",
    },
    "coding": {
        "title": "Coding Assistant",
        "system_prompt": "You are a programming expert. Help with code, debugging, and software development best practices.",
    },
}


def chat(request):
    context = {
        "messages": [],
        "chat_type": "general",  # default chat type
        "chat_title": CHAT_CONFIGS["general"]["title"],
    }

    if request.user.is_authenticated:
        # Get chat type from URL parameter or form data
        chat_type = (
            request.GET.get("type") or request.POST.get("chat_type") or "general"
        )
        if chat_type not in CHAT_CONFIGS:
            chat_type = "general"

        context["chat_type"] = chat_type
        context["chat_title"] = CHAT_CONFIGS[chat_type]["title"]

        if request.method == "POST":
            user_message = request.POST.get("message", "")
            if user_message:
                # Call Ollama API with system prompt based on chat type
                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content": CHAT_CONFIGS[chat_type]["system_prompt"],
                        },
                        {"role": "user", "content": user_message},
                    ],
                )

                # Add messages to context
                context["messages"] = [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response["message"]["content"]},
                ]

    return render(request, "chat/chat.html", context)
