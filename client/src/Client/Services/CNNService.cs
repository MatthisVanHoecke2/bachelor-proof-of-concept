using Project.Shared.CNN;
using Project.Shared.LLM;
using System.Net.Http.Json;

namespace Project.Client.Services;

public class CNNService : IImageClassifierService
{
    private readonly HttpClient client;
    private const string endpoint = "cnn";

    public CNNService(HttpClient client)
    {
        this.client = client;
    }

    public async Task<ImageClassifierDto.Index?> PostImageAsync(MultipartFormDataContent content)
    {
        var response = await client.PostAsync($"{endpoint}/upload", content);
        return await response.Content.ReadFromJsonAsync<ImageClassifierDto.Index?>();
    }
}
