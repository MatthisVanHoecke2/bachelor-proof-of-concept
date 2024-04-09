using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.JSInterop;
using Project.Shared.LLM;

namespace Project.Client.LLM;
public partial class Index : IDisposable, IAsyncDisposable
{
    private string? Uuid { get; set; }
    private string textfield = default!;
    public bool Loading { get; set; } = true;
    public List<string> systemMessages = new();
    public string endMessage { get; set; } = default!;

    [Inject] IChatService chatService { get; set; } = default!;
    [Inject] IJSRuntime JS { get; set; } = default!;
    [Inject] ILogger<Index> Logger { get; set; } = default!;

    private List<ChatMessage> chatMessages = new();

    private Task<string> starting = default!;

    protected async override Task OnInitializedAsync()
    {
        await base.OnInitializedAsync();

        systemMessages.Add("Starting chat service...");
        try
        {
            starting = chatService.StartChatAsync();
            Uuid = await starting;
            Loading = false;
            systemMessages.Add("Chat service is running.");
        }
        catch(Exception ex)
        {
            systemMessages.Add("Chat service failed to start. Please make sure the back-end is running.");
            Logger.LogError(ex, ex.Message);
        }
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
        try
        {
            ChatMessageDto.Index? response = await chatService.GetIndexAsync(request, Uuid!);
            if (response == null) return;
            chatMessages[^1].Message = response.Output;
        }
        catch(Exception ex)
        {
            chatMessages.RemoveAt(chatMessages.Count-1);
            endMessage = "Session expired.";
            Logger.LogError(ex, ex.Message);
        }
        Loading = false;
        StateHasChanged();
        ScrollToEnd();
    }

    private async void ScrollToEnd()
    {
        await Task.Delay(1);
        await JS.InvokeVoidAsync("onScrollEvent", null);
    }

    public void Dispose()
    {
        try
        {
            chatService.StopChatAsync(Uuid!);
            Loading = false;
        }
        catch (Exception ex)
        {
            Logger.LogError(ex, ex.Message);
        }
        GC.SuppressFinalize(this);
    }

    public async ValueTask DisposeAsync()
    {
        try
        {
            await starting;
            Dispose();
        }
        catch(Exception ex)
        {
            Logger.LogError(ex, ex.Message);
        }
        GC.SuppressFinalize(this);
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