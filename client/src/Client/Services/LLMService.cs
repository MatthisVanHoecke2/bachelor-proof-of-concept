using Shared.LLM;
using System.Net.Http.Json;

namespace Client.Services;

public class LLMService : IChatService
{
    private readonly HttpClient client;
    private const string endpoint = "llm";

    public LLMService(HttpClient client)
    {
        this.client = client;
    }

    public async Task<ChatMessageDto.Detail?> GetDetailAsync(ChatMessageRequest.Index request, string uuid)
    {
        var response = await client.PostAsJsonAsync($"{endpoint}/response/{uuid}", request);
        return await response.Content.ReadFromJsonAsync<ChatMessageDto.Detail?>();
    }

    public async Task<ChatMessageDto.Index?> GetIndexAsync(ChatMessageRequest.Index request, string uuid)
    {
        var response = await client.PostAsJsonAsync($"{endpoint}/response/{uuid}", request);
        return await response.Content.ReadFromJsonAsync<ChatMessageDto.Index?>();
    }

    public async Task<string> StartChatAsync()
    {
        var response = await client.GetFromJsonAsync<string>($"{endpoint}/start");
        return response!;
    }

    public async Task<string> StopChatAsync(string uuid)
    {
        var response = await client.GetFromJsonAsync<string>($"{endpoint}/stop/{uuid}");
        return response!;
    }
}
