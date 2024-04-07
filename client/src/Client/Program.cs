using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Client;
using MudBlazor.Services;
using Shared.LLM;
using Client.Services;

string MLAPI = "http://localhost:8000/";

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.RootComponents.Add<App>("#app");
builder.RootComponents.Add<HeadOutlet>("head::after");

builder.Services.AddHttpClient<HttpClient>("UIClient", client => client.BaseAddress = new Uri(builder.HostEnvironment.BaseAddress));
builder.Services.AddHttpClient<MLClient>("UIClient.MachineLearning", client => client.BaseAddress = new Uri(MLAPI));
builder.Services.AddScoped(sp => sp.GetRequiredService<IHttpClientFactory>()
       .CreateClient("UIClient"));
builder.Services.AddScoped(sp => sp.GetRequiredService<IHttpClientFactory>()
       .CreateClient("UIClient.MachineLearning"));

builder.Services.AddScoped<IChatService, LLMService>();
builder.Services.AddMudServices();

await builder.Build().RunAsync();
