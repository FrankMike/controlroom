from django.shortcuts import render
import ollama

# Create your views here.


def chat(request):
    context = {"messages": []}
    if request.user.is_authenticated:
        if request.method == "POST":
            user_message = request.POST.get("message", "")
            if user_message:
                # Call Ollama API
                response = ollama.chat(
                    model="llama3.2",
                    messages=[{"role": "user", "content": user_message}],
                )

                # Add messages to context
                context["messages"] = [
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response["message"]["content"]},
                ]

    return render(request, "chat/chat.html", context)
