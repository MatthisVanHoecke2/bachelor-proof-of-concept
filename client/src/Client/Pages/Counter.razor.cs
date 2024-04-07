using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.JSInterop;
using Shared.LLM;

namespace Client.Pages;
public partial class Counter
{
    private string? Uuid { get; set; }
    private string textfield = default!;
    public bool Loading { get; set; } = true;
    public List<string> systemMessages = new();

    [Inject] IChatService chatService { get; set; } = default!;
    [Inject] IJSRuntime JS { get; set; } = default!;

    private List<ChatMessage> chatMessages = new();

    protected async override Task OnInitializedAsync()
    {
        await base.OnInitializedAsync();

        systemMessages.Add("Starting chat service...");
        Uuid = await chatService.StartChatAsync();
        Loading = false;
        systemMessages.Add("Chat service is running.");
    }

    private void OnEnter(KeyboardEventArgs args)
    {
        if (!Loading && (args.Code == "Enter" || args.Code == "NumpadEnter"))
        {
            OnSend();
        }
    }

    private void OnSend()
    {
        chatMessages.Add(new ChatMessage(MessageSender.Human, textfield));
        ChatMessageRequest.Index request = new() { Value = textfield };
        textfield = "";
        Loading = true;
        chatMessages.Add(new ChatMessage(MessageSender.Assistant, ""));
        ScrollToEnd();
        SendRequest(request);
    }

    private async void SendRequest(ChatMessageRequest.Index request)
    {
        ChatMessageDto.Index? response = await chatService.GetIndexAsync(request, Uuid!);
        Loading = false;
        if (response == null) return;
        chatMessages[chatMessages.Count - 1].Message = response.Output;
        StateHasChanged();
        ScrollToEnd();
    }

    private async void ScrollToEnd()
    {
        await Task.Delay(1);
        await JS.InvokeVoidAsync("onScrollEvent", null);
    }

    private class ChatMessage
    {
        public MessageSender Sender { get; }
        public string Message { get; set; }
        public ChatMessage(MessageSender sender, string message)
        {
            this.Sender = sender;
            this.Message = message;
        }
    }
}